#!/usr/bin/env bash
#
# run.sh — serve librera.app locally.
#
# The site is plain static HTML and ships a .nojekyll file, so GitHub Pages
# serves it as-is with no Jekyll build. This script mirrors that: it serves the
# repo root over HTTP. If a Jekyll site is ever added here (a _config.yml plus
# jekyll on PATH or in the bundle), it switches to `jekyll serve` automatically
# so the local preview keeps matching what Pages would do.
#
#   ./run.sh                 serve on http://127.0.0.1:4000
#   ./run.sh 8080            serve on a different port
#   ./run.sh --open          serve and open a browser
#   ./run.sh --static        force the static server, never Jekyll
#   PORT=8080 ./run.sh       port via environment
#
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PORT="${PORT:-4000}"
HOST="127.0.0.1"
OPEN=0
FORCE_STATIC=0

usage() {
  sed -n '3,15p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 0
}

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help)   usage ;;
    -o|--open)   OPEN=1 ;;
    -s|--static) FORCE_STATIC=1 ;;
    ''|*[!0-9]*) printf 'run.sh: unknown option %s (try --help)\n' "$1" >&2; exit 2 ;;
    *)           PORT="$1" ;;
  esac
  shift
done

if [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
  printf 'run.sh: port %s out of range\n' "$PORT" >&2
  exit 2
fi

# Refuse to start on a busy port rather than failing halfway with a stack trace.
if command -v lsof >/dev/null 2>&1 && lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  printf 'run.sh: port %s is already in use. Pick another: ./run.sh %s\n' "$PORT" "$((PORT + 1))" >&2
  exit 1
fi

open_browser() {
  [ "$OPEN" -eq 1 ] || return 0
  local url="http://$HOST:$PORT/"
  ( sleep 1
    if   command -v open     >/dev/null 2>&1; then open "$url"
    elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$url"
    fi ) >/dev/null 2>&1 &
}

banner() {
  printf '\n  Librera — %s\n  http://%s:%s/\n\n  Ctrl-C to stop.\n\n' "$1" "$HOST" "$PORT"
}

cd "$ROOT"

# ---- Jekyll, only if there is genuinely a Jekyll site to build ---------------
if [ "$FORCE_STATIC" -eq 0 ] && [ -f "$ROOT/_config.yml" ]; then
  if [ -f "$ROOT/Gemfile" ] && command -v bundle >/dev/null 2>&1 \
     && bundle exec jekyll --version >/dev/null 2>&1; then
    banner "jekyll (bundle)"
    open_browser
    exec bundle exec jekyll serve --host "$HOST" --port "$PORT" --livereload
  elif command -v jekyll >/dev/null 2>&1; then
    banner "jekyll"
    open_browser
    exec jekyll serve --host "$HOST" --port "$PORT" --livereload
  else
    printf 'run.sh: _config.yml found but jekyll is not installed — serving statically.\n' >&2
    printf '        gem install jekyll   (or: bundle install)\n\n' >&2
  fi
elif [ "$FORCE_STATIC" -eq 0 ] && [ -f "$ROOT/.nojekyll" ]; then
  printf 'run.sh: .nojekyll is set and there is no _config.yml — this is a static\n' >&2
  printf '        site, which is exactly how GitHub Pages will serve it.\n' >&2
fi

# ---- Static server ----------------------------------------------------------
banner "static"
open_browser

if command -v python3 >/dev/null 2>&1; then
  exec python3 -m http.server "$PORT" --bind "$HOST" --directory "$ROOT"
elif command -v ruby >/dev/null 2>&1; then
  exec ruby -run -e httpd "$ROOT" --bind-address "$HOST" --port "$PORT"
elif command -v npx >/dev/null 2>&1; then
  exec npx --yes serve --listen "tcp://$HOST:$PORT" "$ROOT"
else
  printf 'run.sh: need python3, ruby or npx to serve. Install one of them.\n' >&2
  exit 1
fi
