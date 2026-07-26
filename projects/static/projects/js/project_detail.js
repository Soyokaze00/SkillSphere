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


// ===== File tree (GitHub-style) =====
  function renderFileTree() {
    const container = document.getElementById('fileTree');
    const dataEl = document.getElementById('fileTreeData');
    const noFilesMsg = document.getElementById('noFilesMsg');
    if (!container || !dataEl) return;

    let tree;
    try {
      tree = JSON.parse(dataEl.textContent);
    } catch (e) {
      return;
    }

    if (Object.keys(tree.folders).length === 0 && tree.files.length === 0) {
      noFilesMsg.classList.remove('hidden');
      return;
    }

    function formatSize(bytes) {
      if (bytes < 1024) return bytes + ' B';
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
      return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }

    function buildFolderRow(name, depth) {
      const row = document.createElement('div');
      row.className = 'flex items-center gap-2 py-1.5 px-2 rounded-lg hover:bg-gray-50 group cursor-pointer select-none';
      row.style.paddingLeft = (depth * 20 + 8) + 'px';
      row.innerHTML =
        '<span class="chevron text-gray-400 text-xs w-3 inline-block">▶</span>' +
        '<span>📁</span>' +
        '<span class="font-semibold text-gray-800 dark:text-white dark:group-hover:text-gray-800">' + name + '</span>';
      return row;
    }

    function buildFileRow(file, depth) {
      const row = document.createElement('div');
      row.className = 'flex items-center gap-2 py-1.5 px-2 rounded-lg hover:bg-gray-50';
      row.style.paddingLeft = (depth * 20 + 28) + 'px';

      const link = document.createElement('a');
      link.href = file.detail_url;
      link.className = 'flex-1 flex items-center gap-2 text-gray-700 hover:text-indigo-600 truncate';
      link.innerHTML = '<span>📄</span><span class="truncate">' + file.name + '</span>';

      const size = document.createElement('span');
      size.className = 'text-xs text-gray-400 whitespace-nowrap';
      size.textContent = formatSize(file.size);

      const download = document.createElement('a');
      download.href = file.download_url;
      download.setAttribute('download', file.name);
      download.className = 'text-xs text-indigo-600 hover:text-indigo-700 whitespace-nowrap';
      download.textContent = '⬇';

      row.appendChild(link);
      row.appendChild(size);
      row.appendChild(download);
      return row;
    }

    function renderNode(node, depth) {
      const fragment = document.createDocumentFragment();

      Object.keys(node.folders).forEach((name) => {
        const sub = node.folders[name];
        const folderRow = buildFolderRow(name, depth);
        const childWrap = document.createElement('div');
        childWrap.className = 'hidden';
        childWrap.appendChild(renderNode(sub, depth + 1));

        folderRow.addEventListener('click', () => {
          const isHidden = childWrap.classList.contains('hidden');
          childWrap.classList.toggle('hidden');
          folderRow.querySelector('.chevron').textContent = isHidden ? '▼' : '▶';
        });

        fragment.appendChild(folderRow);
        fragment.appendChild(childWrap);
      });

      node.files.forEach((file) => {
        fragment.appendChild(buildFileRow(file, depth));
      });

      return fragment;
    }

    container.appendChild(renderNode(tree, 0));
  }



document.addEventListener('DOMContentLoaded', function() {
  var label = document.querySelector('.file-upload-label');
  var wrapper = document.querySelector('.file-input-wrapper');
  var input = wrapper ? wrapper.querySelector('input[type="file"]') : null;

  // console.log('Clicked label, triggering file input click');
  // console.log('wrapper found?', wrapper);
  // console.log('input found?', input);
 
  renderFileTree();

  function renderFileNameLabel() {
    var nameText = document.querySelector('.file-name-text');
    if (nameText && input) {
      if (input.files.length === 0) {
        nameText.textContent = 'No file chosen';
      } else if (input.files.length === 1) {
        nameText.textContent = input.files[0].name;
      } else {
        nameText.textContent = input.files.length + ' files selected';
      }
    }

    // Keep the parallel path list in sync so the backend can tell which
    // files came from a folder (Django strips '/' from the real filename).
    var filePaths = document.getElementById('filePaths');
    if (filePaths && input) {
      filePaths.value = JSON.stringify([...input.files].map(function(f) { return f.name; }));
    }
  }

  if (label && input) {
    label.addEventListener('click', function() {
      console.log('Clicked label, triggering file input click');
      input.click();
    });

    input.addEventListener('change', function() {
      console.log('فایل انتخاب شد:', input.files);
      renderFileNameLabel();
    });
  }

  // ===== Upload Folder =====
  var folderInput = document.getElementById('folderInput');
  if (folderInput && input) {
    var folderBtn = document.getElementById('folderBtn');
    if (folderBtn) {
      folderBtn.addEventListener('click', function() {
        folderInput.click();
      });
    }

    folderInput.addEventListener('change', function() {
      var renamed = [...folderInput.files].map(function(f) {
        var relPath = f.webkitRelativePath || f.name;
        return new File([f], relPath, { type: f.type, lastModified: f.lastModified });
      });

      var dt = new DataTransfer();
      [...input.files].forEach(function(f) { dt.items.add(f); });
      renamed.forEach(function(f) { dt.items.add(f); });
      input.files = dt.files;

      renderFileNameLabel();
      folderInput.value = ''; // allow re-picking the same folder later
    });
  }

  // ===== Like button =====
  function getCookie(name) {
    const match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return match ? decodeURIComponent(match[2]) : null;
  }

  const likeBtn = document.getElementById('likeBtn');
  if (likeBtn) {
    likeBtn.addEventListener('click', function() {
      const url = likeBtn.dataset.likeUrl;
      likeBtn.disabled = true;

      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
        },
      })
        .then(res => {
          if (!res.ok) throw new Error('Like request failed');
          return res.json();
        })
        .then(data => {
          const icon = document.getElementById('likeIcon');
          const statLikes = document.getElementById('statLikes');
          if (statLikes) statLikes.textContent = data.like_count;

          if (data.liked) {
            likeBtn.classList.remove('bg-white/15');
            likeBtn.classList.add('bg-red-500');
            icon.setAttribute('fill', 'currentColor');
            likeBtn.title = 'Unlike';
          } else {
            likeBtn.classList.remove('bg-red-500');
            likeBtn.classList.add('bg-white/15');
            icon.setAttribute('fill', 'none');
            likeBtn.title = 'Like';
          }
        })

        .catch(err => {
          console.error(err);
          alert('There was an error processing your like. Please try again.');
        })
        .finally(() => {
          likeBtn.disabled = false;
        });
    });
  }


// ===== Share menu =====
  const shareBtn = document.getElementById('shareBtn');
  const shareMenu = document.getElementById('shareMenu');

  if (shareBtn && shareMenu) {
    const shareUrl = shareBtn.dataset.shareUrl;
    const shareTitle = shareBtn.dataset.shareTitle || document.title;

    document.body.appendChild(shareMenu);
    shareMenu.style.position = 'fixed';
    shareMenu.style.zIndex = '9999';

    function positionShareMenu() {
      const rect = shareBtn.getBoundingClientRect();
      shareMenu.style.top = (rect.bottom + 8) + 'px';
      shareMenu.style.left = 'auto';
      shareMenu.style.right = (window.innerWidth - rect.right) + 'px';
    }

    shareBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      const isHidden = shareMenu.classList.contains('hidden');
      if (isHidden) positionShareMenu();
      shareMenu.classList.toggle('hidden');
    });

    document.addEventListener('click', function(e) {
      if (!shareMenu.contains(e.target) && e.target !== shareBtn) {
        shareMenu.classList.add('hidden');
      }
    });

    window.addEventListener('resize', function() {
      if (!shareMenu.classList.contains('hidden')) positionShareMenu();
    });
    window.addEventListener('scroll', function() {
      if (!shareMenu.classList.contains('hidden')) positionShareMenu();
    }, true);

    const gmailBtn = document.getElementById('shareGmailBtn');
    if (gmailBtn) {
      gmailBtn.addEventListener('click', function() {
        const subject = encodeURIComponent('Check out this project: ' + shareTitle);
        const body = encodeURIComponent(shareTitle + '\n\n' + shareUrl);
        window.open(
          'https://mail.google.com/mail/?view=cm&fs=1&su=' + subject + '&body=' + body,
          '_blank'
        );
        shareMenu.classList.add('hidden');
      });
    }

    const mailBtn = document.getElementById('shareMailBtn');
    if (mailBtn) {
      mailBtn.addEventListener('click', function() {
        const subject = encodeURIComponent('Check out this project: ' + shareTitle);
        const body = encodeURIComponent(shareTitle + '\n\n' + shareUrl);
        window.location.href = 'mailto:?subject=' + subject + '&body=' + body;
        shareMenu.classList.add('hidden');
      });
    }

    const copyBtn = document.getElementById('shareCopyBtn');
    if (copyBtn) {
      copyBtn.addEventListener('click', function() {
        navigator.clipboard.writeText(shareUrl).then(function() {
          const original = copyBtn.innerHTML;
          copyBtn.textContent = '✓ Copied!';
          setTimeout(function() {
            copyBtn.innerHTML = original;
          }, 1500);
        }).catch(function() {
          alert(shareUrl);
        });
        shareMenu.classList.add('hidden');
      });
    }

    // ===== Send directly via SMTP =====
    const emailInput = document.getElementById('shareEmailInput');
    const emailSendBtn = document.getElementById('shareEmailSendBtn');
    const emailStatus = document.getElementById('shareEmailStatus');

    if (emailSendBtn) {
      emailSendBtn.addEventListener('click', function() {
        const recipient = emailInput.value.trim();
        if (!recipient) {
          emailStatus.textContent = 'Enter an email address first.';
          emailStatus.className = 'text-xs mt-1 text-red-500';
          return;
        }

        emailSendBtn.disabled = true;
        const originalLabel = emailSendBtn.textContent;
        emailSendBtn.textContent = '...';
        emailStatus.textContent = '';

        fetch(shareBtn.dataset.emailUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify({ recipient_email: recipient }),
        })
          .then(function(res) {
            return res.json().then(function(data) { return { ok: res.ok, data: data }; });
          })
          .then(function(result) {
            if (result.ok) {
              emailStatus.textContent = 'Sent to ' + recipient + '!';
              emailStatus.className = 'text-xs mt-1 text-green-600';
              emailInput.value = '';
            } else {
              emailStatus.textContent = result.data.error || 'Could not send email.';
              emailStatus.className = 'text-xs mt-1 text-red-500';
            }
          })
          .catch(function() {
            emailStatus.textContent = 'Network error, try again.';
            emailStatus.className = 'text-xs mt-1 text-red-500';
          })
          .finally(function() {
            emailSendBtn.disabled = false;
            emailSendBtn.textContent = originalLabel;
          });
      });

      emailInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          emailSendBtn.click();
        }
      });

      // don't let the click-outside handler close the menu while typing
      emailInput.addEventListener('click', function(e) { e.stopPropagation(); });
    }
  }
});