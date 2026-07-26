function randomSeed() {
  return Math.random().toString(36).slice(2, 10);
}

function renderAvatarGrid(seeds) {
  const grid = document.getElementById('avatarGrid');
  const hiddenInput = document.querySelector('input[name="avatar_seed"]');
  if (!grid || !hiddenInput) return;

  grid.innerHTML = '';

  function highlight(selectedBox) {
    grid.querySelectorAll('.avatar-option').forEach((box) => {
      box.style.borderColor = '#e5e7eb'; // gray-200
      box.style.backgroundColor = 'transparent';
    });
    selectedBox.style.borderColor = '#6366f1'; // indigo-500
    selectedBox.style.backgroundColor = 'rgba(99, 102, 241, 0.08)';
  }

  seeds.forEach((seed) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'avatar-option cursor-pointer';
    wrapper.style.width = '56px';
    wrapper.style.height = '56px';
    wrapper.style.borderRadius = '9999px';
    wrapper.style.overflow = 'hidden';
    wrapper.style.border = '2px solid #e5e7eb';
    wrapper.style.transition = 'border-color 0.15s, background-color 0.15s';

    const img = document.createElement('img');
    img.src = `https://api.dicebear.com/9.x/identicon/svg?seed=${seed}`;
    img.style.width = '100%';
    img.style.height = '100%';

    wrapper.appendChild(img);

    if (hiddenInput.value === seed) {
      wrapper.style.borderColor = '#6366f1';
      wrapper.style.backgroundColor = 'rgba(99, 102, 241, 0.08)';
    }

    wrapper.addEventListener('click', () => {
      hiddenInput.value = seed;
      highlight(wrapper);
    });

    grid.appendChild(wrapper);
  });
}

document.addEventListener('DOMContentLoaded', function() {
  const hiddenInput = document.querySelector('input[name="avatar_seed"]');
  const existingSeed = hiddenInput ? hiddenInput.value : '';

  const seeds = existingSeed
    ? [existingSeed, randomSeed(), randomSeed(), randomSeed(), randomSeed(), randomSeed(), randomSeed(), randomSeed()]
    : Array.from({ length: 8 }, randomSeed);

  renderAvatarGrid(seeds);

  const shuffleBtn = document.getElementById('shuffleAvatars');
  if (shuffleBtn) {
    shuffleBtn.addEventListener('click', () => {
      renderAvatarGrid(Array.from({ length: 8 }, randomSeed));
    });
  }
});