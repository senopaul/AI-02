# Approved assets

Every generation below was approved by the owner. The URLs are Higgsfield's
result CDN. This file exists because the build container's egress policy blocks
that CDN, so the files could not be pulled down in the session that made them.
Nothing here needs regenerating. It needs fetching.

Run `./fetch-and-process.sh` once `d8j0ntlcm91z4.cloudfront.net` is reachable.

## The hero footage: APPROVED, passed the video gate

- **Model:** Seedance 1.5 Pro, image-to-video, 1080p, 8 seconds, silent
- **Cost:** 24 credits
- **Job:** `1b5b9091-2ef1-4b10-8e26-418bdd6f5d52`
- **URL:** https://d8j0ntlcm91z4.cloudfront.net/user_3GjfBZXakynUrIaoqxw3rGbFtB4/hf_20260905_082430_1b5b9091-2ef1-4b10-8e26-418bdd6f5d52.mp4

The shot: a continuous descent from high above Kampala at blue hour, down
through a thin cloud layer that streaks the lens, settling at rest on one
vehicle on a narrow murram road.

## The start frame it was animated from: APPROVED

- **Model:** Soul Cinema, 16:9, 2k. **Cost:** 0.12 credits
- **Job:** `0a9b831e-7bc8-4601-bc09-e2d8b034a796`
- **Higgsfield media id:** `8163d6c0-58d9-4853-a560-d6b402b9a40e`
- **URL:** https://d8j0ntlcm91z4.cloudfront.net/user_3GjfBZXakynUrIaoqxw3rGbFtB4/hf_20260905_082058_0a9b831e-7bc8-4601-bc09-e2d8b034a796.png

## Supporting stills: generated, awaiting a pick

Two variants each. The owner picks one per slot; the script defaults to
variant A. Both are 4:3, 2048x1536, Soul Cinema, 0.12 credits each.

### Fuel section (`assets/fuel-corridor.jpg`)

- **A:** `4f60247e-fda7-451e-8f09-d0ce0c24f88a`
  https://d8j0ntlcm91z4.cloudfront.net/user_3GjfBZXakynUrIaoqxw3rGbFtB4/hf_20260905_082451_4f60247e-fda7-451e-8f09-d0ce0c24f88a.png
- **B:** `fa48c979-ffd4-4d72-8cbd-bfffa94c3f12`
  https://d8j0ntlcm91z4.cloudfront.net/user_3GjfBZXakynUrIaoqxw3rGbFtB4/hf_20260905_082451_fa48c979-ffd4-4d72-8cbd-bfffa94c3f12.png

### Why-us section (`assets/fitting-bay.jpg`)

- **A:** `df3e626d-d78a-4da6-9c8b-46e9ebe3536a`
  https://d8j0ntlcm91z4.cloudfront.net/user_3GjfBZXakynUrIaoqxw3rGbFtB4/hf_20260905_082454_df3e626d-d78a-4da6-9c8b-46e9ebe3536a.png
- **B:** `3be031dc-e72a-4c9d-8aa2-3430d708c524`
  https://d8j0ntlcm91z4.cloudfront.net/user_3GjfBZXakynUrIaoqxw3rGbFtB4/hf_20260905_082454_3be031dc-e72a-4c9d-8aa2-3430d708c524.png

## What still has to happen after the fetch

These are the steps the script performs or prepares, in order:

1. **Scrub encode.** Re-encode with a keyframe every 8 frames, or scrubbing
   stutters because the browser can only seek precisely to keyframes. This one
   step is the difference between smooth and broken.
2. **Poster and ending frame** cut from the encoded file.
3. **The ending-rest check.** A motion curve per frame. If the tail stays high,
   the shot never truly settles and wants a trim rather than a re-roll.
4. **Stills sized** to 1920 wide with one clean compression pass.
5. **`VIDEO_BYTES`** in `index.html` patched to the real encoded byte size,
   which is the fallback the loading ring uses when the host omits
   Content-Length.
6. **The audits that need the real footage**: the worst-frame legibility audit
   per caption band at 3.5:1 minimum, and the flick test on the beat map.
7. **The og tags** patched with the live URL at deploy time. They are marked
   with a `<!-- DEPLOY STEP -->` comment in `index.html`.

## Cost so far

| Round | Spend |
|---|---|
| First frames, three across three models | 4.12 |
| Reference recomposition, two | 2.12 |
| Kampala night, four | 0.48 |
| Kampala blue hour, four | 0.48 |
| Hero video, Seedance 1.5 Pro | 24.00 |
| Supporting stills, four | 0.48 |
| **Total** | **~31.8 of 270** |
