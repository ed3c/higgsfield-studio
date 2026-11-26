# Higgsfield Studio — Evidence-Grounded Agentic Film Production / Handoff

- Contract: HF-AGENTIC-FILM-2026-11-26
- Decision state: DECISION_COMPLETE (scope/implementation policy only).
- Execution state: NOT_RUN. Parent Goal is OPEN. No implementation, media download, asset upload, generation, GPU rental, worker start, paid API, or external publication performed by this handoff session.
- Destination: ed3c/higgsfield-studio, main, this file. Source baseline Studio commit d9eb999966df3794b07f954af091ea3c7b4bc73f (actual tree 7d272550452bb291195553c1a3f90264b7ed70c1). Soodles source commit 939875f91a8d6d38853989b5bd3a8a497a06bf88 (tree 0cbc832b55a13872115483390fb088e979be792c).
- Owner: human project owner for scope, rights, costs, creative acceptance and promotion; Main Session for engineering decisions and integration; respective original domain/provider owners for effects and independent acceptance. Consumers: fresh Main/Codex CLI/Antigravity, Soodles, Studio managers, distillation Teacher/Student/Observer, GPU/provider adapters, editor, local reviewer UI. Do not infer that any of these has received or consumed this file.
- Stop: fresh conversation must receive explicit GO before implementation or experiments. Paid effects need separate approved budget/entitlement. Handoff commit is the only authorized mutation now.
- Language: Traditional Chinese; technical identifiers in English. Public repository: private Notion/Drive locators, account details, raw private media, tokens and host-specific private paths are NOT copied here. Authorized resolver uses the exact source titles and stable logical source IDs below. Missing access is a coverage gap, not permission to discard the obligation.

## 0. Original intent and precedence

Original user task (verbatim public-safe input):

> 前沿Agent 開源可商用庫 youtube 影片下載與Codex CLI & Google Antigravity & Colab & HiggsField GPU 服務的影片生成與剪輯，結合 @Notion 電影、當代藝術逆向分析 skills & 工業級影片生成，配合 HiggsStudio 架構，Codex CLI 結合 MAGI-2 現已上線，僅限 Higgsfield 提供。
>
> 現在你可以試用這款規模最大、接近最先進水準的影片模型。
>
> > 每秒生成費用 $0.08
> > 4800 億個參數，每次約有 280 億個參數處於啟用狀態
> > 最高可生成 30 秒的 1080p 影片，並支援最多 20 個參考素材
>
> 現已可在 Higgsfield 及透過 Higgsfield MCP 使用。
>
> 介紹 Blender 中的 Higgsfield。
>
> > 提示場景並建構粗略模型
> > 描述攝影機移動並使其動畫化
> > 手動調整任何內容
> > 在數秒內重新粗略建構整個鏡頭
>
> 參考第一部使用 Blender + Higgsfield 管線製作的混合 AI 動畫短片。
>
> 我們結合手工製作的 2D 分鏡與 3D Blender 預覽，搭配 AI 動畫，創造出「Passport Rush」。
>
> 這部影片現已開放原始碼，因此您可以了解我們的製作方式。每個提示與資產皆公開。公開。
>
> 現已透過 Higgsfield MCP 或 Supercomputer 提供。
>
> 目標是下載https://www.youtube.com/watch?v=onNBysMf9WM 並全方位逆向分析並結合HiggsField 範例 full project 「Passport Rush」 專案架構與用逆向分析流程來處理專案到創作方法論到提示詞的蒸餾方法（不寫死，可以任選）以上所有創作架構到 HiggsField Studio

Handoff instruction (verbatim):

> 用 soodles handoff skill 交接任任務給新對話，直接 commit handoff.md 到 higgsField Studio ，先不遺漏的定義這個對話的任務內容，紀錄的 handoff 不語意退化，先用 thinking route 問我釐清這個問題 Scope & 實作這個需求的問題再實作，提問直到 thinking route 雙腦乒乓認知遞迴沒有疑問為止

Accepted human decision (verbatim):

> Higgsfield Studio Handoff Thinking Route 第一輪決策：HF-Q01=A；HF-Q02=A；HF-Q03=A；HF-Q04=A；HF-Q05=A；HF-Q06=A。保留 H01～H32、完整原始需求、候選工具、原 Oracle、授權政策、失敗史與 NOT_RUN。繼續 Thinking × Ambitious 雙腦反證、逐義務四分類及 Ponytail 最短閉環審查。只詢問真正會改變 Scope、實作或驗收的新問題。達到 Decision-Complete 後直接 commit 完整 handoff.md 到 Higgsfield Studio 並取得 Git readback。

Precedence: original human goal and accepted six decisions > prior assistant candidate designs (not implemented) > current source facts (which can correct outdated status, not erase future obligations). Existing benchmark/J4 protocols are immutable for their own run identity; a new film-production experiment is a separate contract, not a replacement. Public-safe original user wording above is preserved as claims/requirements, not proof of provider capability, download rights or open-source status. No absolute proof of all unknown semantic retention is claimed; the obligation mapping, original request, existing exact artifacts and readback are independently checkable.

Mission: a reusable industrial Agentic Film Studio, not a pile of prompt templates. Three flywheels:
1. Reverse Engineering: film/artwork/full project -> source evidence -> reverse analysis -> creative methodology -> distilled skills.
2. Film Production: creative intent -> art direction -> elements -> storyboard -> Blender previs -> video generation -> editing.
3. Creative Evolution: independent visual/audio QC -> Evals -> failure analysis -> regression -> skill improvement -> next work.
Original creation rather than copying protected output. Methods must transfer to a novel subject, scene and work.

## 1. Thinking × Ambitious decisions and counterexamples

All A choices below accepted. Unselected alternatives are retained; no new grant is inferred.

| ID | Accepted A (full decision) | Unselected B / counterexample and reason |
|---|---|---|
| HF-Q01 | Core strictly uses permissive open-source licenses; explicitly allow Blender and FFmpeg as independent external creative tools, comply with applicable licenses, no vendoring, no evasion. | B: blanket exclusion of copyleft, Blender/FFmpeg and dependent routes HOLD, find alternatives. Existing Soodles route excludes FFmpeg-dependent tools. Accepted exception is limited to Studio external tooling, NOT a change to Soodles global license/admission, NOT blanket authorization for arbitrary GPL/LGPL dependency or redistribution. External tools must still be audited, versioned and separately gated; no use of subprocess/MCP to evade obligations. |
| HF-Q02 | Both the specified YouTube source and Passport Rush are mandatory independent research cases; Passport Rush is ground-truth-supported benchmark; a blocked source blocks only its dependent tasks. | B: finish specified YouTube first, then Passport Rush. Rejected artificial dependency: source identity differs and neither should substitute for the other. |
| HF-Q03 | Preserve H01–H32; first real end-to-end vertical slice, then incrementally connect remaining capabilities on named gaps. MVP PASS must not close Parent Goal. | B: build every manager/schema/provider runtime first. Counterexample: complete architecture can exist while no verified artistic operation transfers. |
| HF-Q04 | Manual selection AND capability-based automatic router; pin versions, skill combination, Oracle and provider per experiment; independent validation before ranking promotion. | B: manual only. Counterexample: static coupling impedes future selection; unpinned dynamic selection destroys reproducibility. Registry selection is separate from per-run immutable manifest. |
| HF-Q05 | Decision-Complete then directly commit handoff.md and Git readback. Fresh conversation explicit GO before implementation; paid generation separately approved budget. | B: immediately start free implementation and legal acquisition without fresh GO. Not selected. No download, upload, analysis job, generation, worker, GPU or repo code change authorized by this handoff. Read-only research already performed is evidence only. |
| HF-Q06 | Public Git stores public sources, full task semantics, logical references, verification contracts; private Notion/Drive locators, originals and sensitive content remain controlled; resolve through authorization, no private paths or credentials. | B: publish private page links but not content. Rejected. Preserve precise titles, dated source IDs and exact private evidence requirements, report MISSING_SOURCE if unable to resolve. |

Second review (same session methodological alternation, not two native agents):
- Thinking: first causal breakpoint is missing bytes/rights, not lack of another manager. Ambitious: exploit Passport Rush project + breakdown to get an independent reference Oracle rather than guess from result alone. Resolution Q02/Q03: independent source tracks, one evidence-backed method to first closure, complete coverage still mandatory. Counterexample: no actual source bytes = no measured cut timing, no original prompt claim.
- Thinking: strict Reverse Route license conflicts with external Blender/FFmpeg. Ambitious: preserve hybrid control of space/camera/time instead of removing it. Resolution Q01: explicit Studio external-tool exception only; keep original global Soodles guards, separately audit dependency/weight/asset rights, do not claim all upstream commands approved. Counterexample: embedding GPL or unknown model assets is not allowed merely because Blender can run outside the core.
- Thinking: one named candidate may appear strongest without independent samples. Ambitious: reusable strategy choice and cross-provider comparison. Resolution Q04: manual/automatic selection from admitted capabilities, fixed manifest per run and independent holdout, no score invention or hard-coded winner. Existing admitted text subsets are not authorization for full upstream execution.
- Thinking: a public file with private locators leaks source access paths. Ambitious: exact source discovery and full semantics still reachable. Resolution Q06: titles/logical IDs, authorized connector lookup; access gap holds dependent operations only, no public disclosure.
- Thinking: cost advertised vs charged and actual remote effect may differ. Ambitious: compare providers without losing control. Resolution Q05: explicit fresh GO, separate rights and budget, read preflight and receipts, no automatic paid retry/duplicate uncertain jobs. No need to decide exact GPU model now; provider capability/readback and pre-registered budget decide.
- Thinking: original P1/S13 oracle cannot be changed retroactively. Ambitious: new tests can improve artistic mechanism evaluation. Resolution: version new independent Oracle before trials; keep prior tests/results unchanged, do not share labels with tested Consumer.
- Ponytail: reuse existing Studio templates, budget CSV/track.py, research index, Soodles Reverse Route/Skill Composition/Harness² and Medium Compiler; no new scheduler, second harness, microservice fleet, second asset store or forced 20-manager implementation before a proven slice. Add only missing responsibility/adapter/schema as actual gap requires. No scope deletion. First proposed slice: three original shots (performance, spatial camera movement, artistic mechanism), one transferable method, one edit timeline; compare MAGI-2 and one admitted Colab model only when both are authorized. If the comparison is blocked, finish independent authorized evidence tasks; no fake comparison or full-goal closure.

No materially new human trade-off identified. Remaining rights, availability, exact commits, native integrations, budget quote, labels and source access are factual/effect checks with defined fail-closed recovery, not unanswered policy decisions. DECISION_COMPLETE does not imply evidence/implementation PASS. Reopen only for new conflict materially changing scope, authority, cost or acceptance. Source-bound dual-brain method: same model/session, no claim of independent agents or native Soodles runtime invocation. Prompt Delta for fresh Main relative to entire accepted input: consume this file and exact referenced original contracts; apply six decisions as explicit deltas; no change to Frozen earlier runs. No further delta/NOOP for consumers already holding these obligations.

## 2. Original obligation index and four-way classification

Classification is of current handoff treatment, not completion. KEEP=必須保留; MOVE=只可搬移 (exact original is referenced, not replaced); CHECK=需查證; UNWIRED=尚未接通. Each H row retains original scope even when CHECK/UNWIRED. Sections are precise coverage anchors; next/legal gate in sections 3–10. All implementation and new experiment rows are NOT_RUN unless a specific read-only fact is explicitly observed.

| ID | Original obligation (preserved) | Class | Source/owner -> Consumer; evidence / next |
|---|---|---|---|
| H01 | Download specified YouTube onNBysMf9WM | CHECK | S1 / SourceManager -> EvidenceManager; rights, identity, bytes, SHA; §3, blocked |
| H02 | Full multidimensional shot-by-shot reverse of S1 | UNWIRED | S1 / ReverseManager -> MethodologyManager; evidence pack/oracle; §4 |
| H03 | Full Passport Rush project research | CHECK | S2–S5 / ProjectManager -> ReverseManager; actual export/read permissions; §3–4 |
| H04 | Align film, breakdown, original prompts, Elements and assets | UNWIRED | S2–S5 / EvidenceManager -> independent evaluator; exact IDs/timestamps; §4 |
| H05 | Full Project -> creative methodology reverse | KEEP | S2–S5 / ReverseManager -> MethodologyManager; causal evidence; §4–5 |
| H06 | Methodology -> reusable Skill distillation | KEEP | Soodles / Teacher -> Student/Observer; §5, reference/holdout |
| H07 | Methodology -> Shot IR -> Prompt compilation | UNWIRED | MethodologyManager -> compiler -> provider; §6 |
| H08 | Select/replace/compose reverse methods, not hard-coded | KEEP | HF-Q04 / registry -> fresh Main; §5–6 |
| H09 | 100 film reverse research entries | MOVE | N1 / authorized Notion -> ReverseManager; exact title §3 |
| H10 | 100 contemporary art research entries | MOVE | N2 / authorized Notion -> Artwork Reverse; exact title §3 |
| H11 | 46 reverse engineering + universal distillation | MOVE | N3 / authorized Notion + Soodles -> registry; §3,5 |
| H12 | Frontier commercially usable open-source libraries/license gate | KEEP | HF-Q01 / rights reviewer -> registry; §5 |
| H13 | REA-Video, HyperFrames and all candidate tools | CHECK | §5 / registry -> runtime; licenses/compatibility, no automatic execution |
| H14 | Codex CLI execution | UNWIRED | runtime -> Main/Worker; native evidence §7 |
| H15 | Google Antigravity execution | UNWIRED | runtime -> alternate Agent; native evidence §7 |
| H16 | Colab GPU Worker | UNWIRED | provider owner -> runtime; authorization/CU/receipt §7 |
| H17 | Higgsfield GPU Worker | UNWIRED | provider owner -> runtime; rental readback §7 |
| H18 | Higgsfield MCP and official Skills | UNWIRED | catalog read observed, native generation NOT_RUN; §5,7 |
| H19 | MAGI-2 hosted provider capabilities/limits/cost | CHECK | catalog + official claims -> compiler/budget; §7 |
| H20 | Blender 3D previs/camera/blocking/animation | UNWIRED | HF-Q01 / PrevisManager -> compiler; external-tool compliance §6–7 |
| H21 | Elements-first identity and consistency | KEEP | Full Project/ElementsManager -> ShotCompiler; §6 |
| H22 | 20 domain-manager responsibility boundaries | KEEP | §6 / Main -> incremental implementation, no 20 microservices |
| H23 | Provider-independent Schema Compiler | UNWIRED | compiler -> provider adapters; validation §6–7 |
| H24 | OTIO/HyperFrames/editing and post-production | UNWIRED | editorial -> final cut; §6–7 |
| H25 | Drive/local/GitHub/Notion storage separation | KEEP | HF-Q06 / asset owner -> consumers; §6 |
| H26 | Medium Compiler local playable review | UNWIRED | editor/evidence -> UI reviewer; §6,9 |
| H27 | Soodles Reverse Route and Skill Composition with Eval | MOVE | fixed Soodles source -> Main/Composer; §5,11 |
| H28 | Independent Oracle, Fresh Student, Holdout, Regression | KEEP | supervisor/observer -> verification; §5,8–9 |
| H29 | Artwork-only -> Shot-only -> Composition acceptance | KEEP | existing art contracts -> independent visual reviewers; §8–9 |
| H30 | J4/P1/S13 original evidence, failures and NOT_RUN | MOVE | original project owner/benchmark artifacts -> fresh Main; §8 |
| H31 | Bounded Convergence, Human Approval, Freeze, Version, Reuse | KEEP | owner/observer -> registry; §9 |
| H32 | Three flywheels and cumulative cross-project creative capacity | KEEP | original goal §0 -> all domain consumers; §10, no Parent closure on slice |

Count 32/32. MOVE rows preserve complete original versioned artifact, not just the label. For private sources resolve before affected work, otherwise record source access gap. CHECK and UNWIRED are not deletion. Suggested design choices in §5–7 are candidates (not forced implementation of every option). Distinguish source metadata verification, actual loading, native consumption, product acceptance and comparative benefit.

## 3. Source registry, provenance, rights and acquisition

Public source locators (prior conversation source discoveries; some still unverified in this session):
- S1 mandatory: https://www.youtube.com/watch?v=onNBysMf9WM — original requested source. Previous direct read failed; original bytes not acquired. Identity/title/duration/rights remain to establish; never substitute a Passport Rush video and claim S1 complete.
- S2 candidate final film: https://www.youtube.com/watch?v=ZncA70OAgPw
- S3 candidate breakdown: https://www.youtube.com/watch?v=reFzEtCG_m8
- S4 official animation channel: https://www.youtube.com/@HiggsfieldAnimation — reported ~46-minute tutorial; verify exact video and duration.
- S5 candidate Full Project: https://higgsfield.ai/zh/@higgsfield.studio/projects/passport-rush — actual asset/prompt export and license NOT_RUN. Public visibility is not a grant for copying/commercial redistribution.
- S6 third-party archive: https://github.com/YIJUEYIJUE/higgsfield-film-prompts/tree/main/PASSPORT_RUSH — reported 1,193 unique prompts (302 image, 891 video); verify revision/count, missing media, provenance, license. Not official complete export.
- S7 third-party workflow notes: https://github.com/az9713/ai-animation-workflow-guide — verify and distinguish notes from creator-confirmed decisions.
- S8 official model announcement candidate: https://higgsfield.ai/announcing-magi-2 — verify original announcement/spec discrepancy before claiming.
- S9 official skills: https://github.com/higgsfield-ai/skills ; existing Studio vendor snapshot v0.14.0 commit 27000402070db19d958789d05b3b52b6f4718d7c MIT as described in Studio README. Follow skills/UPSTREAM.md; don't update automatically.
- S10 original official festival winners: https://higgsfield.ai/contests/higgsfield-global-film-festival?tab=winners — separate reference corpus, not necessarily open-source creator prompts.
- N1 private Notion exact title: Higgsfield 電影風格逆向｜100 個開源 Prompt / Skills 與 14 部得獎作品（2026-11-23）. Read-only connector result observed, includes 2026-11-25 ranking/分流. 100 files across 7 repos not 100 award-winning creators. 14 films are separate reference corpus; preserve original numbering. New priority REA-Video, Open Edits, Reverse Engineer Any Video, MiniMax H3 Reverse, Novoads, Reanimate, Capsule Cinema (downstream), plus other admitted alternatives; LunarXuan video HOLD per N3. Original 46–62 cinematic reverse DNA is baseline; no quality winner from docs alone.
- N2 private Notion exact title: Higgsfield × 當代藝術｜100 項開源 Skills、Prompt Libraries 與藝術風格參考（2026-11-23）. Read-only result observed; 20 Skills, 16 competition projects, 4 prompt libraries, 60 artist cards; 2026-11-25 re-ranking. Artwork-only -> Shot-only -> merged independent QC. Artist card is not artist-authored skill. Dedicated permissive artwork-level reverse method remains gap. Original #5–10,12–13 candidates; source-specific license checks apply; website design is not art Oracle.
- N3 private Notion exact title: Reverse Skill Engineering｜46 項逆向工程 Skills × Universal Main Session × Skill Distillation（2026-11-25）. Read-only result observed: 46 repo metadata checks, 34 MIT/Apache initial candidates, 4 BLOCK, 8 HOLD; not production whitelist. Preserve complete source original rankings and dispositions. Authorized search by exact title; no private URL copied. Soodles fixed domain admission is operational authority; Notion is research ranking.
- N4 private historical P1 blind-review report: 2026-11-23, benchmark v2, niobium617 vs unimage gap 0.104 vs preregistered 0.25. Resolve via authorized Drive/owner, not public link. Preserve actual original report, raw rating table, mapping, metadata and uncertainty (see §8). This file does not duplicate private rows or claim their reread.
- N5 private S13 rerun assets/receipts: B1-rerun and B2-rerun manually submitted 2026-11-24 15:08 / 15:10 Taipei time. Resolve with owner by J4/S13/reruns identifiers. Private paths and hashes not invented. Original B1/B2 11/23 18:37/18:38 remain UNKNOWN.
- Original Studio 79-creator inventory and scope: fixed baseline research/creators.json, creators.csv, profiles_raw.json, prompt_libraries.json, creators/index.md and creators/study-queue.md, research/reverse-skill-benchmark/v2/CREATIVE_RESEARCH_SCOPE.md. Preserve all named works and reference obligations; ten-person queue not full inventory. Prior J4 original canonical/prompt sources pinned in §8. If earlier chat/attachment unavailable, mark coverage_gap/MISSING_SOURCE rather than inventing or skipping.

Rights: source access, download, private analysis, third-party transfer, derivative creation, publication and commercial reuse are distinct. Record rights holder, evidence, allowed operations, expiry if any; no access-control bypass. Acquisition for own/authorized source only in accordance with platform terms; if official export or owner-provided file is available use that. Read-only inspection of project metadata allowed only under actual access; no claim that public project contains every prompt or that all assets are open licensed. All new external effect requires HF-Q05 GO, then specific rights and budget. No login/session cookies or credentials published.

Candidate Mac acquisition recipe from prior design (NOT_RUN, audit actual yt-dlp distribution/dependencies first; FFmpeg only under HF-Q01 scoped external exception; never execute unreviewed installer on production machine). Use approved versions, approved directory; commands below illustrative after authorization, not a current action:

```sh
brew install ffmpeg
uv tool install yt-dlp
SOURCE_ID=onNBysMf9WM
SOURCE_DIR="<authorized-local-asset-root>/sources/$SOURCE_ID"
mkdir -p "$SOURCE_DIR"
yt-dlp --no-playlist --write-info-json --write-description --write-thumbnail \
  --write-subs --write-auto-subs --sub-langs "en.*,zh.*" -f "bv*+ba/b" \
  --merge-output-format mkv -o "$SOURCE_DIR/%(id)s.%(ext)s" \
  "https://www.youtube.com/watch?v=$SOURCE_ID"
cd "$SOURCE_DIR"
ffprobe -v quiet -print_format json -show_format -show_streams "$SOURCE_ID.mkv" > media-probe.json
find . -type f ! -name SHA256SUMS -exec shasum -a 256 {} \; > SHA256SUMS
```

Keep raw bytes, actual container/codec/timebase and caption source/version, hash all artifacts after finalization; do not overwrite source. Handle actual download extension, failure and partial artifacts; no fabricated hash or receipt. If permissions/network/format blocked, record exact error and legitimate alternate original source or owner-provided evidence, only hold dependent measures. Downloaded captions vs ASR are different sources.

## 4. Evidence-aligned reverse and Full Project

For each source, deliver full Reverse Evidence Pack: source-manifest.json; rights.json; SHA256SUMS; media-probe.json; VIDEO.md; transcript/; keyframes/; shots/; audio/; timeline.otio; reverse-ir.json; methodology.json; claims-evidence.jsonl; unknowns.json; failure-cases.jsonl; report.html. Store large files outside Git. Each claim includes source ID, version, media hash, shot/timecode/frame/audio locator, observation, inference, alternative explanation, unknowns, confidence/limits, verified creator statement if available, reviewer and status. Keep SOURCE_EVIDENCE / MEASURED / INFERRED / UNVERIFIED_CLAIM (and explicit UNKNOWN). A frame doesn't reveal exact lens/focal length/seed/prompt/actual camera path or model parameters by itself. Don't infer protected identity or copy exact source style compositions. No output judged solely on pretty pictures.

Analyze across story structure, script/acting, mise-en-scène, blocking, shot boundaries/durations, scale, composition, depth, lens as hypothesis, light/material/palette, motion/optical flow, camera geometry, animation/physics, state continuity, cut rhythm, transitions, sound/music/dialogue/silence, audio-visual sync, grade and post. Measure when possible; missing actual data = NOT_RUN, not guesses. Use timestamp-anchored evidence/shot IDs, uncertainty and negative cases. Artist research: observable object relations, materials, perception/illusion, space and time, process, source interviews and alternate interpretations, not artist-name tags or visual adjectives. Art mechanism must compile to physical operations with observable effect.

Passport Rush study: align official final film + breakdown + Full Project readback (source placements, Elements, actual prompts/settings, versions, media, timeline revisions); establish chronology, failure takes, decision reason, alternatives and differences between proposed and actual method. With read-only authorized project metadata, use placement ID for prompt/source and saved Editing Room revision for sequence; do not create/upload/render to read. Preserve 20 production domains:
Story (motivation/structure), Script (dialogue/comedy rhythm), Storyboard (handcrafted 2D blocking), Art Direction (visual grammar), Character (identity/proportions), Character Motion (turnarounds/motion sheets), Environment (space), Props (state/continuity), Elements (named reusable refs), Layout (blocking), Previs (Blender greybox/animation), Camera (path/shot/lens), Performance (expressions/subtle gestures), Physics (collision/gravity/object motion), Prompt (model-specific compilation), Generation (model choices/retries), Continuity (cross-shot), Editorial (rhythm/timeline), Sound & Color (post), Production (budget/scheduling/failures/delivery). Research both successes and failures, not only final prompts. Claims that every prompt/asset is public, hybrid pipeline first film, official Blender plugin features and tutorial duration remain claims to verify.

Use Passport Rush as benchmark, not fixed template or content to duplicate:
A = final film only (blind reverse), B = film + official breakdown (decision understanding), C = film + Full Project (project reverse). Separate independent evaluator holds actual evidence; don't give A full-project answers; avoid leakage across sessions and labels, compare overlapping criteria fairly while distinguishing information advantage. If material absent, mark that group incomplete; no invented ground truth. Study S1 independently even if same topic later established. New original work is holdout, not copy. Reference/production assets cannot be used to cheat evaluation.

## 5. Candidate tools, license admission, universal reverse and distillation

Prior proposed S/A/B ordering is architecture relevance only (NOT_RUN). Complete original shortlist retained:
| Rank | Candidate | Prior repo-level license claim / purpose |
|---|---|---|
| S | https://github.com/JuneYaooo/rea-video | Apache-2.0; film reverse, VIDEO.md/HTML |
| S | https://github.com/heygen-com/hyperframes | Apache-2.0 candidate; agent-native video, HTML/CSS/JS editing/render, reverse, style sampling, captions/motion |
| S | https://github.com/sybil-solutions/skill-distill | MIT; reference/session -> skill |
| S | https://github.com/AcademySoftwareFoundation/OpenTimelineIO | Apache-2.0; Editorial IR |
| S | https://github.com/yt-dlp/yt-dlp | Unlicense source claim; actual distribution/deps differ, audit |
| S | https://github.com/Breakthrough/PySceneDetect | BSD-3; cuts |
| S | https://github.com/QwenLM/Qwen3-VL | Apache-2.0 candidate; model/weights and deps separately |
| A | https://github.com/FireRedTeam/FireRed-OpenStoryline | Apache-2.0 initial claim; semantic editorial decision, not director replacement |
| A | https://github.com/kevinbadi/open-edits | MIT; edit style |
| A | https://github.com/openai/whisper | MIT; speech timecodes; deps audit |
| A | https://github.com/JuneYaooo/teacher-to-skills | Apache-2.0; expert method |
| A | https://github.com/imMamdouhaboammar/repo-to-skill | MIT; project methodology |
| A | https://github.com/juxt/allium | MIT; behavior/spec extraction |
| A | https://github.com/JuneYaooo/capsule-cinema | Apache-2.0; downstream recipe |
| A | https://github.com/Wan-Video/Wan2.2 | Apache-2.0 code claim; weights separately |
| A | https://github.com/huggingface/diffusers | Apache-2.0; GPU runtime |
| A | https://github.com/opencv/opencv | Apache-2.0; optical flow/forensics |
| A | https://github.com/librosa/librosa | ISC; sound/rhythm |
| A | https://github.com/PyAV-Org/PyAV | BSD-3; FFmpeg dependency requires separate review |
| B | https://github.com/NiazMorshed2007/reanimate | MIT initial claim; motion reconstruction |

Other original N1/N2/N3 candidates retained by exact authorized source, with important explicit distinctions: lisn0/reverse-engineer-any-video (MIT), gnipbao/minimax-h3-video-reverse-skill (MIT), novoads/agent-skills analyze-video (MIT), luozhilzh/video-prompt-reverse (MIT), wocha-xiaoli/video-shot-analysis-feishu (MIT), eruto-skills/analyze-video (MIT research alternative), WuDao0123/taste-skill (MIT metadata, website-only/cross-domain HOLD for art), corpus-to-skill and skills-evolve (MIT), PyDriller (Apache-2.0), Waza (MIT existing check), graphify (Apache-2.0). Caph-dev, unimage, niobium617 are historic benchmark candidates, not automatically admitted. Existing OSideMedia prompt suite reference only per Studio README; not vendored. BLOCK: LunarXuan/image-prompt-reverse GPL-3.0; OpenMontage AGPL-3.0 claim; ComfyUI GPL-3.0 claim; PM4Py, Code Maat, ALKYH/skill-distillation per N3. HOLD: LunarXuan/video-prompt-reverse (license absent), senlindesign/taste-skill, others per exact N3; Remotion special license not default; WanGP dependency/weights pending; audio analyzers and dedicated contemporary-art reverse gap. Blender GPL and FFmpeg LGPL/GPL (actual build) allowed only as independently approved external tools under Q01. Commercial Higgsfield/Antigravity/Colab service is not open-source core. MAGI-2 hosted only unless actual weights+terms verified; don't claim local deploy. REA-Video audio separation weight reported CC BY-SA 4.0; hold unadmitted weight/deps, no inference that Apache repo covers it.

For each candidate: exact upstream commit, file paths, LICENSE/NOTICE blob/hash/SPDX/full terms, actual target artifacts/dependency lock/SBOM, plugin/install hooks/scripts, network/data scope, model weights, bundled assets and output rights, obligations, date, reviewer, scoped ALLOW/HOLD/BLOCK. MIT/Apache/BSD/ISC etc only after actual applicable checks; no source-available, NC/ND, strong/weak copyleft in core; no laundering via wrapper or distillation. Q01 does not auto-approve FFmpeg-dependent upstream tools. For strict Reverse Route respect exact Soodles admitted subset; if additional capability needed, use separately approved Studio-specific adapter after GO, do not widen or rewrite shared global route. Candidate selection filters rights/availability/capability then ranking; manually selectable within approved scope; changes versioned with independent tests.

Fixed current Soodles source operational limits: skills/reverse-route/routes/domain-selection.md, library/安裝來源.md, library/高階方法准入.md, library/統一蒸餾架構.md and routes/higgsfield-studio.md at baseline Soodles commit in §11. REA-Video pinned 8b40ef79beffa4d9a9a8c5e407c64ba11192063c taxonomy and existing classification only; Open Edits 7fbd74651ea945711792b207e8a9f0a167f78132 Step 2/4 existing cuts; reverse-engineer-any-video 0fd2162e435a4c373b173b86e2e27cb4be5f7134 Step 3/Labels/evidence reading; MiniMax H3 2fd1cc182606b81b69e0a9dca31c6cc7c2e973af factual narrative only; Novoads 82e6d0628d848d36fcf441549d7d77c7b399396e Step 4–5; Reanimate 3f7a55a2986a84ca2173e86ee9127eefe31d046d Step 3 analysis; luozhilzh c14f99784f01eacfd22c6a90f3719ed318f04ba1 Step 0–1 references; Feishu 943f960300111758023b2da2b6802e68642ce9a0 local table only; Teacher-to-Skills 0ca966c83044d36eee1103861b7e7e64dd5787bf source/provenance/invariants; Sybil skill-distill 4c3b307096aea36ecd6cffddf52d1b415cf63d68 sections 3/6/8 only, native runner NOT_RUN. Exact file sets/limits in source; no running media extraction, new measurements, external generation or plugins merely because text admitted. Soodles current route explicitly excludes FFmpeg-dependent routes; Q01 scoped exception requires separate Studio path and review. Prior suggested commands 'codex plugin marketplace add JuneYaooo/rea-video', 'codex plugin add rea-video@rea-video', 'npx skills add heygen-com/hyperframes' are NOT_RUN, unapproved until pinned/audited/authorized. HyperFrames proposed skills: /hyperframes, /hyperframes-cli, /hyperframes-registry, /media-use, /reverse-any-video, /style-sampling; verify actual revision/support, don't assume installed.

Universal approach:
source discovery -> License Admission -> select minimal legal skill combination -> Main Session (Thinking × Ambitious / Ponytail) -> independent Reference Eval -> selectable distillation -> fresh Student & holdout -> Skill Composition with Eval -> Harness² + original Oracle -> human approval -> Freeze/Version/Reuse.
Use REA, HyperFrames, teacher-to-skills, repo-to-skill, Sybil or another approved approach as configurable capabilities, never baked into core or ranked without tests. Keep provider-neutral methodology and source refs, separate from model-specific prompt. If only analysis is required don't create a skill gratuitously. If Reference not independently verified, candidate only; don't distill from unapproved content. Source extraction may be ChatGPT Main Session, repo, film, interview, art, permitted trace. Session parser/Strata/native wiring NOT_RUN. Original method three fresh trials per version where authorized; budget and original stops govern. Comparison: no Skill vs original source/summary vs candidate; same clean start, tools/model/budget, first attempt, independent Observer with expected answers kept separate. Test same task, unseen transfer, negative cases, ablation, composition (fresh Composer then fresh Worker when needed), regression. Formal holdout never used for training/tuning. Original Soodles fixed 10-case Skill Composition experiment remains separate, don't reuse labels/score. Use source-specific independent Oracle; no self-eval substitution.

Creative method abstraction levels L0 artwork (rights), L1 observations, L2 artistic mechanism, L3 reusable methodology, L4 executable skill, L5 project-specific Shot IR, L6 provider prompt (recompile), L7 actual result (project-specific). Extract trigger, preconditions, exclusions, observation, decision, rationale, physical operation, invariants, effect, failure patterns, negative examples, evidence and exit. Skill contract candidate:
```yaml
skill:
  id: creative-method
  version: 0.1.0
  domain: configurable
  source: {evidence_refs: [], license_status: HOLD}
  applicability: {triggers: [], preconditions: [], exclusions: []}
  methodology: {observations: [], decisions: [], rationales: [], operations: [], failure_patterns: []}
  compilation: {input_schema: null, output_schema: null, provider_independent: true}
  verification: {reference_oracle: null, holdout_cases: [], regression_cases: [], status: NOT_RUN}
  promotion: {human_approval: required}
```
Never embed answer or protected original asset in skill. Store complete evidence for review. Source-bound method can choose different reverse approaches per domain and manually or automatically select from admitted methods. Ranking updates only after preregistered independent comparisons, not marketing claim or vendor win rate.

## 6. Architecture, schema, assets, editorial and review

Retain existing Studio baseline README, projects/_template, skills, prompts, research, budget, templates, J4 and benchmark paths. Incremental architecture: Source/Evidence -> Universal Reverse -> Creative Methodology/Registry -> Project/Art Direction/Elements -> Scene/Shot/Prompt Compiler + Blender Previs -> provider/GPU runtime -> editorial/post -> independent QC -> human approval/freeze/reuse -> feedback into registry. Proposed twenty responsibility boundaries (not 20 processes):
1. SourceManager: URL, download, rights, immutable raw evidence.
2. EvidenceManager: keyframes, transcript, sound, timecodes and provenance.
3. ReverseManager: film/artwork/project/audio reverse strategy.
4. MethodologyManager: methodology, Teacher/Student distillation.
5. SkillRegistry: license, pinned versions, ranking, capabilities and promotion.
6. ProjectManager: full project schema, scope/version and dependencies.
7. ArtDirectionManager: artistic rules/mechanism and constraints.
8. ElementsManager: character/location/prop/material/audio/previs identity, versions, usage references.
9. StoryManager: script, narrative state, continuity of intent.
10. CharacterManager: identity, wardrobe, performance.
11. SceneManager: space, objects, environment.
12. PrevisManager: Blender greybox, animation, camera path, blocking and temporal control.
13. ShotCompiler: provider-neutral Shot IR -> capability-valid model prompt, evidence/canonical constraints.
14. ProviderManager: MAGI-2, Colab, other models/adapters, selection and actual receipts.
15. GPUManager: authorized job/capacity/reclaim via existing Soodles owner, not duplicate scheduler.
16. EditorialManager: OTIO timeline and cuts/transitions.
17. PostProductionManager: sound/color/composite/exports.
18. EvalsManager: independent Oracle, blind evals, regression and calibration.
19. BudgetManager: Credits/CU/GPU costs, caps, preserve existing ledger.
20. KnowledgeManager: Git/Notion/Drive/local evidence and cumulative reusable methods.

Candidate path layout (implementation not created; prefer existing interfaces):
```text
projects/_template/ ; projects/j4-async-succession/  # preserve
research/reverse-skill-benchmark/ ; research/passport-rush/ ; research/source-manifests/
studio/{managers,reverse,distillation,compiler,providers,editorial,runtime}/
schemas/{source,evidence,methodology,skill,project,element,shot,evaluation}.schema.json
skills/{reverse-route,creative-method-distill,production-route,vendor}/
registry/{reverse-skills,creative-methods,providers,licenses}.yaml
evals/{fixtures,oracles,holdout,regressions}/
web/ ; budget/ ; docs/{architecture,handoff}/
```
Do not instantiate all directories solely for visual architecture; responsibility and future scope retained. A single CLI/shared state initially; no duplicate Soodles orchestration. Proposed DuckDB local query index only if needed; Git stores permitted code/contracts/metadata/eval evidence; Notion creator/art/film knowledge indices; Google Drive or controlled local source library original media/Blender/audio/renders; Mac work cache/proxies; Higgsfield actual Elements and provider receipts. URI/opaque logical ID + SHA-256, version, rights, owner and resolution; avoid duplicating big media across worktrees. Use actual storage availability, never assume cross-provider upload permission. No private locators/large media in public Git.

Full Project schema candidate:
```yaml
project:
  id: original-film
  schema_version: 1
  creative_direction: {methodology_refs: [], artwork_refs: [], film_refs: []}
  reverse_pipeline: {strategy: capability_router, candidates: [], approved_skills: []}
  elements: {characters: [], environments: [], props: [], materials: [], audio: [], previs: []}
  production: {scenes: [], shots: [], timeline_ref: null}
  providers: {preferred: higgsfield, fallbacks: [], model_selection: dynamic}
  verification: {artwork_only: NOT_RUN, shot_only: NOT_RUN, composition: NOT_RUN, continuity: NOT_RUN, final_cut: NOT_RUN}
```
Schema must remain extensible by actual need. Storyboard/ArtDirection/Elements precede per-shot compilation. Shot IR includes scene ID, action beat/state before/after, timing/timebase, object relations, framing, camera, light/material, audio cue, forbidden outcomes, evidence and artistic mechanism refs, continuity locks, approved Elements versions and actual provider inputs. Blender provides editable spatial geometry, character blocking, camera path, timing, object locations, keyframes, light direction; AI provides materials, appearance, cinematic look, dynamic details, temporal frames. Handcrafted 2D storyboard + 3D previs + AI animation; manual adjustment and regenerate rough shot where capability exists. Need actual native readback of scene/camera/animation/render; no claims of plugin features beyond verified surface. Prior proposal Blender plugin includes Scene Builder, Camera, Animation, 3D Model, Image, Video, Asset; verify actual version/tool. Compile capability-checked provider-specific prompt from neutral IR; reject invalid input combinations, no silently dropping lock constraints. Store exact compiled bytes, hashes, inputs, settings, provider receipt, full failures.

Editorial: OpenTimelineIO canonical interchange for clips/tracks/timebases/cut points, source range and media references; actual editor handles unsupported OTIO effects with explicit mappings and roundtrip checks. HyperFrames candidate HTML/CSS/JS rendered video, preview, motion/text overlays, subtitles; FireRed OpenStoryline candidate editorial suggestions; Open Edits style rules from measured evidence. Verify deterministic render claim in actual environment; test source/record ranges, frame count, A/V sync, transitions, audio, color, deliverables. Model output not finished cut. Medium Compiler existing project integration (https://github.com/ed3c/medium-compiler) for local playable acceptance: original film (authorized), frames/timestamps, storyboard, Blender previs, generation outputs, side-by-side evidence/ratings, editable timeline, actual prompt, Elements, failures and budget. Private media via local authorized references only; no public hosting assumed. Browser playback is not proof of editing/quality PASS.

## 7. Runtime/provider, MAGI-2 and cost

Codex CLI = primary engineering/agent session, compiler/tests/git; Antigravity = alternative agent research/GPU workflow; Colab = open-model inference/video/vision; Higgsfield MCP = hosted image/video/Elements/editing; Higgsfield GPU = actual rentable GPU compute if admitted; Mac = local analysis/previs/edit/cache incl MLX where compatible; Soodles = existing orchestration, state and Evals, Noodle/LoopManager as applicable after GO. Separate Agent runner, provider, worker and media format adapters. Shared job identity and state manifest, original Owner readback, no hidden duplicate effects. Do not assume current network/API/local execution capabilities. For paid service, verify quote, cap, actual balance/receipt before promotion, handle unknown effect by readback before retry; if remote GPU cannot be reached, retain independent tasks. No API key or credentials in Git. Colab runtime availability/terms, quota/session lifetime and actual model compatibility check required; no assumed H100 or G4 capacity. Higgsfield GPU and hosted model are distinct billing/resources.

Observed read-only Higgsfield models_search in prior conversation: provider Sand AI, model ID magi_2, duration integer 4–30 default 5, 1080p only; aspect ratios 21:9,16:9,4:3,1:1,3:4,9:16; generate_audio default true, enhance_prompt default false, seed optional integer 0..4294967295; start_image first frame cannot combine reference mode, end_image requires start_image; image_references max 10; video_references max 5, each 2–30 sec and total <=30 sec; audio_references max 5, each 2–30 sec and total <=30 sec. Catalog metadata media type may be generic; inspect actual schema before generation. Seed capability does not guarantee deterministic backend. No observed MAGI-2 unlimited free generation entitlement, no actual price returned in that catalog read. Catalog read != provider native generation. Verify fresh read and supported modes. Preserve model-independent IR and reference roles.

Reported original publicity: 2026-11-25 announcement; $0.08 per generated second, 480B total / ~28B active as user quoted; prior assistant reported official blog 400B vs social post 480B, 1080p/25fps, up to 30s and 20 references. These claims/conflict need authoritative current confirmation. Vendor Video Arena reported Nov24 internal wins vs Seedance 2.5 39%, Seedance 2.0 71%, Wan 3.0 79%, Kling 4.0 83%, MiniMax H3 83%; not independent evaluation, verify source and metric; not ranking guarantee. Weight availability and commercial rights not established; model hosted via Higgsfield only on current evidence; no claim that it's open source. Pricing estimate = target seconds * average takes * (1 + extra generation ratio) * 0.08 USD; e.g. 90s * 3 * 1.2 = 324 generated seconds, $25.92 advertised estimate. Not account credit quote, excludes images/upscale/render/rental/post. Actual billing provider receipt and approved max required.

Existing budget baseline README and budget/allocation.csv, ledger.csv, track.py, plan/monthly-usage-and-content-strategy.md. Historical plan 9,000 monthly credits split methodology 2520/daily 2250/trends 1980/retry 1620/rnd 630; 80% warning/exit 2 stops new finals. Historical plan not current balance. Do not repurpose retry bucket or assume subscription entitlement. Zero-credit P1/S13 protocols separate (website only); MCP/CLI/Canvas/Supercomputer generally charged per original protocol. Current route quote/eligibility read separately; no automatic paid fallback. No spend in handoff.

## 8. Existing evidence and original Oracle preservation

Original artifacts (do not duplicate/overwrite): at Studio baseline, research/reverse-skill-benchmark/v2/BENCHMARK_SPEC_V2.md (blob 339a577baf6ce262fa91f08defd7922160f02a87), manifest_v2.json, EXECUTION_PROMPT.md, REPORT_TEMPLATE.md, ratings/generations/prompts templates, validate_spec.py, CREATIVE_RESEARCH_SCOPE.md (blob 4c4fa58b1751d4ee5c370784bda13034e1b982c6), DOT_HANDOFF.md; v1 records in parent. Original Draft PR #4 https://github.com/ed3c/higgsfield-studio/pull/4. P1 N4 private actual report remains separate from Git spec state: reported INCONCLUSIVE 2026-11-23 niobium617–unimage gap 0.104 < 0.25 pre-registered threshold, original ratings/metadata to retrieve, missing samples and two independent reviewer independence unverified. Do not proclaim winner, don't upgrade partial/inconclusive with spec or new method. Preserve previous unimage/caph/niobium617 candidates. Existing source pack remains BLOCKED_ENTITLEMENT_RECHECK/NOT_RUN for its recorded scope; distinguish actual historical report and raw evidence missing rather than resetting it. Original P0 lock identical input/analysis budget, deterministic normalization only/no human polishing, exact prompt hashes; P1 3 refs x 3 skills x 2 = 18 text-only reconstruction; P2 3 x 2 x 2 = 12 style transfer Caph + eligible highest non-Caph P1, new subject pre-fixed, no source image attached to render, no global 3-way conclusion; optional P3 6 cross-model, P4 repair separate. No silent replacement, selection of best takes or pooling models. Previously discussed 12-image two-Skill vs 18-image three-Skill followup candidates, not authorization or new result. Original P1 weighted 0–5 rubric composition .25 perspective .20 lighting .15 palette .10 material .15 artifact_control .15; P2 style_dna .25 new_subject_integrity .25 composition .15 lighting .15 palette .10 artifact_control .10. Hard fails major geometry/anatomy unrelated, protected copied identity P2, watermark/text leakage. Two independent human reviewers, sealed shuffled blind IDs, disagreement >2 criterion adjudication retain both original scores, weighted mean per reviewer/image then case/replicate and 3-case mean, report paired differences, no statistical significance claim from 3 cases, hard-fail rates separate. Keep existing original Gate labels and exact scoring spec. No new film Oracle replaces this one. Website entitlement fresh Unlimited ON and 0 Credits each exact submission, before/after balance, serial random/declared order, no paid retry; screenshot unlabeled Nov20 cannot infer expiry/activation, fresh confirmation. Model GPT Image 2.6 not Flare 1K 16:9 as original spec, fallback separate run only. Actual image bytes, settings/run IDs or not_exposed, hashes, all samples and labels; no fabricated scores.

J4 ASYNC: SUCCESSION (90s/25 shots; historical project plan: Act I 0:00–0:20, II 0:20–1:05 with 1:03.7–1:05 black, III 1:05–1:30; original locked roles JACKET/STEWARD/MARCHER/COMPANION/WEAVERS etc; actual exact contract from owner/canonical). Six-image prior failure: pretty conceptual illustration rather than contemporary-art operation; nouns retained but optical illusion, state transition, temporal memory, object/space constraints lost; not established root cause without submission history. Preserve original art-mechanism/Shot IR/Optical IR and original independent gates. Existing J4-S13-Dot-Handoff.md baseline blob a1fc9649e82d2590b532aa20c424bfbfac00540c, original canonical and G2 links there:
https://github.com/ed3c/higgsfield-studio/blob/e5b4c4157de7c275c712b294e7d5c5fdb9626160/projects/j4-async-succession/archive/v2_6/j4_shots.json
https://github.com/ed3c/higgsfield-studio/blob/e5b4c4157de7c275c712b294e7d5c5fdb9626160/projects/j4-async-succession/contracts/art_mechanism_v4_1.json
https://github.com/ed3c/higgsfield-studio/blob/e5b4c4157de7c275c712b294e7d5c5fdb9626160/docs/G2_EVIDENCE_GATE_V4_2.md
Draft PR #3 https://github.com/ed3c/higgsfield-studio/pull/3 . Exact A/B original prompts in handoff with SHA A 39d59539817efd090cf14a3841cdd7e7f97c9183e21d0dbda36d103f989d74a2, B 36fd1932be3b2c6b60cc7f546c2b3c3081365f14930fbc73fc0e5e1b5060ebd4, compiler payload 4588779e43bf6de0f1a436eddb9b01515e6b77f8c04b809b01749056000efb11. Do not retype or normalize those prompts; use exact source. S13 1.2–2.4s contact still, A1/B1/A2/B2 fixed model/settings 9:16/no ref, paired seeds if available, canonical negative; five original P0: indoor lab incl sea outside high windows; localized lower wood salt damage intact piano; single finger/one key contact; small wafer/physical light reflection; beach piano forbidden. Original six-grid outdoor piano historical cause UNKNOWN. Original B1/B2 receipts/assets UNKNOWN; manual reruns only visual diagnosis, not original proof. v4.2 official receipt and two independent human reviewers still required. Preserve original negative conditions, actual original media, original prompt hashes and all failure history. S13 and prior benchmark not reopened by new handoff. No status changes from mere publication or new methods.

New production artwork-only / shot-only / composition test is a separate preregistered protocol; inherited old six-dimension >=7/mean>=8 where applicable must use original versioned J4 oracle, not casually import threshold into new unrelated experiment. Calibrate new oracle separately; independent visual reviewers (two humans for formal artistic acceptance as prior constraint), human final approval; distinguish artwork fidelity from reconstruction similarity, new subject integrity, original art mechanism and actual temporal causality.

## 9. Verification matrix / responsibility / stopping

All below new execution NOT_RUN. Main Supervisor fixes versions, conditions, budget, independent Observer and rubric before testing; expected labels reviewer-only. Domain owner evaluates product; provider owner actual readbacks; Harness² coordinates method acceptance, not substitute for native/product evidence. State transitions require actual evidence. Suggested test obligations (not arbitrary fixed metrics; exact numeric thresholds for NEW experiments preregister before trial, old thresholds preserved):
| Gate | Producer -> Consumer / independent Oracle | Positive / negative control / failure next |
|---|---|---|
| V0 Source & license | SourceManager + rights reviewer -> EvidenceManager/registry | Actual rights/version/bytes/sha & scoped admission; absent permission/unknown license/wrong identity reject, resolve with owner; not global hold |
| V1 Evidence | EvidenceManager -> ReverseManager / independent timestamps and source artifacts | Validate hash/timebase/cuts, align frames/audio; wrong timestamp/guess lens/prompt labeled fact reject; preserve unknown, re-extract only needed evidence |
| V2 Reverse | ReverseManager -> Methodology / independent S2–S5 original evidence, S1 observable evidence | A/B/C information isolation, scored evidence coverage and inference accuracy; leakage or missing original source no false pass; fix first gap |
| V3 Reference | Teacher/Main -> Supervisor / frozen independent reference oracle | One real reference succeeds, original method observable; negative control fails; no pretty-output-only claims |
| V4 Distillation/transfer | Teacher -> Fresh Student -> Observer | Clean first trial same task, holdout novel work, ablation, negative case, no answer leakage; original/summary/no-skill controls; failure compare earliest source/load/consumer/oracle/host |
| V5 Composition | Fresh Composer -> Fresh Worker / separate observer | Preserve each scope/negative/invariant, measure source selection and worker behavior; dropped constraints or incompatible skills reject; use single source-bound delta |
| G1 Artwork Fidelity | ArtDirectionManager -> independent human reviewer | Observable material/space/perception/time artistic operation with evidence, not artist/style keyword; wrong mechanism hard fail |
| G2 Shot Fidelity | ShotCompiler -> independent reviewer | Shot-only action, framing, narrative, identity/state; object misrelation or forbidden condition reject |
| G3 Composition Fidelity | merged IR -> reviewer | Artwork-only + shot-only independently accepted BEFORE combined render; both hold after merge; reject loss of either |
| G4 Temporal Consistency | Provider/Previs -> independent frame/time reviewer | Actual temporal physics/identity/spatial/state continuity, start/end/beat; morphing or wrong transition reject |
| G5 Editorial Quality | Editorial/Post -> independent playback/timeline/audio reviewer | OTIO source ranges/timebase, actual cuts/rhythm/story/A-V, source and output playback, no missing or corrupt frames/audio |
| G6 Methodology Transfer | Registry -> new independent original project | Different subject/scene/work, valid trigger, holds invariant and effect, negative case; no copied reference or memorized answer |
| G7 Production Reproducibility | Runtime/Budget -> independent owner | exact manifest, seed if supported, asset/source versions/hashes, provider receipts, costs, retries, all takes, reproducible editor/preview; unknown receipt or stale rights blocks affected claim |
| V6 Integration | Codex/Antigravity/Colab/Higgsfield/Local adapters -> original runtime owner | actual supported calls, authorization, input/output/unknown effect guards, tested reject paths and recovery, real playback UI; native integration NOT_RUN until actual observation |
| V7 Landing | Main -> human owner/registry | original acceptance + independent reviewer readback + approved freeze/version; no PASS based only on docs, candidate commit, mock, model self-review or unit tests |
| V8 Benefit | Harness² -> independent comparator | matched budgets/models/tools, actual comparative quality/time/cost, no conflating source/native/product/benefit results; inconclusive if evidence insufficient |

Verification state vocabulary: NOT_RUN, BLOCKED/HOLD with reason+owner+next, UNKNOWN for uncertain observed effect (read back same request, not replay), INCONCLUSIVE when observed data cannot discriminate, PASS/FAIL only for exact verified scope. Keep Frozen identities and original failed attempts. Bounded Convergence: cap retries/budget per approved trial; same issue three failed corrections re-examine cause and alternate explanations, not rename/reset. One variable changed when isolating a failure. No blind extra generations, no indefinite expansion, no paid escalation/fallback without approval. Human final artistic/production approval before promote; no automatic source publication. Freeze method version, original source, run settings, results and regression; new version for changes. Original product, native adoption, and comparative improvement each require their own evidence. Parent Goal remains open until H01–H32 actual deliverables/acceptance (or explicit owner revised scope); partial PASS never full completion.

## 10. Minimal path and full frontier

After fresh explicit GO:
1. Verify current Studio and Soodles HEADs, this exact handoff and original constraints; resolve N1–N5 privately, read exact source/contracts by need, keep all original scope and latest accepted decision. Check access/rights for S1 and S2–S5. Collect permitted independent artifacts; separate source tracks; if missing record owner/next. Confirm no existing running/frozen conflicting task before any effect.
2. Source admission -> evidence pack for first available legitimate source (but both sources required). Compare minimal admitted reverse methods: prior proposal REA-Video vs HyperFrames reverse vs existing film baseline, not all tools simultaneously; for new execution ensure each independently admitted and common evidence. Reference Oracle prepared before evaluation. Complete all shot/film/art/project obligations incrementally; no pretending unmeasured results.
3. Distill one verified transferable methodology (choose appropriate method/manual or router). Independent same-task, holdout, negative/ablation and composition as warranted. Registry version candidate.
4. Use original character, environment, objects, movement; Elements-first plus artwork-only and shot-only; Blender previs for physical controllability. Verify source/asset rights; generate only authorized tests. First slice suggestion three shots (character performance/spatial camera/art mechanism), not complete Passport Rush remake.
5. Compile provider-independent shot into capability-specific prompts; compare authorized MAGI-2 vs admitted Colab open model where meaningful and budget approved; provider-specific receipts, actual cost. Don't require both to proceed with independent no-cost work. Keep dynamic/manual selection but freeze run.
6. Edit OTIO + HyperFrames/approved actual tool, audio/color, local Medium Compiler playback/inspection. Independent visual/audio/editorial gates, negative controls and actual readback. Correct first causal break, regression. Human approval then freeze/reuse on a novel work.
7. Review entire H01–H32 frontier, fill named missing managers/adapters/coverage from actual needs, no spurious services. Keep separate required H01/S1, H03/S5 and all Notion research original indices; complete full product beyond first vertical slice. No auto-start background work merely from this doc.

## 11. Suggested Skills / exact upstream method sources

Use Soodles source at fixed 939875f91a8d6d38853989b5bd3a8a497a06bf88; fetch original paths, not copied modified instructions. If a fresher version changes scope/semantics, compare and record before adoption. Call actual skill tool where available, otherwise explicitly read source and distinguish NOT_RUN native use.
- AGENTS.md, relevant AGENTS.reference.md; .agents/skills/handoff/SKILL.md (upstream TMP default overridden solely by user-directed public-safe Git handoff); .agents/skills/thinking-router/SKILL.md, references/dual-brain-model.md, references/intent-handoff.md, references/loop-execution.md; contracts/thinking-route-process.md; contracts/state-machine-change.md (semantic preservation, four-way classification).
- .agents/skills/ambitious-route/SKILL.md (single outcome-improvement entry), .agents/skills/ponytail/SKILL.md and .agents/skills/outer-review/SKILL.md (only for actual relevant candidate review); .agents/skills/neo-route/SKILL.md + references/neoweaver-heartbeat-prompt.md as applicable, not a new scheduler.
- skills/reverse-route/SKILL.md; routes/higgsfield-studio.md, routes/domain-selection.md, routes/engineering.md, routes/soodles.md; library/情境與領域排名.md, library/安裝來源.md, library/高階方法准入.md, library/統一蒸餾架構.md; use exact fixed subset as §5. Skill authoring: skills/codex-route/routes/skill-authoring.md (path as referenced by upstream; verify actual source).
- Skill Composition with Eval fixed candidate: https://github.com/ed3c/soodles/blob/37e41302e361249848e1013a7c8267ad3c1c33f0/.agents/skills/thinking-router/SKILL.md#思考對象skill-composition-with-eval ; source-bound Evals methods, .agents/skills/eval-audit/SKILL.md, Test Manager, error-discovery/write-code-evals if actual source/available; docs/pclass-harness-optimization-protocol.md, contracts/pclass-feedback-process.md, original Owner/Oracle; don't infer native validation.
- Studio skills/README.md, skills/UPSTREAM.md, skills/methodology-breakdown/SKILL.md, skills/image-reverse-benchmark/SKILL.md, skills/social-creator-intelligence/SKILL.md, skills/draft-to-final-upscale/SKILL.md and existing daily/trend skills; official Higgsfield generate/official references and Elements per current catalog; candidate tools from §5 only admitted scopes; Medium Compiler actual repo contract and playback acceptance.
- Soodles existing LESSONS and fixed known source cases for root cause/readback; formal-route or FactoryWeaver only if named actual gap, not default overhead. Preserve old Owner/Consumer/Oracle, exact digest/argv/next when real runtime binds them; do not invent worker/task IDs.

## 12. Completion and legal next

Read-only observations: three Notion research pages retrieved in previous turn; Studio and Soodles branch commits and relevant exact paths read; MAGI-2 model catalog capabilities read. Prior public-source links/tool claims from conversation retained as candidate source registry, not reverified in this handoff. No media bytes/Passport Rush full export, no native tests, no actual comparison, no license audit of every dependency, no paid operations. Current file is a design/decision handoff only. The committing session must read this exact file back at resulting commit and verify intended content, parent, changed path and main HEAD; report SHA/blob/readback, not claim product PASS. If commit response uncertain, read same path/branch before retry; do not overwrite another owner change. No ZIP. Private references intentionally resolved via authorized source titles, not publicly copied; if unreachable, record named coverage gaps.

Fresh session instruction (paste with commit-pinned link): Read the full handoff and its original source references, preserve H01–H32 and HF-Q01–HF-Q06=A, original Oracle and historical states. You are in WAIT_FOR_EXPLICIT_GO until user authorizes implementation. Once GO, perform the shortest legal real evidence-to-original-film closure per §10, incrementally deliver complete goal, independently verify each layer, keep unauthorized paid/remote/publication actions blocked. Only ask genuinely new decisions that change scope/implementation/authority/acceptance; resolve factual source/capability questions yourself where authorized. Report actual evidence, blockers and lawful next; do not claim source/skill/film/model/runner PASS from handoff alone. No new Worker or spend before authorization.

End of handoff.
