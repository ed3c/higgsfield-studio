#!/usr/bin/env python3
"""Render treatments.json into README.md and costs.csv. Prices come from budget/cost-table.csv."""
import csv, json, math, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
P = {(r["model"], r["settings"]): float(r["credits_numeric"] or 0) for r in csv.DictReader(open(ROOT / "budget/cost-table.csv", encoding="utf-8"))}
CS4 = P[("Cinema Studio 4.0", "5 秒，720p")] / 5        # 7 per second, min 5 s
GJ = P[("Genjutsu Lite", "15 秒，720p")]                # 32 per clip up to 15 s
UPS = P[("ByteDance 影片放大", "4K，帶 5 秒時長參數，未帶來源影片")]
VO = P[("Seed Audio 1.0", "語音預設")]
TAKES, RESERVE, LANGS = 2, 0.15, 7
TOOL = {"cs4": "Cinema Studio 4.0 720p", "genjutsu": "Genjutsu Lite 720p", "edit": "剪輯軟體"}
CONTEST = {"safe-if-replaced": "比賽可用（人物換成虛構、權力人物只以物件與字幕存在）", "portfolio-only": "只能當作品集"}

def cost(s, portfolio=False):
    d = s["t"][1] - s["t"][0]
    if s["tool"] == "edit" or (portfolio and s["tool"] == "genjutsu"):
        return 0.0
    return (max(5, d) * CS4 if s["tool"] == "cs4" else GJ * math.ceil(d / 15)) * TAKES

def total(T, portfolio=False):
    gen = sum(cost(s, portfolio) for s in T["shots"])
    ups = UPS * sum(1 for s in T["shots"] if cost(s, portfolio) > 0)
    vo = VO * sum((LANGS if s.get("babel") else 1) for s in T["shots"] if s.get("vo"))
    return gen, ups, vo, math.ceil((gen + ups + vo) * (1 + RESERVE))

data = json.load(open(HERE / "treatments.json", encoding="utf-8"))
rows = []
md = ["# 黃仁勳寓言 × 坂本龍一理論：三個新劇本", "", "由 `build_treatments.py` 從 `treatments.json` 產生。來源見 `sources.md`。這一階段 0 點。", "", f"> {data['premise']}", "",
      "## 坂本龍一原則 → 剪輯／聲音／結構規則", "", "| 原則 | 出處 | 規則 |", "| --- | --- | --- |"]
md += [f"| {r['principle']} | {r['source']} | {r['rule']} |" for r in data["sakamoto_rules"]]
md += ["", "## 估點總表", "", "Cinema Studio 4.0 720p 每秒 7 點（最少 5 秒）、Genjutsu Lite 每段 15 秒內 32 點，每鏡 2 take；放大每鏡 4 點；旁白每句 0.2 點（七語疊念算 7 句）；加 15% 修補預備。關鍵幀走網站 Unlimited，0 點。", "",
       "| 劇本 | 長度 | 影片 | 放大 | 旁白 | 合計（含 15%） | 作品集版（保留原片、不跑 Genjutsu） | 比賽 |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
summ = []
for T in data["treatments"]:
    g, u, v, t = total(T); pt = total(T, True)[3]
    dur = max(s["t"][1] for s in T["shots"])
    T["_c"] = (g, u, v, t, pt, dur)
    summ.append([T["id"], T["zh"], T["en"], dur, g, u, round(v, 1), t, pt, T["contest"]])
    md.append(f"| {T['id']} {T['zh']} {T['en']}{'（推薦）' if T['recommended'] else ''} | {dur} 秒 | {g:g} | {u:g} | {v:.1f} | **{t}** | {pt} | {CONTEST[T['contest']]} |")
    for s in T["shots"]:
        rows.append([T["id"], s["id"], s["t"][0], s["t"][1], s["src"], TOOL[s["tool"]], cost(s), cost(s, True)])
for T in data["treatments"]:
    g, u, v, t, pt, dur = T["_c"]
    md += ["", f"## {T['id']}《{T['zh']} {T['en']}》{'（推薦）' if T['recommended'] else ''}", "", f"- 一句話：{T['logline_zh']}", f"- Logline: {T['logline_en']}", f"- 結構：{T['structure']}", f"- 原片主幹：{T['spine']}", f"- 比賽：{CONTEST[T['contest']]}。{T['contest_note']}", "",
           f"### 鏡頭表（{dur} 秒）", "", "| 鏡 | 時間 | 原片 | 畫面 | 旁白／字幕 | 工具 | 點數 |", "| --- | --- | --- | --- | --- | --- | ---: |"]
    for s in T["shots"]:
        vo = (f"「{s['vo'][0]}」<br>“{s['vo'][1]}”" + ("<br>（七語疊念）" if s.get("babel") else "")) if s.get("vo") else "—"
        md.append(f"| {s['id']} | {s['t'][0]}–{s['t'][1]}s | {s['src']} | {s['zh']} | {vo} | {TOOL[s['tool']]} | {cost(s):g} |")
    md += ["", f"聲音與配樂：{T['sound']}", "", f"估點：影片 {g:g}＋放大 {u:g}＋旁白 {v:.1f}，含 15% 預備 **{t} 點**（月額度 {t/90:.1f}%）；作品集版 {pt} 點。", "", "### 關鍵幀（網站 Unlimited，上傳對應 plate 當參考圖）", ""]
    for k in T["keyframes"]:
        md += [f"**{k['id']}**（{k['model']}，9:16，參考 `{k['plate']}`）", "", "```text", k["prompt"], "```", ""]
    if T.get("short_outline"):
        md += ["### 3–5 分鐘短片大綱", ""] + [f"- {x}" for x in T["short_outline"]]
md += ["", "## 風險", "",
       "- 真人肖像：任何版本都不畫黃仁勳、川普、普丁、習近平的臉或逼真肖像；J2 的黑皮衣背影、J3 的三王棋子仍可能被認出原型，所以只當作品集。",
       "- 誹謗：只用已公開報導的事實（15% 抽成、H20、華為昇騰、「落後幾奈秒」）；字幕引語要與報導一致；普丁只當寓言，不陳述事實。片頭加「虛構寓言」字卡。",
       "- 宗教隱喻：燃燒的荊棘、巴別塔、金牛犢只當寓言，不連結當前以色列政治或戰爭；避免任何宗教符號被當成嘲諷對象。",
       "- 商標：不出現 NVIDIA、GeForce、Huawei、Sega 等名稱與標誌；提示詞都寫 no logos，字幕也不寫公司名。",
       "- 坂本龍一版權：只借理論，不用錄音、旋律、取樣；原創五聲動機要避免近似〈戰場上的快樂聖誕〉。",
       "- 比賽：J1 比賽版要用 Genjutsu 換掉 Neon、所有影像在 Contest Project 內生成；拿真人影片當動作參考是否允許仍待確認。",
       "- 技術：沿用原片風險（地上水紋閃動、00:41 全黑、反光襯衫、臉只有約 70 像素）。"]
(HERE / "README.md").write_text("\n".join(md) + "\n", encoding="utf-8")
with open(HERE / "costs.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["treatment", "shot", "start_s", "end_s", "source", "tool", "credits", "credits_portfolio"]); w.writerows(rows)
with open(HERE / "costs-summary.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["treatment", "name_zh", "name_en", "seconds", "video", "upscale", "vo", "total_with_15pct", "portfolio_total", "contest"]); w.writerows(summ)
for s in summ: print(s)
