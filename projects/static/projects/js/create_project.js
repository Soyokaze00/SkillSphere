let status = "{{ project_form.status.value|default:'OPEN' }}";
let tags = [];

const title = document.getElementById("title");
const desc = document.getElementById("desc");
const titleCount = document.getElementById("titleCount");
const descCount = document.getElementById("descCount");
const tagInput = document.getElementById("tagInput");
const tagBox = document.getElementById("tagBox");
const publishBtn = document.getElementById("publishBtn");
const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const fileList = document.getElementById("fileList");
const statusInput = document.getElementById("statusInput");
const tagsInput = document.getElementById("tagsInput");

function updateCounts() {
  titleCount.textContent = title.value.length;
  descCount.textContent = desc.value.length;
  validate();
}

title.addEventListener("input", updateCounts);
desc.addEventListener("input", updateCounts);

updateCounts();


const statusBtns = document.querySelectorAll(".status-btn");

statusBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    status = btn.dataset.status;
    statusInput.value = status;

    statusBtns.forEach((b) => {
      b.classList.remove(
        "ring-2", "ring-indigo-500",
        "bg-green-100", "text-green-700", "dark:bg-green-500/20", "dark:text-green-400",
        "bg-yellow-100", "text-yellow-700", "dark:bg-yellow-500/20", "dark:text-yellow-400",
        "bg-gray-100", "text-gray-700", "dark:bg-gray-500/20", "dark:text-gray-300",
      );

      if (b.dataset.status === "OPEN") {
        b.className = "status-btn w-full px-3 py-2 rounded-xl text-sm font-medium transition bg-green-100 text-green-700 dark:bg-green-500/20 dark:text-green-400";
      } else if (b.dataset.status === "IN_PROGRESS") {
        b.className = "status-btn w-full px-3 py-2 rounded-xl text-sm font-medium transition bg-yellow-100 text-yellow-700 dark:bg-yellow-500/20 dark:text-yellow-400";
      } else {
        b.className = "status-btn w-full px-3 py-2 rounded-xl text-sm font-medium transition bg-gray-100 text-gray-700 dark:bg-gray-500/20 dark:text-gray-300";
      }
    });

    btn.classList.add("ring-2", "ring-indigo-500");
    validate();
  });
});

function renderTags() {
  tagBox.innerHTML = "";
  tags.forEach((t, i) => {
    const el = document.createElement("span");
    el.className =
      "text-xs bg-indigo-100 text-indigo-600 px-2 py-1 rounded-lg cursor-pointer hover:bg-indigo-200";
    el.textContent = t;

    el.onclick = () => {
      tags.splice(i, 1);
      renderTags();
      updateTagsInput();
    };

    tagBox.appendChild(el);
  });
  updateTagsInput();
}

function updateTagsInput() {
  tagsInput.value = tags.join(",");
}

document.getElementById("addTagBtn").onclick = () => {
  const tag = tagInput.value.trim();
  if (tag && !tags.includes(tag)) {
    tags.push(tag);
    tagInput.value = "";
    renderTags();
    validate();
  }
};

tagInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    document.getElementById("addTagBtn").click();
  }
});

const folderInput = document.getElementById("folderInput");
const folderBtn = document.getElementById("folderBtn");

function mergeFilesIntoInput(newFiles) {
  const dt = new DataTransfer();
  // keep whatever was already selected...
  [...fileInput.files].forEach((f) => dt.items.add(f));
  // ...and add the newly picked/dropped ones on top
  [...newFiles].forEach((f) => dt.items.add(f));
  fileInput.files = dt.files;
  fileInput.dispatchEvent(new Event("change"));
}

let fileListExpanded = false;
const FILE_LIST_COLLAPSED_LIMIT = 3;

function renderFileList() {
  fileList.innerHTML = "";

  const allFiles = [...fileInput.files];
  const showCount = fileListExpanded
    ? allFiles.length
    : Math.min(FILE_LIST_COLLAPSED_LIMIT, allFiles.length);

  allFiles.slice(0, showCount).forEach((file) => {
    const div = document.createElement("div");
    div.className = "p-3 border rounded-xl bg-gray-50 text-sm";
    const icon = file.name.includes("/") ? "📁 " : "📄 ";

    div.textContent =
      icon + file.name + " (" + (file.size / 1024).toFixed(1) + " KB)";

    fileList.appendChild(div);
  });

  if (allFiles.length > FILE_LIST_COLLAPSED_LIMIT) {
    const toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.className =
      "w-full text-center text-xs font-semibold text-indigo-600 hover:text-indigo-700 py-2 border border-dashed border-indigo-200 rounded-xl";

    toggleBtn.textContent = fileListExpanded
      ? "▲ Show less"
      : `▾ Show ${allFiles.length - FILE_LIST_COLLAPSED_LIMIT} more file(s)`;

    toggleBtn.onclick = () => {
      fileListExpanded = !fileListExpanded;
      renderFileList();
    };

    fileList.appendChild(toggleBtn);
  }

  const totalBytes = [...fileInput.files].reduce((sum, f) => sum + f.size, 0);
  const totalEl = document.getElementById("totalSizeMsg");
  if (totalEl) {
    if (fileInput.files.length > 0) {
      const mb = (totalBytes / (1024 * 1024)).toFixed(1);
      totalEl.textContent = `Total: ${fileInput.files.length} file(s), ~${mb} MB`;
      totalEl.className =
        totalBytes > 150 * 1024 * 1024
          ? "text-xs text-red-500 mt-1 font-semibold"
          : "text-xs text-gray-500 mt-1";
    } else {
      totalEl.textContent = "";
    }
  }

  const filePaths = document.getElementById("filePaths");
  if (filePaths) {
    filePaths.value = JSON.stringify([...fileInput.files].map((f) => f.name));
  }

  validate();
}

fileInput.onchange = renderFileList;
folderBtn.onclick = () => folderInput.click();
document.getElementById("browseFilesBtn").onclick = () => fileInput.click();
folderBtn.onclick = () => folderInput.click();

folderInput.onchange = async (e) => {
  const { kept, skipped, skippedBytes } = await filterFolderFiles(e.target.files);

  const renamed = kept.map((f) => {
    const relPath = f.webkitRelativePath || f.name;
    return new File([f], relPath, { type: f.type, lastModified: f.lastModified });
  });

  mergeFilesIntoInput(renamed);
  folderInput.value = ""; // allow re-picking the same folder later

  const msgEl = document.getElementById("folderSkipMsg");
  if (msgEl) {
    if (skipped > 0) {
      const mb = (skippedBytes / (1024 * 1024)).toFixed(1);
      msgEl.textContent =
        `Skipped ${skipped} file(s) (~${mb} MB) like node_modules, .git, venv, build output, and anything matched by .gitignore.`;
    } else {
      msgEl.textContent = "";
    }
  }
};

dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("border-indigo-500", "bg-indigo-50");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("border-indigo-500", "bg-indigo-50");
});

dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("border-indigo-500", "bg-indigo-50");
  mergeFilesIntoInput(e.dataTransfer.files);
});

function validate() {
  const ok = title.value.trim() && desc.value.trim();

  if (ok) {
    publishBtn.disabled = false;
    publishBtn.classList.remove("bg-gray-300", "text-gray-600");
    publishBtn.classList.add("bg-indigo-600", "hover:bg-indigo-700");
  } else {
    publishBtn.disabled = true;
    publishBtn.classList.remove("bg-indigo-600", "hover:bg-indigo-700");
    publishBtn.classList.add("bg-gray-300", "text-gray-600");
  }
}

document.getElementById("projectForm").addEventListener("submit", function (e) {
  const ok = title.value.trim() && desc.value.trim();

  if (!ok) {
    e.preventDefault();
    alert("Please fill all required fields");
    return;
  }


  const btn = document.getElementById("publishBtn");
  btn.textContent = "⏳ Publishing...";
  btn.disabled = true;

});