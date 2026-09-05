#!/usr/bin/env python3
"""Generate a STAND-IN hero clip so the scroll engine can be demonstrated.

This is not Sky Worth's footage. It is a procedural blue-hour descent used only
to prove the scrub pipeline end to end while the real Higgsfield asset cannot be
fetched. Delete it and run ./fetch-and-process.sh once the CDN is reachable.

Pipes raw RGB frames into ffmpeg, so nothing large touches the disk.
"""
import subprocess, sys, numpy as np

W, H, FPS, SECS = 1280, 720, 30, 8
N = FPS * SECS
OUT = sys.argv[1] if len(sys.argv) > 1 else "review/placeholder-raw.mp4"

rng = np.random.default_rng(20260905)

# ---- the light field: points on a ground plane, seen from above -------------
NL = 620
LX = rng.normal(0, 0.62, NL)
LY = rng.normal(0, 0.62, NL)
# a few dense clusters, the way a city sits on hills rather than spread evenly
for _ in range(7):
    cx, cy = rng.normal(0, 0.45, 2)
    m = rng.choice(NL, 60, replace=False)
    LX[m] = cx + rng.normal(0, 0.09, 60)
    LY[m] = cy + rng.normal(0, 0.09, 60)
LB = rng.uniform(0.35, 1.0, NL) ** 1.7                       # brightness
LW = rng.uniform(0, 1, NL)                                    # warm vs cool mix
SODIUM = np.array([1.00, 0.62, 0.29])                         # warm street light
COOLROOF = np.array([0.55, 0.70, 0.92])                       # iron sheet sheen

ys = np.linspace(0, 1, H, dtype=np.float32)[:, None]
xs = np.linspace(-1, 1, W, dtype=np.float32)[None, :]

def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)

ff = subprocess.Popen(
    ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
     "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
     "-c:v", "libx264", "-crf", "20", "-preset", "medium",
     "-pix_fmt", "yuv420p", "-an", OUT],
    stdin=subprocess.PIPE)

for i in range(N):
    t = i / (N - 1)

    # ---- sky: deep blue above, the last of the light low down --------------
    horizon = 0.30 + 0.30 * t                 # descending: the ground rises
    sky_t = np.clip((ys - 0.0) / max(horizon, 1e-3), 0, 1)
    top = np.array([0.031, 0.055, 0.110])     # matches --canvas
    mid = np.array([0.055, 0.115, 0.215])
    glow = np.array([0.255, 0.180, 0.130])    # warm haze at the horizon
    img = (top[None, None, :] * (1 - sky_t)[..., None]
           + mid[None, None, :] * sky_t[..., None])
    band = np.exp(-((ys - horizon) ** 2) / (2 * 0.055 ** 2))
    img = img + glow[None, None, :] * band[..., None] * 0.55
    img = np.repeat(img, W, axis=1) if img.shape[1] == 1 else img

    # ---- ground below the horizon, slightly darker -------------------------
    below = smoothstep(horizon - 0.02, horizon + 0.06, ys)
    img *= (1 - 0.42 * below)[..., None]

    # ---- the descent: lights fly outward as the camera drops --------------
    h = 1.0 - 0.93 * (t ** 1.35)              # camera height, eased
    scale = 0.30 / max(h, 0.055)
    sx = (W * 0.5 + LX * scale * W * 0.62).astype(np.int32)
    sy = (H * (horizon + 0.16) + LY * scale * H * 0.62).astype(np.int32)
    rad = np.clip(1.0 + scale * 3.4, 1, 26).astype(int)
    amp = LB * (0.55 + 0.85 * min(scale, 2.2))

    r = int(rad if np.isscalar(rad) else rad)
    gy, gx = np.mgrid[-r:r + 1, -r:r + 1]
    kern = np.exp(-(gx ** 2 + gy ** 2) / (2 * (r / 2.1 + 0.6) ** 2)).astype(np.float32)

    for k in range(NL):
        x0, y0 = sx[k], sy[k]
        if x0 < -r or x0 > W + r or y0 < -r or y0 > H + r:
            continue
        xa, xb = max(0, x0 - r), min(W, x0 + r + 1)
        ya, yb = max(0, y0 - r), min(H, y0 + r + 1)
        if xa >= xb or ya >= yb:
            continue
        ks = kern[ya - (y0 - r):yb - (y0 - r), xa - (x0 - r):xb - (x0 - r)]
        col = SODIUM * LW[k] + COOLROOF * (1 - LW[k])
        # a slow flicker so the scene is never dead
        fl = 0.86 + 0.14 * np.sin(i * 0.21 + k * 1.7)
        img[ya:yb, xa:xb, :] += ks[..., None] * (col[None, None, :] * amp[k] * 0.5 * fl)

    # ---- the cloud pass: a real lens moment on the way down ----------------
    cy_ = -0.35 + 2.0 * t
    cloud = np.exp(-((ys - cy_) ** 2) / (2 * 0.20 ** 2))
    strength = float(smoothstep(0.20, 0.34, t) * (1 - smoothstep(0.52, 0.68, t)))
    if strength > 0.001:
        haze = np.array([0.62, 0.70, 0.82])
        a = (cloud * strength * 0.80)[..., None]
        img = img * (1 - a) + haze[None, None, :] * a

    # ---- the settle: one locator pulse on the resting frame ---------------
    s = smoothstep(0.80, 1.0, t)
    if s > 0.001:
        px, py = W * 0.5, H * 0.62
        d = np.sqrt((xs * W / 2 - (px - W / 2)) ** 2 + (ys * H - py) ** 2)
        ring = np.exp(-((d - 26) ** 2) / (2 * 3.6 ** 2)) + np.exp(-(d ** 2) / (2 * 4.0 ** 2)) * 1.6
        img += (np.array([0.169, 0.878, 0.769])[None, None, :] * (ring * s * 0.85)[..., None])

    np.clip(img, 0, 1, out=img)
    ff.stdin.write((img * 255).astype(np.uint8).tobytes())

ff.stdin.close()
if ff.wait() != 0:
    sys.exit("ffmpeg failed")
print(f"wrote {OUT}")
