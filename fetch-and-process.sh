#!/usr/bin/env bash
# Fetch the approved Higgsfield assets and process them into site/assets/.
#
# Run this once d8j0ntlcm91z4.cloudfront.net is reachable. It is idempotent:
# re-running it re-fetches and re-encodes from scratch.
#
#   ./fetch-and-process.sh            # uses variant A for both stills
#   FUEL=B BAY=B ./fetch-and-process.sh
#
# Needs: curl, ffmpeg with libx264.

set -euo pipefail

CDN="https://d8j0ntlcm91z4.cloudfront.net/user_3GjfBZXakynUrIaoqxw3rGbFtB4"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAW="$ROOT/review"          # raws and review copies stay OUT of the deploy folder
OUT="$ROOT/site/assets"     # only processed files ship
mkdir -p "$RAW" "$OUT"

VIDEO="hf_20260905_082430_1b5b9091-2ef1-4b10-8e26-418bdd6f5d52.mp4"
FUEL_A="hf_20260905_082451_4f60247e-fda7-451e-8f09-d0ce0c24f88a.png"
FUEL_B="hf_20260905_082451_fa48c979-ffd4-4d72-8cbd-bfffa94c3f12.png"
BAY_A="hf_20260905_082454_df3e626d-d78a-4da6-9c8b-46e9ebe3536a.png"
BAY_B="hf_20260905_082454_3be031dc-e72a-4c9d-8aa2-3430d708c524.png"

FUEL_PICK="$([ "${FUEL:-A}" = "B" ] && echo "$FUEL_B" || echo "$FUEL_A")"
BAY_PICK="$([ "${BAY:-A}" = "B" ] && echo "$BAY_B" || echo "$BAY_A")"

say(){ printf '\n\033[36m==> %s\033[0m\n' "$1"; }

# ---------------------------------------------------------------- 0. reachable?
say "Checking the CDN is reachable"
if ! curl -fsS -o /dev/null --max-time 20 "$CDN/$VIDEO"; then
  echo "The CDN is still refusing this machine."
  echo "Nothing has been changed. Unblock d8j0ntlcm91z4.cloudfront.net and re-run."
  exit 1
fi
echo "Reachable."

# ---------------------------------------------------------------- 1. fetch
say "Fetching the approved raws"
curl -fsS -o "$RAW/hero-raw.mp4"  "$CDN/$VIDEO"
curl -fsS -o "$RAW/fuel-raw.png"  "$CDN/$FUEL_PICK"
curl -fsS -o "$RAW/bay-raw.png"   "$CDN/$BAY_PICK"
ls -lh "$RAW"

# ------------------------------------------------- 2. inspect before committing
say "Pulling review frames from the raw video"
ffmpeg -v error -ss 0   -i "$RAW/hero-raw.mp4" -frames:v 1 -q:v 2 "$RAW/frame-start.jpg" -y
ffmpeg -v error -ss 4   -i "$RAW/hero-raw.mp4" -frames:v 1 -q:v 2 "$RAW/frame-mid.jpg"   -y
ffmpeg -v error -sseof -0.1 -i "$RAW/hero-raw.mp4" -update 1 -frames:v 1 -q:v 2 "$RAW/frame-end.jpg" -y

say "Ending-rest check (motion per frame; the tail should fall back toward its start)"
ffmpeg -v error -i "$RAW/hero-raw.mp4" \
  -vf "tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG" \
  -f null - 2>&1 | grep -o 'YAVG=[0-9.]*' | tail -24 || true
echo "If those last values stay high, the shot drifts at the end: trim to the"
echo "last steady frame with -t rather than paying for a re-roll."

# ---------------------------------------------------------------- 3. scrub encode
# -g 8 -keyint_min 8 is the rule that matters: a keyframe every 8 frames so
# every scroll position seeks cleanly. crf 18 is the starting point. This clip
# mixes busy city detail with smooth sky gradient, and gradients band before
# detail does, so check the calm sky frames first if you raise crf.
say "Scrub encode"
ffmpeg -v error -i "$RAW/hero-raw.mp4" \
  -c:v libx264 -crf 18 -preset slow -g 8 -keyint_min 8 \
  -pix_fmt yuv420p -movflags +faststart -an "$OUT/hero-scrub.mp4" -y

SIZE=$(stat -c%s "$OUT/hero-scrub.mp4" 2>/dev/null || stat -f%z "$OUT/hero-scrub.mp4")
MB=$(awk "BEGIN{printf \"%.1f\", $SIZE/1048576}")
echo "hero-scrub.mp4 is ${MB} MB (${SIZE} bytes)"
echo "An 8 second 1080p clip wants roughly 6 to 11 MB. If it is far over, step"
echo "crf toward 20 to 22 first, then add -vf scale=1728:-2. Change one at a time."

# ---------------------------------------------------------------- 4. stills
say "Poster, ending frame and section stills"
ffmpeg -v error -i "$OUT/hero-scrub.mp4" -frames:v 1 -q:v 2 "$OUT/hero-poster.jpg" -y
ffmpeg -v error -sseof -0.1 -i "$OUT/hero-scrub.mp4" -update 1 -frames:v 1 -q:v 2 "$OUT/hero-ending.jpg" -y
ffmpeg -v error -i "$RAW/fuel-raw.png" -vf scale=1920:-2 -q:v 2 "$OUT/fuel-corridor.jpg" -y
ffmpeg -v error -i "$RAW/bay-raw.png"  -vf scale=1920:-2 -q:v 2 "$OUT/fitting-bay.jpg"  -y

# -------------------------------------------- 5. patch the real byte size in
say "Patching VIDEO_BYTES in index.html"
python3 - "$SIZE" "$ROOT/site/index.html" <<'PY'
import re, sys
size, path = sys.argv[1], sys.argv[2]
src = open(path, encoding='utf-8').read()
new, n = re.subn(r"var VIDEO_BYTES=\d+;", f"var VIDEO_BYTES={size};", src)
if n != 1:
    sys.exit(f"expected exactly one VIDEO_BYTES, found {n}")
open(path, 'w', encoding='utf-8').write(new)
print(f"VIDEO_BYTES set to {size}")
PY

# ---------------------------------------------------------------- 6. verify
say "Verifying every output"
for f in hero-scrub.mp4 hero-poster.jpg hero-ending.jpg fuel-corridor.jpg fitting-bay.jpg; do
  p="$OUT/$f"
  [ -s "$p" ] || { echo "MISSING or empty: $f"; exit 1; }
  printf '  %-20s %8s bytes  %s\n' "$f" "$(stat -c%s "$p" 2>/dev/null || stat -f%z "$p")" \
    "$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of csv=p=0 "$p")"
done

say "Done. Assets are in site/assets/ and the raws stayed in review/."
cat <<'NEXT'

Still to do after this, and each one needs the real footage:

  1. Serve site/ and scrub the hero top, middle and bottom. Watch Chrome.
  2. Worst-frame legibility audit: every caption band at 3.5:1 or better
     against the busiest frame it sits over, not the average one.
  3. Flick test the beat map at 120, 240 and 360 px wheel steps.
  4. Reduced motion on, then flipped live mid-session, both directions.
  5. Load with the video blocked: the page must still be complete.
  6. Then deploy, and patch the og tags at the DEPLOY STEP comment.

NEXT
