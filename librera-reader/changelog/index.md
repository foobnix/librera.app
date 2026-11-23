---
layout: "doc"
app: "librera-reader"
title: "Changelog"
description: "What changed in each Librera Reader release."
---
# Changelog

### [10.1.16] Open on page 1, PDF search fix, TTS to MP3

**Opening books**

* New option in Preferences › Advanced Settings: open books on page 1 instead of where you left off (also in Preferences › General, and for books opened in LibreraX)

**Text-to-speech**

* Record the book read aloud to an MP3 file

**PDF**

* Search highlights the found word itself: with the PDFium engine the box was one word off on pages with math symbols
* Text can be selected and searched on a page the book opened on zoomed in

**Reading**

* In day mode the page colour is used for the whole page, also where the book sets its own background
* Pages with only a picture (an EPUB cover) are no longer drawn blank in the HTML engine

**About**

* Changelog link at the bottom of the preferences, to this page in the browser

### [10.1.14] Internet radio, music and radio in the TTS panel

* Internet radio: play M3U playlists, with a built-in list of recommended stations
* Music and radio buttons in the TTS panel, with seek buttons for streams
* Panels and buttons adjusted for landscape

### [10.1.10] CHM and LIT books, MuPDF 1.28.6, self test

* CHM and LIT books open, converted to EPUB
* MuPDF engine upgraded to 1.28.6
* Self test of the reading engines on your own books
* Fixed hyphenation, fonts and the e-ink theme
* Show or hide the Musician's mode button
* Fixed double tap and paged mode

### [10.0.35] Draw shapes on PDF, TTS reading icon

* Draw shapes on PDF pages
* An animated sound icon shows while TTS is reading
* Fixed splitting pages and right-to-left reading
* Interface updates and fixes

### [10.0.31] Page count for reflowable books, draw in paged mode

* Page count shown for EPUB and other reflowable books (estimated, marked ≈)
* Draw on PDF pages in paged mode
* TIFF images and books open without MuPDF
* Fixed the TTS buttons, text selection and the library sort order

### [10.0.22] TTS highlight in the HTML engine, JS build

* TTS highlights the text being read with the HTML engine
* JS build: reads without MuPDF, with the HTML engine and PDFium
* Fixed Google Drive sync, SVG images and FB2 images
* Fonts included by default

### [10.0.19] Comics without unpacking, home screen widget

* Comic books (CBZ, CBR) open from the archive without unpacking it first
* Home screen widget and shortcut for a book
* TTS buttons at the bottom of the reader
* Send a book with its bookmarks and progress to LibreraX; a book that crashed can be opened in LibreraX
* Fixed hyphenation, the dictionary and bookmark panels

### [10.0.0] foliate-js and PDFium engines, SAF folders in the library, highlights in EPUB

* Reflowable books now render in a WebView with foliate-js, and PDFs with PDFium
* Icons are shown in the SAF folder browser
* SAF folders can be added to the library
* Underline and highlight in EPUB
* Open a book in LibreraX, our new modern reader for Android and iOS

### [9.6.39] MuPDF 1.28.5, library sort

* MuPDF engine upgraded to 1.28.5
* Pull to refresh in the library can be turned off
* Full published date shown and used for sorting
* The library shows its current sort

### [9.6.25] MuPDF 1.28.4, bookmarks to LibreraX

* MuPDF engine upgraded to 1.28.4
* Bookmarks are sent to LibreraX
* Cover corner radius option

### [9.6.17] Open with LibreraX, faster footnotes

* Open a book with LibreraX
* Faster footnotes (2.4x)
* BBCode formatting is off by default

### [9.6.7] New design

* New design: floating rounded tabs, round buttons, rounded dialogs and menus, new theme colours.
* Redesigned settings, book info and TTS dialogs.
* Library button and one-tap Vertical/Paged switch in the reader.
* BBCode formatting in books.
* Bookmarks and reading position stay on the right page after font changes and sync.
* Favourites use a heart.

### [9.5.7] Android Auto, faster Google Drive sync, MuPDF 1.28.3

**Android Auto**

* Librera now appears as a media app in Android Auto
* Browse recent books in the car, with covers, titles and authors
* Selecting a book resumes it at its saved position
* Playback controls work from the car, the lock screen and Bluetooth

**Text-to-speech**

* Uses Android's standard media notification, with cover art, a progress bar and lock screen controls
* Fixed no speech when the system default engine points at an uninstalled package
* Fixed the notification disappearing, or staying stuck on "please wait", after a long time in the background
* Fixed audio focus not being released on pause, which left other apps muted
* Fixed a crash when requesting the notification permission from the TTS controls

**Reading**

* Upgraded the MuPDF engine to 1.28.3 (Librera patches ported from 1.23.7)
* Text selection now works while "crop white space" is enabled, in both book and scroll modes
* Reading direction (RTL) can now be set in scroll mode, not only in book mode
* Annotating is allowed while crop is enabled
* Fixed reflow when toggling "crop white space"
* Book mode: the clock/battery ticker stops when the status bar is hidden
* New "Show progress slider" setting to toggle the seek bar row
* Improved jump history and "Back" arrow visibility when using the slider
* More consistent brightness values when adjusting by scroll
* Fixes for formatted .txt files

**Google Drive sync**

* Much faster: smaller listing requests, parallel downloads and a change check that skips work when nothing changed
* Deleting a book now propagates: it no longer comes back from another device
* Fixed downloads failing into folders that did not exist locally
* Fixed a sync that could stop early on files without a size
* Temporary download files are no longer uploaded to Drive

### [9.4.21] Text replacement and color settings

* Fixed text replacement for multiple words
* Updated the UI for changing text and background colors
* Added an alert for permanent file deletion
* Clicking on File Information metadata now navigates to the library
* Added the "iw" translation and fixed other translations
* Fixed the grid view widget
* Fixed the eye reset timer

### [9.4.8] All-storage access is optional

* All-storage access is optional
* Apps can use the system file manager to open individual files
* Fixed choose profile

### [9.3.75]

* Fixed contrast and brightness
* Advanced option to enable contrast and brightness for all reading modes
* Fixed Chinese language
* Fixed search in many PDF and EPUB books

### [9.3.63]

* Improvements
* Fixes

### [9.3.55]

* Fixes
* Librera for macOS, supports PDF, EPUB, FB2, CBZ, CBR (beta.librera.mobi for downloads)

Older releases: https://github.com/foobnix/LibreraReader/releases
