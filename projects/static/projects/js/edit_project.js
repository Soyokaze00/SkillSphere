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

document.getElementById("editProjectForm").addEventListener("submit", function (e) {
  const ok = title.value.trim() && desc.value.trim();
  if (!ok) {
    e.preventDefault();
    alert("Please fill all required fields");
    return;
  }
  saveBtn.textContent = "⏳ Saving...";
  saveBtn.disabled = true;
});

document.addEventListener("DOMContentLoaded", function () {
  const label = document.querySelector(".file-upload-label");
  const wrapper = document.querySelector(".file-input-wrapper");
  const input = wrapper ? wrapper.querySelector('input[type="file"]') : null;
  const folderBtn = document.getElementById("folderBtn");
  const folderInput = document.getElementById("folderInput");
  const filePaths = document.getElementById("filePaths");

  function renderFileNameLabel() {
    const nameText = document.querySelector(".file-name-text");
    if (nameText && input) {
      if (input.files.length === 0) {
        nameText.textContent = "No file chosen";
      } else if (input.files.length === 1) {
        nameText.textContent = input.files[0].name;
      } else {
        nameText.textContent = input.files.length + " files selected";
      }
    }
    if (filePaths && input) {
      filePaths.value = JSON.stringify([...input.files].map((f) => f.name));
    }
  }

  if (label && input) {
    label.addEventListener("click", function () {
      input.click();
    });
    input.addEventListener("change", renderFileNameLabel);
  }

  if (folderBtn && folderInput && input) {
    folderBtn.addEventListener("click", function () {
      folderInput.click();
    });

    folderInput.addEventListener("change", function () {
      const renamed = [...folderInput.files].map(function (f) {
        const relPath = f.webkitRelativePath || f.name;
        return new File([f], relPath, { type: f.type, lastModified: f.lastModified });
      });

      const dt = new DataTransfer();
      [...input.files].forEach((f) => dt.items.add(f));
      renamed.forEach((f) => dt.items.add(f));
      input.files = dt.files;

      renderFileNameLabel();
      folderInput.value = "";
    });
  }
});