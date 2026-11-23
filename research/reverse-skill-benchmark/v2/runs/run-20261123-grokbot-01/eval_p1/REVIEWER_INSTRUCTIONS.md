# P1 blind review — reviewer instructions (Benchmark v2, run-20261123-grokbot-01)

You are ONE of two independent reviewers (R1 or R2). Use only the files in this folder.
- **Do not open** `/workspace/hs-bench-private/`, `/workspace/hs-bench/`, `/workspace/hs-bench-jobs/`, or any other folder.
- **Do not read** the other reviewer's sheet.
- **Do not try** to guess which tool made an image.

## Task: reconstruction fidelity
Each image B00xx is a text-only attempt to reconstruct its case reference in `refs/` (C01 portrait, C02 environment, C03 aircraft over sea). `packet_index.json` lists the images for each case. Score each image against its own reference. Do not score pixel identity; score whether the visible properties match.

## Scale (spec §7), whole numbers 0–5
0 broken / unrelated · 1 poor · 2 weak · 3 acceptable · 4 strong · 5 excellent

## Criteria (P1 weights)
| criterion | weight | what to judge against the reference |
| --- | --- | --- |
| composition | .25 | framing, subject placement, crop, shot size, balance |
| perspective | .20 | camera height and angle, vanishing point, lens and depth feel, scale relations |
| lighting | .15 | key direction, ratio, practicals, softness, mood |
| palette | .10 | hues, saturation, grade, black level |
| material | .15 | surface and texture realism (lace, skin, chrome, stone, sea, airframe) and photographic texture |
| artifact_control | .15 | absence of malformed geometry or anatomy, AI smoothness, text, watermarks |

## Hard fail (separate column `hard_fail` = yes/no plus `hard_fail_reason`)
Major malformed geometry or anatomy · unrelated scene · significant watermark or text leakage.

## Output
Fill only your own sheet, `ratings_R1.csv` or `ratings_R2.csv`:
- `score_0_to_5` on every row (6 rows per image, 17 images).
- `hard_fail` (yes/no) on each row, repeating the image-level value.
- `notes`, kept short.
- `scored_at_iso8601`.

Score every image. Do not skip any or cherry-pick.
