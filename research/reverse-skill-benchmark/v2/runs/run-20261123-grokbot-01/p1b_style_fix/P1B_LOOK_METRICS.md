# P1b-style-fix: look metrics against the refs and against P1 (2026-11-23 ~19:55 Asia/Taipei)

Computed with `look_metrics.py`. Every image is resized to 1344×752 with INTER_AREA. Refs are the locked masked 3840×2160 PNGs. P1 = the mean of that case's outputs (6/6/5 images). P1b = the mean of 3 images per case.

"Gap closed" = 1 − |P1b − ref| / |P1 − ref|. Negative means the gap got worse; above 100% would mean P1b landed on the other side, closer.

Measured only. These are **not** quality scores and do not replace the R1/R2 blind review. P1b is executor-authored, so no Skill credit is given.

Metrics:
- `luma`: mean of 0–255.
- `black_p1` / `white_p99`: luma at the 1st and 99th percentiles.
- `sat`: mean HSV S.
- `a`, `b`: Lab means minus 128.
- `sharp_c`: Laplacian variance over the central 50%.
- `edge_ratio`: Laplacian variance of the top and bottom sixths ÷ `sharp_c`. This is a depth-of-field proxy; **it is invalid for C01**, where the bottom band holds the in-focus ruff.

| case | metric | ref | P1 mean | P1b mean [min–max] | gap closed |
| --- | --- | --- | --- | --- | --- |
| C01 | luma | 74.0 | 56.4 | 70.6 [61.2–84.3] | **81%** |
| C01 | white_p99 | 187 | 149 | 163 [148–172] | 37% |
| C01 | black_p1 | 10 | 14.8 | 17.3 [14–23] | **−52%** (lifted more) |
| C01 | sat | 56.5 | 62.6 | 39.7 [32–47] | **−179%** (overshoot: now too desaturated) |
| C01 | a / b | 0.7 / 2.4 | 1.9 / 6.1 | 0.9 / 3.3 | 84% / 76% |
| C01 | sharp_c | 18 | 311 | 68 [43–98] | **83%**, still 3.8× ref |
| C02 | luma | 69.5 | 122.9 | 92.2 [88.5–99.3] | 58%, still +23 |
| C02 | white_p99 | 195 | 224 | 162 [147–172] | −14% (overshoot: highlights now too dull) |
| C02 | black_p1 | 17 | 20.3 | 10.7 [8–14] | −90% (overshoot: now darker blacks than ref) |
| C02 | sat | 58.3 | 37.1 | 37.2 | 0% |
| C02 | a / b | −2.2 / 1.3 | −0.3 / 6.7 | −5.3 / 1.8 | −64% (too green-teal) / **90%** |
| C02 | sharp_c | 113 | 576 | 55 [28–107] | **87%** (overshoot to soft; niobium617 cell 28) |
| C02 | edge_ratio | 0.07 | 0.45 | 0.41 | 11%: background still not defocused relative to centre |
| C03 | luma | 114.6 | 124.5 | 113.2 | **86%** |
| C03 | black_p1 | 1 | 21 | 11.3 [5–16] | 48% |
| C03 | white_p99 | 192 | 177 | 162 [160–164] | −103% (sky now too dull) |
| C03 | sat | 42.7 | 28.8 | 36.5 | 56% |
| C03 | a / b | −4.9 / −1.1 | −4.7 / −0.8 | −6.0 / +0.8 | negative %, but absolute errors ≤ 1.9 Lab units (negligible) |
| C03 | sharp_c | 50 | 105 | 30 [23–40] | 63% (overshoot to soft) |
| C03 | edge_ratio | 0.25 | 0.63 | 0.68 | −12% |

## Read-out
- **Closed.**
  - The CG-crispness tell: centre sharpness is down 63–87% of the gap in all cases.
  - The C02 golden-hour/sunny warm cast (b\* gap closed 90%) and its exposure, partially (−31 luma).
  - The C01 mean exposure and warm cast.
  - The C03 exposure, lifted blacks (about half) and saturation.
  - Visual check of `p1b_compare.jpg`: C02 is overcast, C03's chalk cliffs are gone, C01 is softer.
- **Remaining or new gaps.**
  1. **Highlights are compressed in every case.** p99 is 160–165 against refs of 187–195. The look lock's "muted, roll-off, no HDR" wording pulled the whites down. This is why C01 still *reads* darker than the high-key ref even though its mean luma is close: the face and ruff do not reach the ref's near-clipping brightness.
  2. **C01 is now over-desaturated** (sat 40 vs 57) and its blacks are more lifted (17 vs 10). The skin lost the ref's pink flush. Centre sharpness is still 3.8× the ref, because the face is not as gauzy.
  3. **C02 is still about 0.5 stop too bright on average.** Yet its whites are too dull and its blacks too deep: the tonal shape is wrong, not just the level. It is too green-teal (a\* −5.3 vs −2.2), still under-saturated, and its sharpness overshot to soft. Above all, **the depth-of-field structure is unchanged** (edge_ratio 0.41 vs 0.07): the ref has a sharp near hood and a defocused city, while P1b softens everything evenly. Visually, the hood still does not loom large. That is a camera-distance and composition gap that the style-only block did not touch, by design.
  4. **C03:** blacks are still not crushed (11 vs 1), the sky is too dull (p99 162 vs 192), it overshot to soft, and the edge ratio is unchanged.
- **Overall.** A style-only appended block moves global grade and sharpness strongly. It overshoots on softness and highlight compression, and it cannot create *differential* depth of field (sharp subject, defocused surround) without composition or camera-distance wording.

No regeneration done. Next-iteration ideas (proposal only, not executed):
- State absolute tonal anchors: "brightest highlights near white, true black shadows".
- For C01, keep natural skin saturation and a pink flush.
- For C02, put the camera within half a metre of the hood, with the hood razor-sharp and the city out of focus.
