# REA-Video：pin + 授權／依賴審查（僅審查，不執行）

Owner approval：Neon 2026-11-27 ~01:37 UTC+8「Approved: pin + licence/dependency review of REA-Video and HyperFrames (review only, no execution yet; REA's CC BY-SA separation weights stay HOLD unless the review says otherwise)」。
Reviewer：Grok Bot（static source read；沒有 pip install、沒有執行 CLI／install_skill.sh／plugin、沒有下載任何模型）。

## Pin

| 項目 | 值 |
|---|---|
| Repo | https://github.com/JuneYaooo/rea-video |
| Handoff pin（審查對象） | `8b40ef79beffa4d9a9a8c5e407c64ba11192063c`（2026-11-24T21:22:28-08:00） |
| 審查時 HEAD | `78160e053d378018e970d802d7bb7fa976c649f3`（比 pin 多 2 個 commit：3D motion forensics、remake planning）——**未採用**；採用前需另做差異審查 |
| LICENSE | Apache-2.0；blob `48d71e69dd25a513cdf96663c666cc3385cf0743`；sha256 `2beb280b855389587b12dfda5f61a7baf09d1c4a20aac833b1c96f9569c5e458` |
| NOTICE | blob `e0d50aa90756bae258da59540b35e41c9bfe2ec4`；sha256 `abffceee…025b`（"Copyright 2026 JuneYaooo, Apache-2.0"） |
| Package | `rea-video` 0.1.0，`requires-python >=3.10` |

## 依賴（pyproject @pin）

| 依賴 | 授權 | 備註 | 判定 |
|---|---|---|---|
| numpy | BSD-3-Clause | | ALLOW |
| opencv-python-headless >=4.8,<5 | Apache-2.0；wheel 內含 FFmpeg（LGPL）／libaom／dav1d 等 | 被 Neon 2026-11-27 的 owner exception 涵蓋；**版本上限 <5，box 的 Studio venv 目前是 5.1** → 需要獨立 venv | ALLOW（exception），獨立 venv |
| Pillow | MIT-CMU | | ALLOW |
| PyYAML | MIT | | ALLOW |
| videomd >=1.2 | Apache-2.0（PyPI 1.2.0） | VIDEO.md 規格驗證 | ALLOW（待 pin 版本） |
| onnxruntime | MIT | 用來跑分離模型 | ALLOW（runtime 本身） |
| ffmpeg／ffprobe（系統） | GPL build | HF-Q01 外部工具 | ALLOW（Q01） |
| [ocr] rapidocr-onnxruntime | Apache-2.0 | 會順帶裝有 GUI 的 opencv-python；install_skill.sh 會刪掉再重裝 headless | HOLD（需要時另審） |
| [asr] sherpa-onnx | Apache-2.0 | 首次使用下載 SenseVoice（約 160 MB）＋ speaker 模型（約 35 MB） | HOLD（模型權重另審；S1 已有 Whisper SRT，不需要） |

## 模型權重（首次執行時自動下載；本次都沒有下載）

| 模組 | 權重 | 來源 URL | 授權 | 判定 |
|---|---|---|---|---|
| `stems.py` 人聲／配樂分離 | UVR-MDX-NET-Inst_HQ_3.onnx（約 67 MB，sha256 `317554b0…dc`） | github.com/TRvlvr/model_repo releases | **沒有找到明確的權重授權**（UVR 程式碼是 MIT，社群訓練的權重不保證同授權） | HOLD |
| `effects.py` 對白／音樂／音效分離 | bandit-v2-multi.onnx（約 149 MB，sha256 `319b6293…e4`） | **第三方鏡像** github.com/xuankhanh/MediaDownloader | 原始碼註解寫 **CC BY-SA 4.0**（Watcharasupat et al.） | **HOLD（維持）**：屬於 share-alike 權重，而且是非原作者的鏡像來源；本次審查不解除 |
| `faces.py` | YuNet face_detection_yunet_2023mar.onnx（約 230 KB） | opencv_zoo（pinned commit） | opencv_zoo 標示 MIT | ALLOW-candidate；但 handoff 禁止推論受保護身分 → 對 S1 預設停用 |
| `speech.py`／`speakers.py` | SenseVoice、silero_vad、pyannote 分段、3D-Speaker | k2-fsa/sherpa-onnx releases | 各模型授權不同，需逐一查核 | HOLD |
| `overlay.py` OCR | PP-OCRv4/v5 rec | modelscope.cn | Apache-2.0（PaddleOCR） | HOLD（ocr extra 未採用） |

## 網路／資料範圍、安裝 hook

- `gemini.py`／`vlm.py`：只有在使用 `--vlm` 時才會把影片／影格送到外部 API（Gemini 或 OpenAI-compatible）。對 S1 **禁止**（private_analysis，不能把原始媒體送給第三方）。
- `scripts/install_skill.sh`：會建 venv、pip install，並在 `~/.claude`、`~/.codex`、`~/.agents`、`~/.gemini` 下建 symlink → 只能由 owner 明確執行；box 上不跑。
- `.codex-plugin`／`.claude-plugin`：plugin marketplace 的安裝方式，handoff 已標為 NOT_RUN／未核准，維持不變。
- 遙測：原始碼中**沒有發現遙測**（只會下載模型）。

## 結論（scoped）

| 範圍 | 判定 |
|---|---|
| REA-Video 核心（Apache-2.0）@8b40ef7，在獨立 venv 中只用 shots/visual/motion/transitions/report/videomd，**不用分離、ASR、OCR、臉部、VLM** | **ALLOW-CANDIDATE**：下一步要 Neon 核准執行；需要獨立 venv（opencv<5），並在離線、`REA_VIDEO_MODELS` 指向空目錄的條件下跑 |
| UVR MDX-Net 權重 | HOLD（權重授權不明） |
| BandIt v2 權重（CC BY-SA 4.0，第三方鏡像） | **HOLD（維持）** |
| `--vlm`（Gemini/OpenAI） | BLOCK（S1 不能外傳） |
| install_skill.sh／plugin 安裝 | NOT_RUN（需要 owner 明確執行） |

執行前還需要：鎖定所有依賴的版本與 SBOM、斷網執行、確認不寫入 `~/.cache/rea-video/models`。
