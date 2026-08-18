# Librera — Applications

**librera.app**

---

## Librera Reader for Android

*Reading*

Highly customizable and feature-rich application for reading books in PDF, EPUB, MOBI, DjVu, FB2, TXT, RTF, AZW, AZW3, HTML, CBZ, CBR formats on Android devices. With its intuitive, yet powerful, interface, Librera makes ebook reading a veritable pleasure. It even features a unique auto-scrolling, hands-free Musician’s mode. As of today, it can boast more than 10 million downloads to devices running all flavors of Android OS.

- [Google Play (Pro)](https://play.google.com/store/apps/details?id=com.foobnix.pro.pdf.reader)
- [Google Play](https://play.google.com/store/apps/details?id=com.foobnix.pdf.reader)
- [Direct APK](https://github.com/foobnix/LibreraReader)
- [F-Droid](https://f-droid.org/en/packages/com.foobnix.pro.pdf.reader/)

## Librera1 Reader

*Reading*

A reader for the books you already have. Open an EPUB, PDF, FB2, MOBI or CBZ, and read it on whichever device is to hand — the page you stopped on, the passages you marked and the places you named follow you between them.

- [Web app](https://librera1.com/)
- [Chrome](https://chromewebstore.google.com/detail/librera1-%E2%80%94-read-your-own/dplmfhcjlbkejkdalnkmklpghklcjahg)
- [VS Code](https://marketplace.visualstudio.com/items?itemName=librera.librera-reader)
- [Google Play](https://play.google.com/store/apps/details?id=com.foobnix.pdf.reader)

## Sound Icon

*Utilities*

Volume, one tap away. Media, ring, alarm and call sliders on a single panel that opens from the status bar, with saved profiles for the places you switch between.

- [Web app](https://soundicon.app/)
- macOS — link to come

## Screenshot Helper

*Utilities*

Capture, mark up, send. Crop the frame, blur what shouldn't be in it and share without opening a gallery. The capture button sits in a floating bubble that stays out of the shot.

- macOS — link to come

---

**Apps** — Librera Reader for Android · Librera1 Reader · Sound Icon · Screenshot Helper
**Download** — Google Play · F-Droid · Direct APK · Librera1 on the web · Sound Icon on the web · Chrome extension · VS Code extension
**Support** — librera.reader@gmail.com

Copyright 2026 Ivan Ivanenko. All rights reserved.

---

## Developing

Static site for **librera.app**, served from GitHub Pages. Implements the
`Librera Site.dc.html` design on the `librera-design-system-c87c098d` tokens.
No framework, no bundler, no build step — Pages serves the repo root as-is.

```
index.html                  the whole site
CNAME                       librera.app
.nojekyll                   skip Jekyll processing
assets/css/tokens/*.css     design-system tokens, copied verbatim
assets/css/site.css         page composition + DS components as static CSS
assets/img/                 brand mark, per-app icons, screenshots
```

Run it locally:

```bash
./run.sh
```

Serves on <http://127.0.0.1:4000>. `./run.sh 8080` for another port, `--open` to
open a browser, `--static` to force the static server, `--help` for usage. It
binds loopback only and refuses a port already in use.

Screenshots are shown as they are — no window frame, native aspect ratio, nothing
cropped. `.shot img` only caps the size (`max-width: 100%`,
`max-height: min(620px, 78vh)`), so portrait phone shots and wide desktop ones
both fit at every width. A slot with no image falls back to a neutral panel; the
script at the foot of `index.html` removes the placeholder once an image loads,
and removes the `<img>` instead if the file is missing.

Links still to fill in are tagged in the markup:

```bash
grep -n 'data-todo' index.html
```

## Deploying

1. Settings → Pages → Source: **Deploy from a branch**, branch `main`, folder `/ (root)`.
2. Settings → Pages → Custom domain: `librera.app` (the `CNAME` file already sets this).
3. At the DNS provider, point the apex `librera.app` at GitHub Pages —
   `A` records to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`,
   `185.199.111.153` (and/or `AAAA` to `2606:50c0:800::153` … `803::153`).
   Add a `CNAME` for `www` → `foobnix.github.io` if the www host is wanted too.
4. Tick **Enforce HTTPS** once the certificate is issued.
