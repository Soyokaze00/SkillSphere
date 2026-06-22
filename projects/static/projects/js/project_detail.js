console.time("project-detail-js");

// کل کد

function switchTab(tab) {

  // hide all tabs
  document.querySelectorAll(".tab-panel").forEach(el => {
    el.classList.add("hidden");
  });

  // show active tab
  const target = document.getElementById("tab-" + tab);
  if (target) {
    target.classList.remove("hidden")

  }
;

  // reset buttons
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.classList.remove("text-indigo-600", "border-indigo-600");
    btn.classList.add("text-gray-500", "border-transparent");
  });

  // active button
  const activeBtn = document.querySelector(`[data-tab="${tab}"]`);
  if (activeBtn) {
    activeBtn.classList.add("text-indigo-600", "border-indigo-600");
    activeBtn.classList.remove("text-gray-500", "border-transparent");
  }
}

// default tab
document.addEventListener("DOMContentLoaded", () => {
  switchTab("files");
});
console.timeEnd("project-detail-js");
