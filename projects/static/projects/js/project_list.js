   console.time("pl-js");

// کل کد

   
   // View toggle
        function setView(view) {
            const container = document.getElementById('projectContainer');
            if (view === 'grid') {
                container.className = 'grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4';
            } else {
                container.className = 'grid grid-cols-1 gap-4';
            }
        }

        // Category filter
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                // Update button styles
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

        // Search filter
        document.getElementById('search').addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            const cards = document.querySelectorAll('.project-card');

            cards.forEach(card => {
                const title = card.dataset.title || '';
                if (title.includes(query)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });

        // Sort functionality
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
                } else if (sortBy === '-deadline') {
                    const aDeadline = a.querySelector('[data-deadline]')?.dataset.deadline || '';
                    const bDeadline = b.querySelector('[data-deadline]')?.dataset.deadline || '';
                    return bDeadline.localeCompare(aDeadline);
                }
                return 0;
            });

            cards.forEach(card => container.appendChild(card));
        });

        // Project click
        function onProjectClick(projectId) {
            window.location.href = `/projects/${projectId}/`;
        }

        // Add click event to cards
        document.querySelectorAll('.project-card').forEach(card => {
            card.addEventListener('click', function(e) {
                // Prevent if clicking on a link inside
                if (e.target.closest('a')) return;
                const link = this.querySelector('a[href*="project-detail"]');
                if (link) {
                    window.location.href = link.href;
                }
            });
        });
console.timeEnd("pl-js");
