from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import EmailVerification, CustomUser
from .utils import generate_code, send_verification_email
from .forms import EmailRequestForm, CodeVerificationForm, SignupForm
from django.utils import timezone
from datetime import timedelta


def request_code(request):
    form = EmailRequestForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]

        if CustomUser.objects.filter(email=email).exists():
            return render(
                request,
                "users/request_code.html",
                {
                    "form": form,
                    "error": "An account with this email already exists."
                }
            )

        code = generate_code()

        EmailVerification.objects.update_or_create(
            email=email,
            defaults={
                "code": code, 
                "is_verified": False,
                "created_at": timezone.now(),
                }
        )
        print("POST DATA:", request.POST)
        print("FORM VALID:", form.is_valid())
        print("FORM ERRORS:", form.errors)

        send_verification_email(email, code)

        request.session["email"] = email

        return redirect("users:verify-code")

    return render(request, "users/request_code.html", {"form": form})



def verify_code(request):
    email = request.session.get("email")

    if not email:
        return redirect("users:request-code")

    verification = EmailVerification.objects.filter(
        email=email
    ).first()

    if not verification:
        return redirect("users:request-code")

    expiration_time = verification.created_at + timedelta(minutes=5)

    print("EMAIL:", verification.email)
    print("CREATED:", verification.created_at)
    print("NOW:", timezone.now())
    print("EXPIRES:", expiration_time)

    remaining_seconds = max(
        0,
        int((expiration_time - timezone.now()).total_seconds())
    )

    print("REMAINING:", remaining_seconds)

    remaining_seconds = max(
        0,
        int((expiration_time - timezone.now()).total_seconds())
    )

    form = CodeVerificationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        code = form.cleaned_data["code"]

        record = EmailVerification.objects.filter(
            email=email,
            code=code,
            is_verified=False
        ).first()

        if not record:
            return render(
                request,
                "users/verify_code.html",
                {
                    "form": form,
                    "remaining_seconds": remaining_seconds,
                    "error": "Invalid code"
                }
            )

        if timezone.now() > expiration_time:
            return render(
                request,
                "users/verify_code.html",
                {
                    "form": form,
                    "remaining_seconds": 0,
                    "error": "Code expired. Request a new one."
                }
            )

        record.is_verified = True
        record.save()

        return redirect("users:signup")

    return render(
        request,
        "users/verify_code.html",
        {
            "form": form,
            "remaining_seconds": remaining_seconds,
        }
    )



def resend_code(request):
    email = request.session.get("email")

    if not email:
        return redirect("users:request-code")

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

        if user is None:
            return render(request, "users/login.html", {
                "error": "Invalid credentials"
            })

        login(request, user)
        return render(request, "dashboard/home.html")

    return redirect("dashboard:home")


@login_required
def logout_view(request):
    logout(request)
    return redirect("users:login")