# S1 onNBysMf9WM — Producer QA report (pre-verifier)

- Source: https://www.youtube.com/watch?v=onNBysMf9WM (NTT ICC, 2333 s)
- Rights: rights.json — owner decision '軟體可以下載就下載', private analysis only, no redistribution; not a rights-holder grant.
- Master: onNBysMf9WM.mkv — av1 3840x2160 30000/1001 + opus 48000Hz 2ch; duration 2333.388000 s; yt-dlp format 401+251 (yt-dlp default best; 2160p AV1 chosen over 2160p VP9 313 by yt-dlp codec preference; no upscaling).
- WAV: onNBysMf9WM.audio.wav — pcm_s24le 48000Hz 2ch; duration 2333.373250 s (from same master, map 0:a:0; Opus decoded to PCM, delta vs master container ~0.015 s).
- SRT: onNBysMf9WM.ja.srt — Whisper large-v3 ASR (no official/auto subs exist); 300 cues after deterministic hallucination post-filter (26 dropped, logged); raw ASR kept.
- Alignment: automated sampled check PASS 8/8 (mean 0.931 vs shifted 0.160).
- Known limits: ASR text contains recognition errors; long music-only stretches have no cues by design; filter R1 also dropped one possibly real short phrase at 1496.9 s ("作品空間ですね", 27 s window) — see asr_postfilter_log.json.
- Independent gate verdicts: produced separately by studio/source/yt_gates.py (not part of this file).
