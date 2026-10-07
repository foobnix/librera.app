/* librera.app — page script, shared by every page. */

/* Screenshot / icon slots.
   Each slot holds an <img> and a labelled placeholder. Drop a real file at the
   img's src and it takes over; while the file is missing the placeholder shows
   instead. The mark has transparent corners, so the placeholder is removed on
   a successful load rather than just being painted over. */
(function () {
  function settle(img) {
    var slot = img.parentElement;
    var ph = slot.querySelector('.shot__placeholder, .app-icon__placeholder');
    if (!img.naturalWidth) { img.remove(); return; }
    if (ph) ph.remove();
  }

  var imgs = document.querySelectorAll('.shot img, .app-icon img');
  for (var i = 0; i < imgs.length; i++) {
    (function (img) {
      if (img.complete) { settle(img); return; }
      img.addEventListener('load', function () { settle(img); });
      img.addEventListener('error', function () { settle(img); });
    })(imgs[i]);
  }
})();

/* Lightbox.
   Clicking a screenshot opens it in a modal <dialog>, as large as the window
   allows but never beyond its natural size. Esc, the close button or a click
   anywhere closes it. Screenshots are focusable, so Enter / Space open it too.
   Covers the home page and app header shots, galleries, and the images inside
   documentation pages (except ones that are already links). */
(function () {
  var shots = document.querySelectorAll('.shot img, .gallery img, .prose img');
  if (!shots.length || typeof HTMLDialogElement === 'undefined') return;

  var dialog = document.createElement('dialog');
  dialog.className = 'lightbox';
  dialog.setAttribute('aria-label', 'Screenshot');
  dialog.tabIndex = -1;
  dialog.innerHTML =
    '<button class="lightbox__close" type="button" aria-label="Close">' +
      '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">' +
        '<path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>' +
      '</svg>' +
    '</button>' +
    '<img class="lightbox__img" alt="">';
  document.body.appendChild(dialog);
  var big = dialog.querySelector('.lightbox__img');

  function open(img) {
    big.src = img.currentSrc || img.src;
    big.alt = img.alt;
    big.style.maxWidth = img.naturalWidth ? 'min(100%, ' + img.naturalWidth + 'px)' : '';
    dialog.showModal();
    /* showModal() focuses the close button, which draws its focus ring on a
       mouse click too. Focus the dialog instead; Tab still reaches the button. */
    dialog.focus();
  }

  dialog.addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('close', function () { big.removeAttribute('src'); });

  for (var i = 0; i < shots.length; i++) {
    (function (img) {
      if (img.closest('a')) return;
      img.tabIndex = 0;
      img.setAttribute('role', 'button');
      img.setAttribute('aria-label', 'Enlarge' + (img.alt ? ': ' + img.alt : ' image'));
      img.addEventListener('click', function () { open(img); });
      img.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(img); }
      });
    })(shots[i]);
  }
})();

/* Copy commands.
   Every command / code block gets a copy icon: the home page install box
   (.install__code), code blocks in page text (.prose pre) and the app header's
   install line, whose button is already in the markup. Clicking the icon, or
   the command itself, copies it; a tick shows for a moment. A click that ends
   a text selection is left alone, so the command can still be selected by
   hand. */
(function () {
  var ICON = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1"/></svg>';
  var TICK = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';

  /* Where the async clipboard is missing or refused (older browsers,
     embedded views), copy through a hidden textarea instead. */
  function fallback(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    ta.remove();
    return ok;
  }

  function copy(text, done) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, function () { if (fallback(text)) done(); });
    } else if (fallback(text)) {
      done();
    }
  }

  function flash(btn) {
    btn.innerHTML = TICK;
    btn.classList.add('is-copied');
    btn.setAttribute('aria-label', 'Copied');
    clearTimeout(btn._copyTimer);
    btn._copyTimer = setTimeout(function () {
      btn.innerHTML = ICON;
      btn.classList.remove('is-copied');
      btn.setAttribute('aria-label', 'Copy');
    }, 1500);
  }

  /* Wrap each code block so the icon sits in its corner without scrolling
     away with a long line. */
  var blocks = document.querySelectorAll('.install__code, .prose pre');
  for (var i = 0; i < blocks.length; i++) {
    var pre = blocks[i];
    var wrap = document.createElement('div');
    wrap.className = 'copy-wrap';
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-btn';
    btn.setAttribute('aria-label', 'Copy');
    btn.setAttribute('data-copy', pre.textContent.replace(/\s+$/, ''));
    btn.innerHTML = ICON;
    wrap.appendChild(btn);
    pre.classList.add('is-copyable');
    pre.title = 'Click to copy';
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.copy-btn');
    if (!btn) {
      var code = e.target.closest('.is-copyable');
      if (!code) return;
      var sel = window.getSelection && window.getSelection().toString();
      if (sel) return;
      btn = code.parentNode.querySelector('.copy-btn');
      if (!btn) return;
    }
    copy(btn.getAttribute('data-copy'), function () { flash(btn); });
  });
})();
