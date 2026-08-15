# librera.app

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
assets/img/screenshots/     app screenshots — not yet supplied
assets/img/icons/           per-app icons — not yet supplied
```

No framework, no bundler, no dependencies. Open `index.html` or run any static
server; GitHub Pages serves the repo root as-is.

```bash
python3 -m http.server 4173
```

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

Every screenshot and app-icon slot ships as a neutral empty panel. Each one has the
markup to enable it sitting in a comment directly above:

```html
<div class="shot">
  <!-- add the image: <img src="assets/img/screenshots/reader.png" alt="Librera Reader screenshot" loading="lazy"> -->
  <div class="shot__placeholder" aria-hidden="true"></div>
</div>
```

Drop the file at that path and uncomment the line. The placeholder removes itself as
soon as the image loads, so nothing else needs changing. Slots, with their expected paths:

| Slot | Path | Shape |
|---|---|---|
| Hero | `assets/img/screenshots/hero.png` | wide, ~880×420 |
| Librera Reader | `assets/img/screenshots/reader.png` | 16:10 |
| Screenshot Helper | `assets/img/screenshots/screenshot-helper.png` | 16:10 |
| Sound Icon | `assets/img/screenshots/sound-icon.png` | 16:10 |
| App four / five | `assets/img/screenshots/app-{four,five}.png` | 16:10 |
| App icons | `assets/img/icons/{screenshot-helper,sound-icon,app-four,app-five}.png` | square |

Librera Reader already uses `librera-mark.png` as its icon, per the design.

### Links

Every outbound link is `href="#"` in the design, so they are `href="#"` here too, each
tagged with a `data-todo` attribute naming what belongs there. Find them with:

```bash
grep -n 'data-todo' index.html
```

`google-play-url`, `apk-url`, `web-app-url`, `help-url`, `issues-url`, `contact-url`,
`privacy-policy-url`, `terms-url`, `licences-url`. The Play Store and APK links repeat
per app, so replace them section by section rather than with a blanket find-and-replace.

The "Two more apps" cards are also placeholder copy — the design has no names for
apps four and five yet.

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
