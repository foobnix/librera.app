#!/usr/bin/env python3
"""Import the Librera Reader documentation into this site.

The docs are written in the LibreraReader repository (docs/, the old
librera.mobi Jekyll site). This copies them under librera-reader/ here, in this
site's layout, so they can be re-synced whenever they change:

    scripts/import-librera-reader-docs.py [path/to/LibreraReader/docs]

The default source is ../LibreraReader/docs next to this repository.

What it does
  faq/<topic>/            -> librera-reader/faq/<topic>/
  what-is-new/ (+ 8.x/)   -> librera-reader/what-is-new/
  PrivacyPolicy/*.md      -> librera-reader/privacy-policy/<app>/
  contributors.md         -> librera-reader/contributors/

  * Front matter is replaced: the page title is taken from its first heading,
    and the layout/section come from _config.yml defaults.
  * Links into the old site (/faq/..., /what-is-new/..., /PrivacyPolicy/...)
    are rewritten to their new place.
  * PNG and JPEG images are converted to WebP (cwebp, if installed; otherwise
    they are copied as they are) and every reference is updated. Images are
    marked loading="lazy".

The FAQ index is not copied: librera-reader/faq/index.html lists the topics
from the imported pages themselves. Everything under the four target folders
except that index is generated — edit the source, not the copy.
"""

import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "librera-reader")
SRC = os.path.abspath(sys.argv[1] if len(sys.argv) > 1
                      else os.path.join(ROOT, "..", "LibreraReader", "docs"))

CWEBP = shutil.which("cwebp")
RASTER = re.compile(r"\.(png|jpe?g)$", re.I)

# Old librera.mobi paths whose content now lives somewhere else.
MANUAL = {
    "/manual/Rapid-Serial-Visual-Presentation/": "/librera-reader/faq/rsvp-speed-reading-rapid-serial-visual-presentation/",
    "/manual/Open-Folder-With-Images-As-A-Book/": "/librera-reader/faq/open-folder-with-images-as-a-book/",
}


def webp_name(name):
    return RASTER.sub(".webp", name) if CWEBP else name


def copy_image(src, dst_dir):
    """Copy one image into dst_dir, as WebP when possible. Skips up-to-date files."""
    name = os.path.basename(src)
    out = os.path.join(dst_dir, webp_name(name) if RASTER.search(name) else name)
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src):
        return
    if CWEBP and RASTER.search(name):
        subprocess.run([CWEBP, "-quiet", "-q", "82", "-m", "5", src, "-o", out], check=True)
    else:
        shutil.copy2(src, out)


def read_md(path):
    text = open(path, encoding="utf-8").read()
    if text.startswith("---"):
        end = text.find("\n---", 3)
        text = text[end + 4:] if end != -1 else text
    return text.lstrip("\n")


def plain(md):
    """A heading's text without Markdown emphasis or links."""
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"[*_`]", "", md)
    return re.sub(r"\s+", " ", md).strip()


def rewrite_link(url):
    if url.startswith(("http://", "https://", "mailto:", "#")):
        if "LibreraReader/blob/master/LIBRERAX.md" in url:
            return "/librerax/"
        return url
    for old, new in MANUAL.items():
        if url.startswith(old):
            return new + webp_name(url[len(old):])
    if url.startswith("/librerax/") and RASTER.search(url):
        return "/assets/img/apps/librerax/" + webp_name(os.path.basename(url))
    if url.startswith("/faq") or url.startswith("/what-is-new"):
        url = "/librera-reader" + url
        if not os.path.splitext(url)[1] and not url.endswith("/"):
            url += "/"
        return url
    if url.startswith("/PrivacyPolicy"):
        rest = url[len("/PrivacyPolicy"):].strip("/")
        return "/librera-reader/privacy-policy/" + (rest + "/" if rest else "")
    if url in ("/", "/index.html"):
        return "/librera-reader/"
    if url.rstrip("/") == "/download":
        return "/librera-reader/download/"
    if url.rstrip("/") in ("/online-book-reader", "/epub-reader"):
        return "https://librera.mobi" + url
    if not url.startswith("/") and RASTER.search(url):
        return webp_name(url)
    return url


FENCE = re.compile(r"^```.*?^```[^\n]*$", re.M | re.S)


def outside_code(fn, text):
    """Apply fn to the text between fenced code blocks, leaving examples alone."""
    out, pos = [], 0
    for m in FENCE.finditer(text):
        out += [fn(text[pos:m.start()]), m.group(0)]
        pos = m.end()
    return "".join(out + [fn(text[pos:])])


def convert(text):
    return outside_code(convert_prose, text)


def convert_prose(text):
    # Markdown links and images: [text](url) / ![alt](url)
    def md_link(m):
        bang, label, url = m.group(1), m.group(2), m.group(3)
        new = rewrite_link(url)
        out = f"{bang}[{label}]({new})"
        if bang and not text_has_ial(m.string, m.end()):
            out += '{: loading="lazy"}'
        return out

    text = re.sub(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)", md_link, text)

    # Raw <img src="...">
    def img_tag(m):
        tag = m.group(0)
        tag = re.sub(r'src="([^"]+)"', lambda s: f'src="{rewrite_link(s.group(1))}"', tag)
        if "loading=" not in tag:
            tag = tag.replace("<img ", '<img loading="lazy" ', 1)
        return tag

    text = re.sub(r"<img\b[^>]*>", img_tag, text)
    # Raw <a href="..."> into the old site
    text = re.sub(r'(<a\b[^>]*href=")([^"]+)(")',
                  lambda m: m.group(1) + rewrite_link(m.group(2)) + m.group(3), text)
    return text


def text_has_ial(s, pos):
    return s.startswith("{:", pos)


def write_page(path, front, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in front.items()] + ["---", ""]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + body.rstrip() + "\n")


def first_heading(body, fallback):
    m = re.search(r"^#{1,2}\s+(.+?)\s*#*\s*$", body, re.M)
    return plain(m.group(1)) if m else fallback


def first_image(body):
    m = re.search(r"!\[[^\]]*\]\(([^)\s]+)\)|<img\b[^>]*src=\"([^\"]+)\"", body)
    return (m.group(1) or m.group(2)) if m else None


def import_dir(src_dir, dst_dir, front):
    """One folder holding index.md and its images."""
    os.makedirs(dst_dir, exist_ok=True)
    for name in sorted(os.listdir(src_dir)):
        p = os.path.join(src_dir, name)
        if os.path.isfile(p) and not name.startswith(".") and name != "index.md":
            if re.search(r"\.(png|jpe?g|gif|webp|svg)$", name, re.I):
                copy_image(p, dst_dir)
    body = convert(read_md(os.path.join(src_dir, "index.md")))
    front = dict(front)
    front.setdefault("title", first_heading(body, os.path.basename(src_dir)))
    thumb = first_image(FENCE.sub("", body))
    if thumb and not thumb.startswith(("http", "/")) and os.path.exists(os.path.join(dst_dir, thumb)):
        front["thumb"] = thumb
    write_page(os.path.join(dst_dir, "index.md"), front, body)
    return front


def clean(path, keep=()):
    if not os.path.isdir(path):
        return
    for name in os.listdir(path):
        if name in keep:
            continue
        p = os.path.join(path, name)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)


def main():
    if not os.path.isfile(os.path.join(SRC, "faq", "index.md")):
        sys.exit(f"Not a LibreraReader docs folder: {SRC}")
    if not CWEBP:
        print("cwebp not found: images are copied unconverted (brew install webp).", file=sys.stderr)

    # FAQ ----------------------------------------------------------------
    faq_src, faq_dst = os.path.join(SRC, "faq"), os.path.join(DEST, "faq")
    os.makedirs(faq_dst, exist_ok=True)
    topics = sorted(d for d in os.listdir(faq_src)
                    if os.path.isfile(os.path.join(faq_src, d, "index.md")))
    for name in os.listdir(faq_dst):  # drop topics removed upstream
        if os.path.isdir(os.path.join(faq_dst, name)) and name not in topics:
            shutil.rmtree(os.path.join(faq_dst, name))
    for t in topics:
        import_dir(os.path.join(faq_src, t), os.path.join(faq_dst, t), {"topic": True})
    print(f"faq: {len(topics)} topics")

    # What is new ---------------------------------------------------------
    win_src, win_dst = os.path.join(SRC, "what-is-new"), os.path.join(DEST, "what-is-new")
    clean(win_dst)
    versions = sorted((d for d in os.listdir(win_src)
                       if os.path.isfile(os.path.join(win_src, d, "index.md"))),
                      key=lambda v: [int(x) for x in re.findall(r"\d+", v)], reverse=True)
    for v in versions:
        import_dir(os.path.join(win_src, v), os.path.join(win_dst, v), {
            "title": f"Librera {v}",
            "parent_url": "/librera-reader/what-is-new/",
            "parent_title": "What's new",
        })
    import_dir(win_src, win_dst, {
        "title": "What's new",
        "description": "Release notes for Librera Reader.",
    })
    # The old layout appended the list of older releases to every release page.
    index = os.path.join(win_dst, "index.md")
    older = "\n".join(f"* [Librera {v}](/librera-reader/what-is-new/{v}/)" for v in versions)
    with open(index, "a", encoding="utf-8") as f:
        f.write(f"\n## Older releases\n\n{older}\n")
    print(f"what-is-new: index + {len(versions)} releases")

    # Privacy policies ----------------------------------------------------
    pp_src, pp_dst = os.path.join(SRC, "PrivacyPolicy"), os.path.join(DEST, "privacy-policy")
    clean(pp_dst)
    # The index names each app: * [Librera PRO](/PrivacyPolicy/com.foobnix.pro.pdf.reader)
    names = dict((slug, label) for label, slug in re.findall(
        r"\[([^\]]+)\]\(/PrivacyPolicy/([^)/]+)\)", read_md(os.path.join(pp_src, "index.md"))))
    for name in sorted(os.listdir(pp_src)):
        if not name.endswith(".md"):
            continue
        body = convert(read_md(os.path.join(pp_src, name)))
        slug = name[:-3]
        out = os.path.join(pp_dst, "index.md") if slug == "index" else os.path.join(pp_dst, slug, "index.md")
        front = {"title": first_heading(body, "Privacy Policy")}
        if slug != "index":
            front["parent_url"] = "/librera-reader/privacy-policy/"
            front["parent_title"] = "Privacy"
            front["title"] = f"{front['title']} — {names.get(slug, slug)}"
        write_page(out, front, body)
    print("privacy-policy: done")

    # Contributors --------------------------------------------------------
    body = convert(read_md(os.path.join(SRC, "contributors.md")))
    write_page(os.path.join(DEST, "contributors", "index.md"), {
        "layout": "doc", "app": "librera-reader",
        "title": "Contributors",
        "description": "People who help develop Librera Reader.",
        "lang": "uk",
    }, body)
    print("contributors: done")


if __name__ == "__main__":
    main()
