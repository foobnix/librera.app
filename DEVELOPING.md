# Developing librera.app

Build, run and deploy notes. For what the site actually says, see [README.md](README.md).

Static marketing site for Librera, served from GitHub Pages at **librera.app**.

Implementation of the `Librera Site.dc.html` design from the Claude Design project
`f391d4d9-f1f0-45b0-9a15-41aafc5696fc`, built on the **librera-design-system-c87c098d**
tokens.

## Layout

```
index.html                  the whole site — one page, no build step
CNAME                       librera.app
.nojekyll                   serve _-prefixed paths and skip Jekyll processing
robots.txt  sitemap.xml
assets/css/tokens/*.css     design-system tokens, copied verbatim
assets/css/site.css         page composition + DS components as static CSS
assets/img/librera-mark.png the brand mark (512×512, from the design project)
assets/img/screenshots/     app screenshots
assets/img/icons/           per-app icons
```

No framework, no bundler, no dependencies. GitHub Pages serves the repo root as-is.

## Running it locally

```bash
./run.sh
```

Serves the site at <http://127.0.0.1:4000>. Options:

| | |
|---|---|
| `./run.sh 8080` | use a different port (or `PORT=8080 ./run.sh`) |
| `./run.sh --open` | open a browser once the server is up |
| `./run.sh --static` | force the static server, never Jekyll |
| `./run.sh --help` | usage |

Because this repo ships `.nojekyll` and has no `_config.yml`, there is no Jekyll
build to run — the static server is exactly what GitHub Pages does with these
files. If a `_config.yml` is ever added, `run.sh` detects it and switches to
`bundle exec jekyll serve --livereload` (or plain `jekyll serve`) on its own, so
the local preview keeps matching production. It falls back to the static server
with a warning if Jekyll turns out not to be installed.

The script binds to loopback only, refuses to start on a port already in use, and
uses `python3`, then `ruby`, then `npx serve`, whichever it finds first.

## Deploying

1. Push this repo to GitHub.
2. Settings → Pages → Source: **Deploy from a branch**, branch `main`, folder `/ (root)`.
3. Settings → Pages → Custom domain: `librera.app` (the `CNAME` file already sets this).
4. At your DNS provider, point the apex `librera.app` at GitHub Pages:
   `A` records to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   (and/or `AAAA` to the matching `2606:50c0:800::153` … `803::153`).
   Add a `CNAME` for `www` → `<user>.github.io` if you want the www host too.
5. Tick **Enforce HTTPS** once the certificate is issued.

## Still to fill in

Two things are deliberately unfinished, both because the source design leaves them open.

### Images

The three shipped apps now have their real icon and screenshot:

| Slot | Icon | Screenshot | Screenshot size |
|---|---|---|---|
| Librera Reader | `librera-mark.png` | `screenshots/librera1.png` | 2296×1812 |
| Screenshot Helper | `icons/screenshot.png` | `screenshots/screenshot.png` | 698×804 |
| Sound Icon | `icons/soundicon.png` | `screenshots/soundicon.png` | 666×1298 |

`icons/librera1.png` is the same artwork as `librera-mark.png` at 128px rather than
512px, so the Reader keeps the mark — it stays sharp in the 56px tile on retina.

Any slot with no file still ships as a neutral empty panel, with the markup to
enable it in a comment directly above:

```html
<div class="shot">
  <!-- add the image: <img src="assets/img/screenshots/thing.png" alt="…" loading="lazy"> -->
  <div class="shot__placeholder" aria-hidden="true"></div>
</div>
```

Drop the file at that path and uncomment the line; the placeholder removes itself
once the image loads.

**Fit.** The design's frames are 16:10 landscape, but app screenshots are usually
portrait. Cropping them to fill would have thrown away 21%, 46% and 68% of the
three above, so the script at the foot of `index.html` compares each image's aspect
ratio to its frame and adds `.shot--contain` when they differ by more than 12% —
the picture is letterboxed on the dark panel instead of cropped. Shots that are
already close to 16:10 still fill the frame edge to edge. New screenshots get the
right treatment automatically; no markup change needed.

### Links

Every outbound link is `href="#"` in the design, so they are `href="#"` here too, each
tagged with a `data-todo` attribute naming what belongs there. Find them with:

```bash
grep -n 'data-todo' index.html
```

`google-play-url`, `apk-url`, `web-app-url`, `help-url`, `issues-url`, `contact-url`,
`privacy-policy-url`, `terms-url`, `licences-url`. The Play Store and APK links repeat
per app, so replace them section by section rather than with a blanket find-and-replace.


## Notes on the implementation

- The design file is a Claude Design component (`x-dc`) that renders DS React
  components at runtime. This site is plain HTML: `NavBar`, `Button` and `Footer` are
  transcribed into static CSS classes in `site.css`, matching the bundle's computed
  styles (48px blurred sticky bar; pill buttons at 32/40/52px; sunken footer with link
  columns and a legal row).
- The DS `Icon` component fetches Lucide glyphs from a CDN at runtime. The two icons
  actually used (`chevron-right`, `download`) are inlined as SVG instead — no
  third-party request, no flash of missing icon.
- The token files under `assets/css/tokens/` are byte-for-byte copies of the design
  system's. Re-copy them if the design system changes rather than hand-editing.
- The hero and its section carry `data-theme="dark"`, which is what flips `--accent`
  from `--blue-600` to `--blue-500` for the hero's primary button — that colour
  difference is intentional, not a slip.
- `prefers-reduced-motion` disables smooth scrolling and all transitions.
