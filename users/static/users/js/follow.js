function getCookie(name) {
  const match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return match ? decodeURIComponent(match[2]) : null;
}

document.addEventListener('DOMContentLoaded', function () {
  const followBtn = document.getElementById('followBtn');
  if (!followBtn) return;

  const followLabel = document.getElementById('followLabel');

  followBtn.addEventListener('click', function () {
    const url = followBtn.dataset.followUrl;
    followBtn.disabled = true;

    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
    })
      .then(function (res) {
        if (!res.ok) throw new Error('Follow request failed');
        return res.json();
      })
      .then(function (data) {
        followBtn.dataset.following = data.following;

        if (data.following) {
          followBtn.classList.remove('bg-indigo-600', 'text-white');
          followBtn.classList.add('bg-gray-100', 'text-gray-700');
          if (followLabel) followLabel.textContent = 'Following';
        } else {
          followBtn.classList.remove('bg-gray-100', 'text-gray-700');
          followBtn.classList.add('bg-indigo-600', 'text-white');
          if (followLabel) followLabel.textContent = '+ Follow';
        }

        const followerCountEl = document.getElementById('ownerFollowers')
          || document.getElementById('followerCount');
        if (followerCountEl && typeof data.follower_count === 'number') {
          followerCountEl.textContent = data.follower_count;
        }
      })
      .catch(function (err) {
        console.error(err);
        alert('There was an error updating your follow status. Please try again.');
      })
      .finally(function () {
        followBtn.disabled = false;
      });
  });
});