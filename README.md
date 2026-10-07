# Librera Applications

**librera.app**

---

## LibreraX

*Reading*

It opens EPUB, MOBI, AZW3, FB2, PDF, CBZ, TXT and Markdown — reflowable books laid out by foliate-js, PDF pages by PDFium — and keeps a library of the folders you point it at, with covers, shelves, tags and search. Reading themes are your own list: added, recoloured, reordered and edited over a live page, with the contrast of ink against paper shown while you work. Highlights and bookmarks stay with the book; edited titles, authors and covers are written into the file itself. It reads aloud through a media session the lock screen and headset drive, puts the book you are on into a home-screen widget, and carries the same controls to a paired Wear OS watch.

- [Google Play](https://play.google.com/store/apps/details?id=com.librerax)
- [iOS (TestFlight)](https://testflight.apple.com/join/XVU24NY9)

## Librera Reader

*Reading*

Highly customizable and feature-rich application for reading books in PDF, EPUB, MOBI, DjVu, FB2, TXT, RTF, AZW, AZW3, HTML, CBZ, CBR formats on Android devices. With its intuitive, yet powerful, interface, Librera makes ebook reading a veritable pleasure. It even features a unique auto-scrolling, hands-free Musician’s mode. As of today, it can boast more than 10 million downloads to devices running all flavors of Android OS.

- [Google Play (Pro)](https://play.google.com/store/apps/details?id=com.foobnix.pro.pdf.reader)
- [Google Play](https://play.google.com/store/apps/details?id=com.foobnix.pdf.reader)
- [Direct APK](https://github.com/foobnix/LibreraReader)
- [F-Droid](https://f-droid.org/en/packages/com.foobnix.pro.pdf.reader/)
- [Web](https://librera.mobi/)

## Librera1 Reader

*Reading*

A reader for the books you already have. Open an EPUB, PDF, FB2, MOBI or CBZ, and read it on whichever device is to hand — the page you stopped on, the passages you marked and the places you named follow you between them.

- [Web](https://librera1.com/)
- [Direct APK](https://github.com/foobnix/librera.app/releases/tag/Download)
- [Direct DMG](https://github.com/foobnix/librera.app/releases/tag/Download)
- [Chrome](https://chromewebstore.google.com/detail/dplmfhcjlbkejkdalnkmklpghklcjahg)
- [VS Code](https://marketplace.visualstudio.com/items?itemName=librera.librera-reader)
- [Google Play](https://play.google.com/store/apps/details?id=com.foobnix.pdf.reader)

## Sound Icon

*Utilities*

Volume, one tap away. Media, ring, alarm and call sliders on a single panel that opens from the status bar, with saved profiles for the places you switch between.

- [Web](https://soundicon.app/)
- [Direct DMG](https://github.com/foobnix/librera.app/releases/tag/Download)

## Menu Reminder

*Utilities*

Your to-dos, one click away in the menu bar. Add a reminder with an optional due date and the list groups itself by day — today, tomorrow, overdue in red. When something comes due, the bell lights up and a notification arrives; check it off and it's done.

- [Direct DMG](https://github.com/foobnix/librera.app/releases/tag/Download)

## Menu Screenshot

*Utilities*

Capture perfectly sized screenshots and drag them anywhere. Snap the perfect size. Drag it to any app. Custom screenshots, ready to drag and drop.

- [Direct DMG](https://github.com/foobnix/librera.app/releases/tag/Download)

## LibreraCommander

*Utilities*

A dual-pane file manager for the Mac. Two Finder-style panels with your Finder favourites, a built-in terminal with four shells, and an info panel for drives, memory and battery, Quick Look and text previews, an editor, file and folder comparison and a media player.

Install with Homebrew:

```sh
brew install foobnix/tap/libreracommander
```

Update:

```sh
brew upgrade libreracommander
```

- [Direct DMG](https://github.com/foobnix/LibreraCommander-releases/releases/)


---

## How the site is built

GitHub Pages builds the site with Jekyll. Every page shares one header and footer.

| Where | What |
| --- | --- |
| `_data/apps.yml` | The app list. It drives the home page rows, the navbar, the footer and each app page's header (icon, platforms, summary, buttons, screenshots). |
| `_layouts/default.html` | Every page: `<head>`, navbar, footer, `assets/js/site.js`. |
| `_layouts/app.html` | An app's own page (`/librerax/`, `/sound-icon/`, …): the app header, then the page's Markdown. |
| `_layouts/doc.html` | Documentation pages under an app (Librera Reader FAQ, release notes, privacy policies). |
| `_includes/` | The shared pieces: `head`, `navbar`, `footer`, `app-row` (a home page row), `gallery` (a screenshot gallery). |
| `<app>/index.md` | Each app's full description and screenshot galleries. Images are in `assets/img/apps/<app>/`. |
| `librera-reader/` | Librera Reader's pages. `faq/`, `what-is-new/`, `privacy-policy/` and `contributors/` are imported from the LibreraReader repository. |

To add an app, add an entry to `_data/apps.yml` and create `<id>/index.md` with `layout: app` and `app: <id>`.

**Re-importing the Librera Reader docs** after they change in `LibreraReader/docs`:

```sh
scripts/import-librera-reader-docs.py ../LibreraReader/docs
```

It rewrites links to their new place and converts images to WebP (needs `cwebp`: `brew install webp`). Edit the docs in LibreraReader, not the copies here. The FAQ index (`librera-reader/faq/index.html`) is written by hand and lists the imported topics automatically.

**Preview locally:** `./run.sh` (needs `gem install jekyll`), then open http://127.0.0.1:4000/.

---

Copyright 2026 Ivan Ivanenko. All rights reserved.
