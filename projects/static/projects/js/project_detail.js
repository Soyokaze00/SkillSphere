console.time("project-detail-js");


function switchTab(tab) {

  document.querySelectorAll(".tab-panel").forEach(el => {
    el.classList.add("hidden");
  });

  const target = document.getElementById("tab-" + tab);
  if (target) {
    target.classList.remove("hidden")

  }
;

  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.classList.remove("text-indigo-600", "border-indigo-600");
    btn.classList.add("text-gray-500", "border-transparent");
  });

  const activeBtn = document.querySelector(`[data-tab="${tab}"]`);
  if (activeBtn) {
    activeBtn.classList.add("text-indigo-600", "border-indigo-600");
    activeBtn.classList.remove("text-gray-500", "border-transparent");
  }
}

document.addEventListener('DOMContentLoaded', function() {
  var label = document.querySelector('.file-upload-label');
  var wrapper = document.querySelector('.file-input-wrapper');
  var input = wrapper ? wrapper.querySelector('input[type="file"]') : null;

  console.log('label پیدا شد؟', label);
  console.log('wrapper پیدا شد؟', wrapper);
  console.log('input پیدا شد؟', input);

  if (label && input) {
    label.addEventListener('click', function() {
      console.log('کلیک شد، دارم input.click() صدا می‌زنم');
      input.click();
    });

    input.addEventListener('change', function() {
      console.log('فایل انتخاب شد:', input.files);
      var nameText = document.querySelector('.file-name-text');
      if (nameText) {
        nameText.textContent = input.files.length > 0 ? input.files[0].name : 'No file chosen';
      }
    });
  }
});