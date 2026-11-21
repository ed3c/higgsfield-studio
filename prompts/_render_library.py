#!/usr/bin/env python3
"""Render the original prompt library. Re-run after editing ENTRIES."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent

CINEMA = (
    "技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide"
    "（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。"
    "提示詞是原創模板，不是該文的範例腳本。"
)
FILM = (
    "製作順序來自 How to Master AI Filmmaking"
    "（https://higgsfield.ai/blog/how-to-master-ai-filmmaking）："
    "角色參考與空場景分開，再進影片。"
    "提示詞是原創模板。"
)
ENG = (
    "鏡頭詞彙對齊官方 skill higgsfield-generate 的 prompt-engineering.md"
    "（MIT，skills/vendor，v0.14.0）：主體、鏡頭、光線，image-to-video 只寫運動。"
    "提示詞是原創模板。"
)
COOK = (
    "行銷模式名稱來自官方 skills README 的 Marketing Studio 模式表（MIT，v0.14.0）。"
    "這是交給官方 higgsfield-generate 的 brief，不是手寫的後端提示詞。"
)
PLAN = "點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。"

ENTRIES: list[dict[str, str]] = [
    {
        "id": "art-sketch-materials",
        "title": "同一張素描的三種材質",
        "domain": "art",
        "model": "Soul Cinema",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "methodology",
        "learned": FILM,
        "placeholders": "`{sketch_subject}` 用創作者自己的素描主題，例如「一隻摺紙鶴」。不要畫受保護的角色。",
        "prompt": (
            "Vertical 9:16 still, three equal panels of the same {sketch_subject} drawn by one hand. "
            "Left panel: dry charcoal on warm paper. Middle panel: thin oil paint with visible brush ridges. "
            "Right panel: glazed ceramic relief of that same drawing. "
            "Same pose, same crop, soft north light, no text, no signature, no frame on the wall."
        ),
    },
    {
        "id": "art-pigment-macro",
        "title": "顏料切面",
        "domain": "art",
        "model": "Soul 2.0",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "daily-life",
        "learned": ENG,
        "placeholders": "`{pigment}` 用當天桌上真的有的顏色。",
        "prompt": (
            "Vertical 9:16 macro still of a cut stick of {pigment} pigment on a kitchen table. "
            "85mm, tack sharp at the broken edge, crumbs in the foreground, window light from screen left, "
            "the rest of the table falling soft. No labels, no brand names, no hands."
        ),
    },
    {
        "id": "art-color-script-trio",
        "title": "三張色彩腳本",
        "domain": "art",
        "model": "Nano Banana Pro",
        "settings": "2K",
        "credits": "2",
        "bucket": "methodology",
        "learned": FILM,
        "placeholders": "三張分開生成，`{place}` 同一地點。只在外觀鎖定後才進入 Seedance。",
        "prompt": (
            "Vertical 9:16 color-script still of {place}. Palette limited to cobalt, warm paper white, and one copper accent. "
            "Empty of people. Show the light direction clearly: a single practical lamp and a cool window. "
            "No readable signage, no logos. This frame is a lighting reference, not a poster."
        ),
    },
    {
        "id": "art-gallery-track",
        "title": "小展間橫移",
        "domain": "art",
        "model": "Wan 3.0",
        "settings": "5 秒，720p",
        "credits": "7.5",
        "bucket": "methodology",
        "learned": ENG,
        "placeholders": "用已鎖定的展間靜幀當 start image。提示詞不要重描述畫作內容。",
        "prompt": (
            "Slow lateral tracking shot along the wall, camera at eye height, constant speed. "
            "The frames drift through the shot one by one. Floor reflection moves with the camera. "
            "No new people enter. No whip, no zoom."
        ),
    },
    {
        "id": "fashion-mrt-lookbook",
        "title": "捷運穿搭定場",
        "domain": "fashion",
        "model": "Soul 2.0",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "daily-life",
        "learned": ENG,
        "placeholders": "`{garment}` 用今天真的穿出門的衣服。`{station}` 用站體結構，不要拍到可辨識的路人臉。",
        "prompt": (
            "Vertical 9:16 fashion still on a metro platform at {station}. "
            "The same person as the reference, wearing {garment}, one step forward as the train doors open behind them. "
            "85mm, eye level, shallow depth of field, cool fluorescent light plus one warm practical on the platform edge. "
            "Full body in frame. No logos, no readable ads, no crowd faces."
        ),
    },
    {
        "id": "fashion-night-market-cloth",
        "title": "夜市布料",
        "domain": "fashion",
        "model": "Soul Cinema",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "trends",
        "learned": CINEMA,
        "placeholders": "`{textile}` 用看得到織紋的布。趨勢片只用這張靜幀加一條 7.5 點的影片。",
        "prompt": (
            "Vertical 9:16 still of {textile} hanging in a night-market stall. "
            "Steam in the background, tungsten bulbs, the cloth catching a rim of light. "
            "Close enough to read the weave. No brand marks, no food logos, no readable prices."
        ),
    },
    {
        "id": "fashion-jewelry-macro",
        "title": "飾品靜物",
        "domain": "fashion",
        "model": "Nano Banana Pro",
        "settings": "2K",
        "credits": "2",
        "bucket": "daily-life",
        "learned": CINEMA,
        "placeholders": "只拍自己的飾品。官方產品攝影技能的後端提示詞不要手寫；這條是一般圖像模型用的靜物模板。",
        "prompt": (
            "Vertical 9:16 still life of {jewelry} on dark stone. "
            "Soft top light, a thin rim light separating the metal from the background, "
            "one reflection on the table, the right third of the frame left empty and dark. "
            "No text, no box logo, no fingers."
        ),
    },
    {
        "id": "fashion-runway-walk",
        "title": "五秒走步定稿",
        "domain": "fashion",
        "model": "Kling 4.0",
        "settings": "5 秒，1080p",
        "credits": "18.75",
        "bucket": "daily-life",
        "learned": ENG,
        "placeholders": "靜幀通過之後才用。image-to-video，不要重寫衣服。",
        "prompt": (
            "The person walks three steps toward camera and stops. "
            "Subtle dolly out to keep the full body in frame. Coat and hair react after the step, not before it. "
            "Background stays the same platform. No cut, no turn to a new outfit."
        ),
    },
    {
        "id": "fashion-trend-cut",
        "title": "趨勢節奏短切",
        "domain": "fashion",
        "model": "Kling 4.0 Flash",
        "settings": "5 秒，720p",
        "credits": "7.5",
        "bucket": "trends",
        "learned": ENG,
        "placeholders": "只借節奏，不借別人的運鏡逐格。一天內要發布。",
        "prompt": (
            "One continuous five-second take. A hand lifts {garment} into the light, then the camera tilts up to the collar. "
            "Movement is a single smooth tilt, not a montage. No beat markers, no on-screen text, no logo."
        ),
    },
    {
        "id": "film-empty-location",
        "title": "空場景",
        "domain": "film",
        "model": "Soul Cinema",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "methodology",
        "learned": FILM,
        "placeholders": "`{place}` 先用自己家或公開街景的結構。這張圖之後當 location reference。",
        "prompt": (
            "Vertical 9:16 empty location of {place} at {time_of_day}. "
            "No people. Show the floor, the main practical light, and one depth cue such as a doorway or a window. "
            "Camera at standing eye height, 35mm. The light direction must be obvious enough to reuse in the next shot."
        ),
    },
    {
        "id": "film-character-sheet",
        "title": "角色三視圖",
        "domain": "film",
        "model": "Seedream 5.0 Pro",
        "settings": "預設",
        "credits": "2.5",
        "bucket": "methodology",
        "learned": CINEMA + " " + FILM,
        "placeholders": "虛構角色用這條。真人用 Soul ID，不要用這條去複製某個公眾人物。",
        "prompt": (
            "Vertical 9:16 character sheet of {character_description}, front view, three-quarter view, and side view, "
            "same outfit, same neutral standing pose, even soft light, plain warm-gray background. "
            "No scene, no text labels, no weapons, no logos."
        ),
    },
    {
        "id": "film-night-push",
        "title": "夜景緩推",
        "domain": "film",
        "model": "Wan 3.0",
        "settings": "5 秒，720p",
        "credits": "7.5",
        "bucket": "daily-life",
        "learned": ENG,
        "placeholders": "家中實景重拍。不要點名特定電影或導演，避免被模型當成要模仿某部作品的畫面。",
        "prompt": (
            "Slow push in toward the person at the window. Red practical light from a lamp, green practical light from the street outside, "
            "fine film grain, slight motion smear only on the rain on the glass. "
            "The person does not speak. No poster, no subtitle, no cut."
        ),
    },
    {
        "id": "film-two-shot-blue-hour",
        "title": "藍時兩鏡",
        "domain": "film",
        "model": "Cinema Studio 4.0",
        "settings": "5 秒，720p，可開聲音",
        "credits": "35",
        "bucket": "methodology",
        "learned": FILM,
        "placeholders": "方法論定稿才用。參考圖用 `@` 標註自己的角色表與空場景。不要加長到 30 秒。",
        "prompt": (
            "Two shots, one hard cut at 2.5 seconds. 9:16. "
            "Shot 1: wide, the person from the character reference stands small in the empty location, blue hour, camera slowly dollies in. "
            "Shot 2: close-up, a passing warm light crosses their face, they turn their head a little toward the light. "
            "No dialogue. Sound is only room tone and a distant vehicle. Outfit and light direction stay the same across the cut."
        ),
    },
    {
        "id": "film-locked-exit",
        "title": "鎖定離開",
        "domain": "film",
        "model": "Kling 4.0",
        "settings": "5 秒，720p",
        "credits": "12.5",
        "bucket": "daily-life",
        "learned": CINEMA,
        "placeholders": "官方指南把靜止鏡頭當作可描述的運鏡。這條用在結尾，不要加對白。",
        "prompt": (
            "Locked-off camera. The person walks away from camera toward the doorway, stops, and looks back once. "
            "The lamp above the door does not flicker. No other person enters. End before they touch the handle."
        ),
    },
    {
        "id": "lit-title-card",
        "title": "一句話標題卡",
        "domain": "literature",
        "model": "GPT Image 2.6",
        "settings": "low，1K",
        "credits": "0.75",
        "bucket": "methodology",
        "learned": PLAN,
        "placeholders": "`{line}` 只能是創作者自己寫的句子，或已確認進入公共領域的短句。不要貼仍受保護的小說正文。",
        "prompt": (
            "Vertical 9:16 title card. The only words are: \"{line}\". "
            "Set them in a plain serif, lower third, on a dim room photograph with one lamp. "
            "No author name, no book cover, no publisher mark, no extra slogan."
        ),
    },
    {
        "id": "lit-room-from-sentence",
        "title": "由句子長出的房間",
        "domain": "literature",
        "model": "Soul Cinema",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "methodology",
        "learned": FILM,
        "placeholders": "用自己的句子描述光線與物件，不要描述某本書的角色名。",
        "prompt": (
            "Vertical 9:16 empty room that could illustrate this original sentence: \"{line}\". "
            "Show only the objects named in that sentence, plus one window. "
            "No people, no printed book, no cover typography. Light matches the mood of the sentence without adding new plot."
        ),
    },
    {
        "id": "lit-object-memory",
        "title": "物件記憶特寫",
        "domain": "literature",
        "model": "Soul 2.0",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "daily-life",
        "learned": ENG,
        "placeholders": "`{object}` 用桌上現成的東西。",
        "prompt": (
            "Vertical 9:16 close still of {object} on a reading table. "
            "A cup ring, a folded blank page, warm lamp, cool window. "
            "No readable writing, no printed paragraph, no portrait."
        ),
    },
    {
        "id": "lit-vertical-adaptation",
        "title": "直式轉場",
        "domain": "literature",
        "model": "Wan 3.0",
        "settings": "5 秒，720p",
        "credits": "7.5",
        "bucket": "methodology",
        "learned": ENG,
        "placeholders": "start image 用 lit-room-from-sentence 的靜幀。",
        "prompt": (
            "A slow push from the object on the table up to the window. "
            "Curtain moves once. No one enters. No words appear. No music cue in the picture."
        ),
    },
    {
        "id": "tech-object-hero",
        "title": "器物主視覺",
        "domain": "tech",
        "model": "Nano Banana Pro",
        "settings": "2K",
        "credits": "2",
        "bucket": "methodology",
        "learned": CINEMA,
        "placeholders": "`{device}` 用無商標的自製物件或去掉標誌的通用器材。不要做真實公司的產品照。",
        "prompt": (
            "Vertical 9:16 hero still of {device} on a matte bench. "
            "One hard strip of light across the surface, dark background, "
            "the right third empty for a later caption. No logo, no UI, no screen text, no hands."
        ),
    },
    {
        "id": "tech-bench-macro",
        "title": "工作檯切面",
        "domain": "tech",
        "model": "Soul 2.0",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "daily-life",
        "learned": ENG,
        "placeholders": "用自己的桌面。螢幕內容要模糊到讀不出字。",
        "prompt": (
            "Vertical 9:16 still of a workbench at night. A small unlabeled device, a notebook with a blank page, "
            "a monitor glow with no readable interface. 35mm, slight overhead angle. No brand, no notification bubbles."
        ),
    },
    {
        "id": "tech-reveal-draft",
        "title": "揭示草稿",
        "domain": "tech",
        "model": "Seedance 2.0 Mini",
        "settings": "5 秒，720p",
        "credits": "5",
        "bucket": "methodology",
        "learned": CINEMA,
        "placeholders": "草稿。過關再用 tech-reveal-final。三段式是官方產品廣告指南的結構，產品與動作是原創。",
        "prompt": (
            "A hand slides {device} from shadow into the strip of light, then lets go. "
            "Camera holds. No logo reveal, no screen turns on, no spoken claim."
        ),
    },
    {
        "id": "tech-reveal-final",
        "title": "揭示定稿",
        "domain": "tech",
        "model": "Seedance 2.5",
        "settings": "5 秒，720p",
        "credits": "35",
        "bucket": "methodology",
        "learned": FILM,
        "placeholders": "只在草稿通過後使用。不要升到 1080p（計畫中的 5 秒 1080p 是 80 點）除非 brief 寫明這是開場鏡。",
        "prompt": (
            "Locked lighting. The unlabeled device rotates a quarter turn on the bench as the camera arcs slowly to the left. "
            "One specular highlight travels across the shell. No text, no logo, no cut, no music visualizer."
        ),
    },
    {
        "id": "scifi-street-plate",
        "title": "街頭空景",
        "domain": "sci-fi",
        "model": "Soul Cinema",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "methodology",
        "learned": FILM,
        "placeholders": "先做真實街道的結構參考，再在下一條加近未來物件。建築輪廓以參考圖為準。",
        "prompt": (
            "Vertical 9:16 empty street plate of {street}. "
            "Keep the real building masses, the scooter lane, and the awning line. "
            "No people, no readable shop names, dusk, wet asphalt, practical shop light only."
        ),
    },
    {
        "id": "scifi-signage-lock",
        "title": "招牌鎖定",
        "domain": "sci-fi",
        "model": "Soul 2.0",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "methodology",
        "learned": CINEMA,
        "placeholders": "用 `@` 或參考圖鎖住 scifi-street-plate。新物件只有燈條，不改建築。",
        "prompt": (
            "Same street as the location reference, vertical 9:16. "
            "Add thin practical light strips along the existing awnings and one small hovering indicator above the lane. "
            "Do not move the buildings, do not translate any sign into readable text, do not add a crowd."
        ),
    },
    {
        "id": "scifi-street-walk",
        "title": "近未來街道行走",
        "domain": "sci-fi",
        "model": "Kling 4.0",
        "settings": "5 秒，1080p",
        "credits": "18.75",
        "bucket": "methodology",
        "learned": ENG,
        "placeholders": "定稿鏡。身份用 Soul ID 或角色表。",
        "prompt": (
            "The person walks along the locked street. Tracking shot beside them, medium distance, slight low angle. "
            "The added light strips stay fixed to the awnings. Reflections slide on the wet ground. "
            "No new vehicles enter, no readable text, no cut."
        ),
    },
    {
        "id": "scifi-cabin-console",
        "title": "艙內控制台",
        "domain": "sci-fi",
        "model": "Cinema Studio 4.0",
        "settings": "5 秒，720p",
        "credits": "35",
        "bucket": "rnd",
        "learned": CINEMA,
        "placeholders": "實驗桶。確認生成鍵之後才送。不要做 4K。",
        "prompt": (
            "Vertical 9:16 cabin interior. One person, seen from behind, sits at an unlabeled console. "
            "Slow dolly in. Status lights change brightness but never form letters. "
            "No franchise costume, no known robot design, no dialogue."
        ),
    },
    {
        "id": "ugc-hands-problem",
        "title": "問題是一雙手",
        "domain": "ugc-ads",
        "model": "Soul 2.0",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "trends",
        "learned": CINEMA,
        "placeholders": "官方產品廣告指南把廣告分成問題、解法、packshot。這裡只做問題靜幀，產品用自己的。",
        "prompt": (
            "Vertical 9:16 still, close on two hands at a kitchen counter, paused before using {product}. "
            "Morning window light. The product is generic packaging with no logo. "
            "Face is out of frame. No app UI, no captions."
        ),
    },
    {
        "id": "ugc-howto-step",
        "title": "一步教學",
        "domain": "ugc-ads",
        "model": "Wan 3.0",
        "settings": "5 秒，720p",
        "credits": "7.5",
        "bucket": "trends",
        "learned": COOK,
        "placeholders": "若改走 Marketing Studio 的 `ugc_how_to`，用官方技能，不要把這段再改寫成後端提示詞。這段是一般影片草稿。",
        "prompt": (
            "Hands complete one step with {product}: open, place, and stop. "
            "Camera stays overhead, static. No second step, no talking head, no lower-third text."
        ),
    },
    {
        "id": "ugc-packshot-space",
        "title": "留白的 packshot",
        "domain": "ugc-ads",
        "model": "Nano Banana Pro",
        "settings": "2K",
        "credits": "2",
        "bucket": "daily-life",
        "learned": CINEMA,
        "placeholders": "右側留白是為了後製貼自己的字，不要讓模型生成文字。",
        "prompt": (
            "Vertical 9:16 packshot. {product} held at the left third, neutral background, soft light. "
            "The right third is empty. No letters, no logo, no extra props."
        ),
    },
    {
        "id": "ugc-marketing-studio-brief",
        "title": "Marketing Studio 任務說明",
        "domain": "ugc-ads",
        "model": "Marketing Studio",
        "settings": "12 秒，720p，含音訊",
        "credits": "60",
        "bucket": "rnd",
        "learned": COOK,
        "placeholders": "60 點一條，只放實驗桶，而且一個月最多評估一次。模式用官方的 `ugc`、`ugc_how_to`、`ugc_unboxing`、`product_showcase` 或 `product_review`。交給 higgsfield-generate，不要自己組最終 prompt。",
        "prompt": (
            "Brief, not a final model prompt: 9:16, 12 seconds, mode {marketing_mode}. "
            "Product is {product}, photographed by me, no trademark. "
            "Show one problem and one use. Leave the lower third clear of generated text. "
            "Do not invent claims about health, price, or reviews."
        ),
    },
    {
        "id": "mv-portrait-hold",
        "title": "人像停頓",
        "domain": "music-video",
        "model": "Soul 2.0",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "daily-life",
        "learned": ENG,
        "placeholders": "表演者是創作者本人或已同意的人。不要做特定偶像的臉。",
        "prompt": (
            "Vertical 9:16 portrait still, shoulders and head, the person looking just off camera. "
            "One colored practical behind them, dark room, 85mm, shallow depth of field. "
            "No microphone brand, no poster, no lyric text."
        ),
    },
    {
        "id": "mv-chorus-hit",
        "title": "副歌一下",
        "domain": "music-video",
        "model": "Kling 4.0 Flash",
        "settings": "5 秒，720p",
        "credits": "7.5",
        "bucket": "trends",
        "learned": ENG,
        "placeholders": "音樂在剪輯軟體另軌貼上，而且必須是可用的曲目。不要在提示詞裡寫歌名。",
        "prompt": (
            "The person turns their head to camera on the first beat of movement and holds. "
            "A single practical flares and settles. Handheld, small shake, no lip sync, no lyric cards, no cut."
        ),
    },
    {
        "id": "mv-orbit-neon",
        "title": "霓虹半圈",
        "domain": "music-video",
        "model": "Wan 3.0",
        "settings": "5 秒，1080p",
        "credits": "15",
        "bucket": "daily-life",
        "learned": CINEMA,
        "placeholders": "官方 FAQ 寫明 orbital move 可以寫進提示詞。這條是短弧，不是 360 度展示。",
        "prompt": (
            "A short orbital arc, about a quarter turn, around the person standing in a narrow alley of practical neon. "
            "They stay still. The lights do not form letters. No crowd, no cut."
        ),
    },
    {
        "id": "mv-performance-wide",
        "title": "窄空間表演",
        "domain": "music-video",
        "model": "Seedance 2.0",
        "settings": "5 秒，720p",
        "credits": "22.5",
        "bucket": "methodology",
        "learned": FILM,
        "placeholders": "方法論裡講音樂影像時才用這一檔。趨勢反應片退回 mv-chorus-hit。",
        "prompt": (
            "Wide vertical frame in a small room. The person shifts weight and lifts one hand, then returns to stillness. "
            "Camera is locked off. Practical lights stay constant. No band, no logo, no on-screen lyric."
        ),
    },
    {
        "id": "shot-ecu",
        "title": "極特寫",
        "domain": "shot-size",
        "model": "Soul 2.0",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "daily-life",
        "learned": ENG,
        "placeholders": "`{detail}` 是眼睛、布邊、金屬緣這類局部。",
        "prompt": (
            "Vertical 9:16 extreme close-up of {detail}. "
            "The background is only color. Focus sits on the nearest edge. No text."
        ),
    },
    {
        "id": "shot-cu",
        "title": "特寫",
        "domain": "shot-size",
        "model": "Soul 2.0",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "daily-life",
        "learned": FILM,
        "placeholders": "官方 filmmaking 指南的第二鏡就是臉部特寫。這條是靜幀版。",
        "prompt": (
            "Vertical 9:16 close-up of the face from the reference, three-quarter view. "
            "Eyes sharp, background fully soft, one light from the side. No beauty-filter skin, no text."
        ),
    },
    {
        "id": "shot-ms",
        "title": "中景",
        "domain": "shot-size",
        "model": "Soul 2.0",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "daily-life",
        "learned": ENG,
        "placeholders": "腰部以上。",
        "prompt": (
            "Vertical 9:16 medium shot, waist up, of the person in {place}. "
            "Hands visible and still. Eye-level camera. Room light matches the window. No props with logos."
        ),
    },
    {
        "id": "shot-ws",
        "title": "廣角定場",
        "domain": "shot-size",
        "model": "Soul Cinema",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "methodology",
        "learned": FILM,
        "placeholders": "人在畫面裡要小，才有定場的作用。",
        "prompt": (
            "Vertical 9:16 wide shot of {place}. The person stands near the lower third and is about one fifth of the frame height. "
            "Show floor and ceiling or sky. 35mm. No crowd faces."
        ),
    },
    {
        "id": "shot-ots",
        "title": "過肩",
        "domain": "shot-size",
        "model": "Soul Cinema",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "methodology",
        "learned": CINEMA,
        "placeholders": "官方多鏡範例使用過肩。第二個人若不是同意出鏡的對象，就改成看向空場景。",
        "prompt": (
            "Vertical 9:16 over-the-shoulder still. The near shoulder is soft in the foreground. "
            "Beyond it, the other person or the empty doorway is sharp. No dialogue caption."
        ),
    },
    {
        "id": "shot-low-angle",
        "title": "低角度",
        "domain": "shot-size",
        "model": "Soul 2.0",
        "settings": "2K",
        "credits": "0.12",
        "bucket": "daily-life",
        "learned": CINEMA,
        "placeholders": "官方指南把 low-angle 當作可指定的角度。",
        "prompt": (
            "Vertical 9:16 low-angle still, camera near knee height, looking up at the person in {place}. "
            "Ceiling or sky occupies the top third. No heroic costume, no lens flare streak across the face."
        ),
    },
    {
        "id": "move-locked-off",
        "title": "鎖定機位",
        "domain": "camera-move",
        "model": "Wan 3.0",
        "settings": "5 秒，720p",
        "credits": "7.5",
        "bucket": "daily-life",
        "learned": FILM,
        "placeholders": "image-to-video。官方指南的結尾鏡可以是靜止機位。",
        "prompt": (
            "Locked-off camera. Only the subject moves: a small shift of weight and one breath. "
            "Background geometry stays fixed. No zoom."
        ),
    },
    {
        "id": "move-dolly-in",
        "title": "緩推",
        "domain": "camera-move",
        "model": "Wan 3.0",
        "settings": "5 秒，720p",
        "credits": "7.5",
        "bucket": "daily-life",
        "learned": ENG,
        "placeholders": "官方 prompt 指南把 dolly in 與 slow push 列為運動詞。",
        "prompt": (
            "Slow dolly in, straight toward the subject, constant speed, no change of height. "
            "The subject holds still. Stop before the face fills the frame."
        ),
    },
    {
        "id": "move-tracking",
        "title": "側向跟拍",
        "domain": "camera-move",
        "model": "Kling 4.0 Flash",
        "settings": "5 秒，720p",
        "credits": "7.5",
        "bucket": "trends",
        "learned": CINEMA,
        "placeholders": "官方指南使用 handheld tracking 與 tracking shot。",
        "prompt": (
            "Handheld tracking shot moving with the walking person, camera at their side, medium distance. "
            "Keep their full torso in frame. Background slides. No whip, no cut."
        ),
    },
    {
        "id": "move-telephoto",
        "title": "望遠鏡頭壓縮",
        "domain": "camera-move",
        "model": "Wan 3.0",
        "settings": "5 秒，720p",
        "credits": "7.5",
        "bucket": "methodology",
        "learned": CINEMA,
        "placeholders": "官方多鏡範例以 telephoto 開場。這條只測試壓縮感，人不需要跑。",
        "prompt": (
            "Telephoto look, background stacked close behind the subject. "
            "Very slow dolly in. The subject blinks once. No change of outfit."
        ),
    },
    {
        "id": "move-arc-orbit",
        "title": "弧線",
        "domain": "camera-move",
        "model": "Wan 3.0",
        "settings": "5 秒，720p",
        "credits": "7.5",
        "bucket": "methodology",
        "learned": CINEMA,
        "placeholders": "官方 FAQ 點名 dolly、arc、tracking、orbital。弧線不要轉滿一圈。",
        "prompt": (
            "A short arc shot, less than a quarter orbit, camera rising slightly. "
            "Subject stays planted. End on a three-quarter view. No 360 spin, no cut."
        ),
    },
    {
        "id": "move-whip",
        "title": "甩鏡",
        "domain": "camera-move",
        "model": "Grok Video 1.5 Lite",
        "settings": "5 秒，720p",
        "credits": "5",
        "bucket": "trends",
        "learned": ENG,
        "placeholders": "官方 prompt-engineering 提到 fast whip。只在趨勢草稿用，定稿前先看會不會糊掉主體。",
        "prompt": (
            "Fast whip pan from the object on the table to the person's face, then settle and hold. "
            "One move only. The face is sharp at the end. No second whip."
        ),
    },
    {
        "id": "move-drone",
        "title": "高處下降",
        "domain": "camera-move",
        "model": "Seedance 2.0 Mini",
        "settings": "5 秒，720p",
        "credits": "5",
        "bucket": "trends",
        "learned": CINEMA,
        "placeholders": "官方產品廣告範例使用過寬角的 drone 運動。這條改成街景，不拍真實航班或私人窗內。",
        "prompt": (
            "Wide-angle descent from above the street canopy down to standing height, smooth, no rotation. "
            "Reveal one person already waiting. No readable signs, no faces in the crowd, crowd stays out of focus if present at all."
        ),
    },
    {
        "id": "move-pov",
        "title": "主觀前進",
        "domain": "camera-move",
        "model": "Wan 3.0",
        "settings": "5 秒，480p",
        "credits": "3.75",
        "bucket": "daily-life",
        "learned": ENG,
        "placeholders": "最便宜的動作草稿。過關再換 720p。",
        "prompt": (
            "Point of view, walking forward through {place}, camera at eye height, natural head bob, no hands in frame. "
            "Stop at the doorway. No text, no map overlay."
        ),
    },
]

DOMAIN_FILES = {
    "art": ("by-domain/art.md", "藝術 art", "素描、材質、色彩腳本與展間。方法論的藝術集從這裡拿靜幀。"),
    "fashion": ("by-domain/fashion.md", "時裝 fashion", "捷運、夜市、飾品與走步。日常桶為主，一條留給趨勢節奏。"),
    "film": ("by-domain/film.md", "電影 film", "先空場景與角色表，再夜景、兩鏡定稿與鎖定結尾。"),
    "literature": ("by-domain/literature.md", "文學 literature", "只處理創作者自己的句子或已確認的公共領域短句。"),
    "tech": ("by-domain/tech.md", "科技 tech", "無商標器物。揭示片先草稿再定稿。"),
    "sci-fi": ("by-domain/sci-fi.md", "科幻 sci-fi", "先鎖真實街道，再加少量近未來光線。"),
    "ugc-ads": ("by-domain/ugc-ads.md", "UGC／廣告", "問題、一步教學、packshot。貴的 Marketing Studio 放在實驗桶。"),
    "music-video": ("by-domain/music-video.md", "音樂錄影帶 music video", "人像與表演。歌曲在剪輯軟體另軌處理。"),
    "shot-size": ("by-shot/shot-sizes.md", "鏡位 shot size", "靜幀鏡位。可套進任何領域，畫幅 9:16。"),
    "camera-move": ("by-shot/camera-moves.md", "運鏡 camera move", "給 image-to-video。只寫運動，不要把靜幀再描述一次。"),
}


def render_entry(entry: dict[str, str]) -> str:
    learned = f"{entry['learned']} {PLAN}" if PLAN not in entry["learned"] else entry["learned"]
    return "\n".join(
        [
            f"### `{entry['id']}` {entry['title']}",
            "",
            "| 欄位 | 內容 |",
            "| --- | --- |",
            "| kind | original-template |",
            f"| model | {entry['model']} |",
            "| aspect_ratio | 9:16 |",
            f"| est_credits | {entry['credits']} |",
            f"| settings | {entry['settings']} |",
            f"| bucket | `{entry['bucket']}` |",
            f"| learned_from | {learned} |",
            "",
            "```text",
            entry["prompt"],
            "```",
            "",
            entry["placeholders"],
            "",
        ]
    )


def render_domain(domain: str) -> str:
    path_name, title, intro = DOMAIN_FILES[domain]
    body = [f"# {title}", "", intro, "", "預設畫幅 9:16。改 `{占位符}` 之後再送出。", ""]
    for entry in ENTRIES:
        if entry["domain"] == domain:
            body.append(render_entry(entry))
    return "\n".join(body).rstrip() + "\n", path_name


def render_readme() -> str:
    lines = [
        "# 提示詞庫",
        "",
        "給 IG Reels、TikTok 與 X 的直式畫面。預設畫幅 **9:16**。說明用繁體中文，送給模型的提示詞用英文。",
        "",
        "每一條都是 `original-template`：句法是這個製作環境寫的。`learned_from` 指向公開技法或官方技能裡的鏡頭詞彙，不是把對方的範例整段抄進來。",
        "",
        "沒有收錄的東西：",
        "",
        "- OSideMedia/higgsfield-ai-prompt-skill 的提示詞。該庫已停止維護，見 `skills/UPSTREAM.md`。",
        "- Gumroad 等付費包。研究筆記裡只記錄它們存在，沒有購置，也沒有轉貼。",
        "- 官方 Cinema Studio 指南裡的飯店走廊、拆除大樓、披薩廣告、動畫對打等完整範例。那些文章的網址留在 `learned_from`，正文不複製。",
        "",
        "點數是 2026-11-21 的帳戶估價。生成鍵不同就以生成鍵為準，並改記帳，不回改這份庫，除非整份計畫一起更新。",
        "",
        "Image-to-video 用 `by-shot/camera-moves.md`，不要把靜幀內容再寫一次。",
        "",
        "## 目錄",
        "",
        "| id | 領域 | model | est. credits | bucket |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for entry in ENTRIES:
        _path, title, _intro = DOMAIN_FILES[entry["domain"]]
        lines.append(
            f"| `{entry['id']}` | {title} | {entry['model']} | {entry['credits']} | `{entry['bucket']}` |"
        )
    lines.extend(
        [
            "",
            "## 檔案",
            "",
            "- `by-domain/` 八個領域",
            "- `by-shot/shot-sizes.md` 鏡位",
            "- `by-shot/camera-moves.md` 運鏡",
            "",
            "改這份庫時，編輯 `prompts/_render_library.py` 的 `ENTRIES`，再執行 `python3 prompts/_render_library.py`。不要只改產生的 Markdown，下一次重跑會蓋掉。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    readme = render_readme()
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    for domain in DOMAIN_FILES:
        content, relative = render_domain(domain)
        destination = ROOT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        print(destination)


if __name__ == "__main__":
    main()
