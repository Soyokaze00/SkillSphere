from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from .models import EmailVerification, CustomUser, Follow
from .utils import generate_code, send_verification_email
from .forms import EmailRequestForm, CodeVerificationForm, SignupForm, ProfileEditForm
from django.utils import timezone
from datetime import timedelta
from projects.models import Project
from django.db.models import Q
from notifications.utils import create_notification
from django.urls import reverse


def email_verification_view(request):

    email_form = EmailRequestForm(request.POST or None)
    code_form = CodeVerificationForm(request.POST or None)
    context = {'email_form': email_form, 'code_form': code_form}

    if 'send_code' in request.POST and email_form.is_valid():
        email = email_form.cleaned_data['email']

        if CustomUser.objects.filter(email=email).exists():
            email_form.add_error('email', "User with this email already exists.")
        else:
            code = generate_code()
            verification, _ = EmailVerification.objects.update_or_create(
                email=email,
                defaults={'code': code, 'is_verified': False, 'created_at': timezone.now()}
            )
            send_verification_email(email, code)
            request.session['email'] = email
            context['code_sent'] = True
            context['remaining_seconds'] = 300

    elif 'verify_code' in request.POST and code_form.is_valid():
        email = request.session.get('email')
        code = code_form.cleaned_data['code']
        
        if not email:
            return redirect('users:email-verification')

        verification = EmailVerification.objects.filter(email=email).first()
        
        if verification and verification.code == code:
            if timezone.now() < (verification.created_at + timedelta(minutes=5)):
                verification.is_verified = True
                verification.save()
                return redirect('users:signup')
            else:
                context['error'] = "Code expired. Please request a new one."
        else:
            context['error'] = "Invalid code."
            context['code_sent'] = True

    return render(request, 'users/email_verification.html', context)


def resend_code(request):
    email = request.session.get("email")

    if not email:
        return redirect("users:email-verification")

    verification = EmailVerification.objects.filter(
        email=email
    ).first()

    if verification:
        expiration_time = verification.created_at + timedelta(minutes=5)

        if timezone.now() < expiration_time:
            remaining_seconds = int(
                (expiration_time - timezone.now()).total_seconds()
            )

            form = CodeVerificationForm()

            return render(
                request,
                "users/verify_code.html",
                {
                    'form': form,
                    "error": (
                        f"You can request a new code in "
                        f"{remaining_seconds} seconds."
                    ),
                    "remaining_seconds": remaining_seconds,
                }
            )

    code = generate_code()

    verification, created = EmailVerification.objects.get_or_create(
        email=email
    )

    verification.code = code
    verification.is_verified = False
    verification.created_at = timezone.now()

    verification.save()

    send_verification_email(email, code)

    return redirect("users:verify-code")


def complete_signup(request):
    email = request.session.get("email")

    if not email:
        return redirect("users:request-code")

    form = SignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        if CustomUser.objects.filter(email=email).exists():
            return render(request, "users/signup.html", {
                "form": form,
                "error": "User already exists"
            })

        verification = EmailVerification.objects.filter(
            email=email,
            is_verified=True
        ).first()

        if not verification:
            return render(request, "users/signup.html", {
                "form": form,
                "error": "Email not verified"
            })

        CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        request.session.pop("email", None)

        return redirect("users:login")

    return render(request, "users/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("USERNAME:", username)
        print("PASSWORD:", password)

        user = authenticate(request, username=username, password=password)

        print("AUTH RESULT:", user)

        if user is not None:
            login(request, user)
            return redirect("dashboard:home") 
        else:
            return render(request, "users/login.html", {
                "error": "Invalid credentials"
            })

    return render(request, "users/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("users:login")



@login_required
@require_POST
def delete_account_view(request):
    user = request.user
    logout(request) 
    user.delete()  
    return redirect(f"{reverse('users:login')}?account_deleted=1")


def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    is_own_profile = request.user == profile_user

    projects = Project.objects.filter(
        Q(owner=profile_user) | Q(memberships__user=profile_user)
    ).distinct()

    if not is_own_profile:
        projects = projects.filter(visibility=Project.PUBLIC)
        
    projects = projects.order_by("-created_at")

    is_following = (
        request.user.is_authenticated
        and not is_own_profile
        and Follow.objects.filter(follower=request.user, following=profile_user).exists()
    )

    return render(request, "users/profile.html", {
        "profile_user": profile_user,
        "projects": projects,
        "project_count": projects.count(),
        "is_own_profile": is_own_profile,
        "is_following": is_following,
        "follower_count": profile_user.followers.count(),
        "following_count": profile_user.following.count(),
    })


@login_required
@require_POST
def toggle_follow(request, username):
    """
    Toggle the current user following `username`. Returns JSON so the
    profile page (and the project detail sidebar) can flip the button
    state without a full page reload -- same pattern as the like/save
    toggles elsewhere in the app.
    """
    target = get_object_or_404(CustomUser, username=username)

    if target == request.user:
        return HttpResponseForbidden("You can't follow yourself.")

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target,
    )

    if not created:
        follow.delete()
        following = False
    else:
        following = True
        create_notification(
            user=target,
            title="New follower",
            message=f"{request.user.username} started following you.",
            notification_type="follow",
            link=f"/users/profile/{target.username}/",
        )

    return JsonResponse({
        "following": following,
        "follower_count": target.followers.count(),
    })


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:profile", username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            if request.POST.get("clear_photo") == "1" and "profile_image" not in request.FILES:
                if user.profile_image:
                    user.profile_image.delete(save=False)
                user.profile_image = None

            user.save()
            return redirect("users:profile", username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})