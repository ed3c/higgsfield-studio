# Owner exception：bundled-FFmpeg Python wheels（OpenCV、PySceneDetect、librosa）

**決定（verbatim，由 parent session 轉述）**：Neon 2026-11-27 ~01:37 UTC+8 —「Approved: OpenCV, PySceneDetect, librosa. Record this approval as the explicit owner exception for the bundled-FFmpeg wheels. Use them to add camera-movement estimation, dark-segment cut vs lighting disambiguation, and music analysis to the pack as new files (do not overwrite v1 outputs).」

適用範圍：只限 Studio-specific path（`studio/reverse/ext_analyses.py`），在 box 的 `/workspace/afp-tools/venv` 中執行。**不會**修改 Soodles 共用路線的授權或准入規則；沒有 vendoring，沒有重新散布。

| 套件（實際安裝） | 版本 | 自報授權 | 內含／帶入的需要注意項目 |
|---|---|---|---|
| opencv-python-headless | 5.1.0.95 | Apache-2.0 | wheel 內含 libavcodec/libavformat/libavutil/libswscale/libswresample（FFmpeg，LGPL）、libaom、libdav1d、libvpx、libavif（BSD 類）、libopenblas（BSD）、libgfortran（GPL＋runtime exception）、libquadmath（LGPL）；第三方授權見 dist-info `LICENSE-3RD-PARTY.txt` 與 `sboms/` |
| scenedetect | 0.7.3 | BSD-3-Clause | 帶入 tqdm（**MPL-2.0 AND MIT**）、click（BSD-3）、platformdirs（MIT） |
| librosa | 1.0.1 | ISC | 帶入 **soxr 1.1.0（LGPL-2.1+）**、soundfile 0.14.0（BSD-3；內含 libsndfile，LGPL）、numba/llvmlite（BSD／Apache-2.0 w/ LLVM exception）、scipy、scikit-learn（BSD）、pooch、joblib、msgpack、decorator、lazy_loader |

執行時的限制措施（降低 copyleft 部分的實際使用）：
- 音訊由系統 ffmpeg 先轉成 22,050 Hz 的 float32 PCM，librosa **不使用** soxr 重新取樣，也**不透過** soundfile／libsndfile 讀檔。
- PySceneDetect 讀取的是 ffmpeg 產生的 H.264 proxy（OpenCV backend → 會用到 wheel 內含的 FFmpeg 解碼，屬於本 exception 的範圍）；`show_progress=False`。
- OpenCV 的 optical flow／ORB 用在 ffmpeg 產生的 5 fps 灰階 raw 影格上。

**仍需 Neon 確認**：tqdm（MPL-2.0）與 soxr（LGPL-2.1+）是被間接帶入的弱 copyleft 依賴，**不在**原核准文字明確列出的範圍內。本次 soxr 沒有被呼叫；tqdm 會被 scenedetect import，但不修改、不散布。如果 Neon 不接受，E1（PySceneDetect）的結果要改標 HOLD。
