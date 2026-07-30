
const DEFAULT_IGNORE_DIR_NAMES = [
  "node_modules", ".git", "__pycache__", ".pytest_cache",
  "venv", ".venv", "env", "ENV",
  "dist", "build", ".next", ".nuxt", "target",
  "bin", "obj", ".idea", ".vscode", ".gradle", ".tox",
  ".mypy_cache", "coverage", "vendor", "Pods",
  ".dart_tool", ".pub-cache", ".parcel-cache", ".cache",
];

const DEFAULT_IGNORE_FILE_NAMES = [".DS_Store", "Thumbs.db"];
const DEFAULT_IGNORE_FILE_SUFFIXES = [".pyc", ".pyo", ".class"];

function isDefaultIgnored(relativePath) {
  const segments = relativePath.split("/");
  const filename = segments[segments.length - 1];

  if (segments.some((seg) => DEFAULT_IGNORE_DIR_NAMES.includes(seg))) {
    return true;
  }
  if (DEFAULT_IGNORE_FILE_NAMES.includes(filename)) {
    return true;
  }
  if (DEFAULT_IGNORE_FILE_SUFFIXES.some((suf) => filename.endsWith(suf))) {
    return true;
  }
  return false;
}

function gitignorePatternToRegex(pattern) {
  let p = pattern.trim();
  const anchored = p.startsWith("/");
  if (anchored) p = p.slice(1);
  if (p.endsWith("/")) p = p.slice(0, -1);

  p = p.replace(/[.+^${}()|[\]\\]/g, "\\$&"); // escape regex specials
  p = p.replace(/\*\*/g, "\u0000"); // placeholder for **
  p = p.replace(/\*/g, "[^/]*");
  p = p.replace(/\u0000/g, ".*");
  p = p.replace(/\?/g, ".");

  const body = anchored ? "^" + p : "(^|/)" + p;
  return new RegExp(body + "($|/)");
}

function parseGitignore(text) {
  return text
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith("#") && !l.startsWith("!"))
    .map(gitignorePatternToRegex);
}

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsText(file);
  });
}

async function filterFolderFiles(fileList) {
  const files = [...fileList];

  const gitignoreFile = files.find((f) => {
    const rel = f.webkitRelativePath || "";
    const parts = rel.split("/");
    return parts.length === 2 && parts[1] === ".gitignore";
  });

  let gitignoreRegexes = [];
  if (gitignoreFile) {
    try {
      const text = await readFileAsText(gitignoreFile);
      gitignoreRegexes = parseGitignore(text);
    } catch (e) {
      console.warn("Could not read .gitignore, skipping it", e);
    }
  }

  const kept = [];
  let skipped = 0;
  let skippedBytes = 0;

  files.forEach((f) => {
    const rel = f.webkitRelativePath || f.name;
    const rootRelative = rel.split("/").slice(1).join("/");

    const ignored =
      isDefaultIgnored(rel) ||
      gitignoreRegexes.some((re) => re.test(rootRelative));

    if (ignored) {
      skipped++;
      skippedBytes += f.size;
      return;
    }

    kept.push(f);
  });

  return { kept, skipped, skippedBytes };
}