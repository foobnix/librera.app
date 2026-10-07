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
