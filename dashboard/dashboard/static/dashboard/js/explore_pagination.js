document.addEventListener('DOMContentLoaded', function () {
  const wrapper = document.getElementById('explore-results-wrapper');
  if (!wrapper) return;

  function loadPage(url, pushState = true) {
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(response => response.text())
      .then(html => {
        wrapper.innerHTML = html;
        if (pushState) {
          window.history.pushState({}, '', url);
        }
        wrapper.scrollIntoView({ behavior: 'smooth', block: 'start' });
      })
      .catch(err => console.error('Pagination load failed:', err));
  }

  wrapper.addEventListener('click', function (e) {
    const link = e.target.closest('.page-link');
    if (!link) return;
    e.preventDefault();
    loadPage(link.href);
  });

  window.addEventListener('popstate', function () {
    loadPage(window.location.href, false);
  });
});