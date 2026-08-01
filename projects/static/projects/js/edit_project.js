const title = document.getElementById("title");
const desc = document.getElementById("desc");
const titleCount = document.getElementById("titleCount");
const descCount = document.getElementById("descCount");
const tagInput = document.getElementById("tagInput");
const tagBox = document.getElementById("tagBox");
const saveBtn = document.getElementById("saveBtn");
const statusInput = document.getElementById("statusInput");
const tagsInput = document.getElementById("tagsInput");

let tags = Array.isArray(window.INITIAL_TAGS) ? [...window.INITIAL_TAGS] : [];

function updateCounts() {
  titleCount.textContent = title.value.length;
  descCount.textContent = desc.value.length;
}
title.addEventListener("input", updateCounts);
desc.addEventListener("input", updateCounts);
updateCounts();

const statusBtns = document.querySelectorAll(".status-btn");
statusBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    statusInput.value = btn.dataset.status;
    statusBtns.forEach((b) => b.classList.remove("ring-2", "ring-indigo-500"));
    btn.classList.add("ring-2", "ring-indigo-500");
  });
});

function renderTags() {
  tagBox.innerHTML = "";
  tags.forEach((t, i) => {
    const el = document.createElement("span");
    el.className = "text-xs bg-indigo-100 text-indigo-600 px-2 py-1 rounded-lg cursor-pointer hover:bg-indigo-200";
    el.textContent = t;
    el.onclick = () => {
      tags.splice(i, 1);
      renderTags();
    };
    tagBox.appendChild(el);
  });
  tagsInput.value = tags.join(",");
}
renderTags();

document.getElementById("addTagBtn").onclick = () => {
  const tag = tagInput.value.trim();
  if (tag && !tags.includes(tag)) {
    tags.push(tag);
    tagInput.value = "";
    renderTags();
  }
};

tagInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    document.getElementById("addTagBtn").click();
  }
});

if (editProjectForm) {
  editProjectForm.addEventListener("submit", function (e) {
    const isTitleValid = title ? title.value.trim().length > 0 : true;
    const isDescValid = desc ? desc.value.trim().length > 0 : true;

    if (!isTitleValid || !isDescValid) {
      e.preventDefault();
      alert("لطفاً تمامی فیلدهای ضروری (عنوان و توضیحات) را پر کنید.");
      return;
    }

    if (saveBtn) {
      saveBtn.disabled = true; // فوری، نه با تاخیر
      saveBtn.textContent = "⏳ Saving...";
    }
  });
}