console.time("pl-js");

function setView(view) {
    const container = document.getElementById('projectContainer');
    if (view === 'grid') {
        container.className = 'grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4';
    } else {
        container.className = 'grid grid-cols-1 gap-4';
    }
}

document.querySelectorAll('.category-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.category-btn').forEach(b => {
            b.className = 'category-btn px-3 py-1 rounded-lg text-xs bg-gray-100 text-gray-700';
        });
        this.className = 'category-btn px-3 py-1 rounded-lg text-xs bg-indigo-600 text-white';

        const category = this.dataset.category;
        const cards = document.querySelectorAll('.project-card');

        cards.forEach(card => {
            if (category === 'all') {
                card.style.display = '';
            } else {
                card.style.display = card.dataset.status === category ? '' : 'none';
            }
        });
    });
});

const searchInput = document.getElementById('search');
if (searchInput && searchInput.dataset.serverSearch) {
  const resultsWrapper = document.getElementById('resultsWrapper');
  let debounceTimer = null;
  let latestRequestId = 0;

  function runSearch() {
    const query = searchInput.value.trim();
    const requestId = ++latestRequestId;

    const url = new URL(window.location.href);
    url.searchParams.set('q', query);
    url.searchParams.delete('page');

    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(res => res.text())
      .then(html => {
        if (requestId !== latestRequestId) return;
        resultsWrapper.innerHTML = html;
        history.replaceState(null, '', url);
      })
      .catch(err => console.error('Search failed', err));
  }

  searchInput.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(runSearch, 350);
  });
}

document.addEventListener('click', function(e) {
    const card = e.target.closest('.project-card');
    if (!card) return;
    if (e.target.closest('a')) return;
    const link = card.querySelector('a[href*="project-detail"]');
    if (link) {
        window.location.href = link.href;
    }
});

document.getElementById('sort').addEventListener('change', function() {
    const container = document.getElementById('projectContainer');
    const cards = Array.from(document.querySelectorAll('.project-card'));
    const sortBy = this.value;

    cards.sort((a, b) => {
        let aVal, bVal;

        if (sortBy === '-created_at') {
            const aDate = new Date(a.querySelector('.text-gray-500:last-child')?.textContent || '');
            const bDate = new Date(b.querySelector('.text-gray-500:last-child')?.textContent || '');
            return bDate - aDate;
        } else if (sortBy === 'title') {
            aVal = a.dataset.title || '';
            bVal = b.dataset.title || '';
            return aVal.localeCompare(bVal);
        } 
        return 0;
    });

    cards.forEach(card => container.appendChild(card));
});


console.timeEnd("pl-js");