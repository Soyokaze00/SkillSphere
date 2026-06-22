/* ---------------- DATA ---------------- */
const categories = ["Design", "UI/UX", "Templates", "Code", "Other"];
let selectedCategory = "{{ project_form.category.value|default:'' }}";
let status = "{{ project_form.status.value|default:'open' }}";
let tags = [];

/* ---------------- ELEMENTS ---------------- */
const title = document.getElementById("title");
const desc = document.getElementById("desc");
const titleCount = document.getElementById("titleCount");
const descCount = document.getElementById("descCount");
const deadline = document.getElementById("deadline");
const tagInput = document.getElementById("tagInput");
const tagBox = document.getElementById("tagBox");
const publishBtn = document.getElementById("publishBtn");
const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const fileList = document.getElementById("fileList");
const categoryInput = document.getElementById("categoryInput");
const statusInput = document.getElementById("statusInput");
const tagsInput = document.getElementById("tagsInput");

/* ---------------- COUNT ---------------- */
function updateCounts() {
  titleCount.textContent = title.value.length;
  descCount.textContent = desc.value.length;
  validate();
}

title.addEventListener("input", updateCounts);
desc.addEventListener("input", updateCounts);

// Initial counts
updateCounts();

/* ---------------- CATEGORY ---------------- */
const catBox = document.getElementById("categories");

categories.forEach((c) => {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.textContent = c;
  btn.className = `px-3 py-2 rounded-xl bg-gray-100 text-xs transition ${
    selectedCategory === c ? "bg-indigo-600 text-white" : ""
  }`;

  btn.onclick = () => {
    selectedCategory = c;
    categoryInput.value = c;
    [...catBox.children].forEach((x) =>
      x.classList.remove("bg-indigo-600", "text-white"),
    );
    btn.classList.add("bg-indigo-600", "text-white");
    validate();
  };

  catBox.appendChild(btn);
});

if (selectedCategory) {
  categoryInput.value = selectedCategory;
}

/* ---------------- STATUS TOGGLE ---------------- */
const statusBtns = document.querySelectorAll(".status-btn");

statusBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    status = btn.dataset.status;
    statusInput.value = status;

    statusBtns.forEach((b) => {
      b.classList.remove(
        "ring-2",
        "ring-indigo-500",
        "bg-green-100",
        "text-green-700",
        "bg-yellow-100",
        "text-yellow-700",
        "bg-gray-100",
        "text-gray-700",
      );

      if (b.dataset.status === "open") {
        b.className =
          "status-btn w-full px-3 py-2 rounded-xl text-sm bg-green-100 text-green-700";
      } else if (b.dataset.status === "progress") {
        b.className =
          "status-btn w-full px-3 py-2 rounded-xl text-sm bg-yellow-100 text-yellow-700";
      } else {
        b.className =
          "status-btn w-full px-3 py-2 rounded-xl text-sm bg-gray-100 text-gray-700";
      }
    });

    btn.classList.add("ring-2", "ring-indigo-500");
    validate();
  });
});

/* ---------------- TAGS ---------------- */
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

/* ---------------- UPLOAD ---------------- */
dropzone.onclick = () => fileInput.click();

fileInput.onchange = (e) => {
  [...e.target.files].forEach((file) => {
    const div = document.createElement("div");
    div.className = "p-3 border rounded-xl bg-gray-50 text-sm";

    div.textContent =
      "📄 " + file.name + " (" + (file.size / 1024).toFixed(1) + " KB)";

    fileList.appendChild(div);
  });

  validate();
};

// Drag and drop support
dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("border-indigo-500", "bg-indigo-50");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("border-indigo-500", "bg-indigo-50");
});

dropzone.addEventListener("drop", (e) => {
  e.preventDefault();

  const dt = new DataTransfer();

  [...e.dataTransfer.files].forEach(file => {
    dt.items.add(file);
  });

  fileInput.files = dt.files;
  fileInput.dispatchEvent(new Event("change"));
});

/* ---------------- VALIDATION ---------------- */
function validate() {
  const ok =
    title.value.trim() &&
    desc.value.trim() &&
    selectedCategory &&
    deadline.value;

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
/* ---------------- FORM SUBMIT ---------------- */
// در JavaScript - حذف publishBtn.onclick و جایگزینی با این:

document.getElementById("projectForm").addEventListener("submit", function (e) {
  // اعتبارسنجی
  const ok =
    title.value.trim() &&
    desc.value.trim() &&
    selectedCategory &&
    deadline.value;

  if (!ok) {
    e.preventDefault();
    alert("Please fill all required fields");
    return;
  }

  // اگر اعتبارسنجی موفق بود، فرم ارسال میشه
  // می‌تونید یک loading indicator اضافه کنید
  const btn = document.getElementById("publishBtn");
  btn.textContent = "⏳ Publishing...";
  btn.disabled = true;

  // توجه: اینجا نیازی به setTimeout نیست چون فرم خودش ارسال میشه
});
