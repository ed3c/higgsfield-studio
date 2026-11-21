#!/usr/bin/env python3
"""Build the creator index and study queue from research/creators.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research" / "creators.json"
INDEX = Path(__file__).resolve().parent / "index.md"
QUEUE = Path(__file__).resolve().parent / "study-queue.md"

DOMAIN_ORDER = [
    "art",
    "fashion",
    "film",
    "literature",
    "tech",
    "scifi",
    "ads",
    "mv",
    "shorts",
    "sports",
]

DOMAIN_LABELS = {
    "art": "藝術 art",
    "fashion": "時裝 fashion",
    "film": "電影 film",
    "literature": "文學 literature",
    "tech": "科技 tech",
    "scifi": "科幻 sci-fi",
    "ads": "廣告／UGC ads",
    "mv": "音樂錄影帶 music video",
    "shorts": "短影音 shorts",
    "sports": "運動 sports",
}

CATEGORY_ORDER = {
    "award_winner": 0,
    "official_partner": 1,
    "community_featured": 2,
    "industrial_studio": 3,
}

CATEGORY_LABELS = {
    "award_winner": "得獎",
    "official_partner": "官方合作",
    "community_featured": "社群精選",
    "industrial_studio": "產業案例",
}

# 學習隊列不是獎金排名。十個位子要蓋住方法論六個領域，以及日常再創作與音樂錄影。
STUDY_QUEUE = [
    {
        "hf_username": "joeysnoisygroup",
        "pillar": "方法論",
        "lesson": "學他把流程拆開的方式：公開的 Story Bible、Castkit、Scenecraft、Shotcaller。本系列要觀眾能跟著做。不要複製他的成片。他的 TinyURL skill 包沒有版本庫，使用前另存，且不要把它當成官方 skills。",
    },
    {
        "name": "PURGA Studio（Martín & Manuel Montes de Oca、Bautista Vidal、Joaquín Iraola）",
        "pillar": "電影、文學",
        "lesson": "看一支得獎短片怎麼用一個荒謬情境撐完全片，而不是堆模型。文學領域的方法論集，研究「一句話如何變成對峙」，不要重做 Listen to Meh 的角色或台詞。",
    },
    {
        "hf_username": "aist",
        "pillar": "電影、科技",
        "lesson": "看災難題材如何把人物表情與聲音放在視覺前面。科技集若要做「揭示片」，先學這類完成度，再決定模型。",
    },
    {
        "hf_username": "tseily",
        "pillar": "日常再創作",
        "lesson": "官方 Creative Partner，定位是電影感日常。這是日常桶最接近的公開參考：生活素材如何變成電影感，而不是換一張臉。",
    },
    {
        "hf_username": "aleksandra",
        "pillar": "時裝、藝術",
        "lesson": "時裝與編輯設計，並有藝術教育。方法論集要講得清楚時，看她如何把風格說成可以教的東西。提示詞仍用本庫原創模板。",
    },
    {
        "hf_username": "yoav_yariv",
        "pillar": "科幻、科技",
        "lesson": "人與機器的關係可以是一集的題目，不一定是爆炸場景。做台北近未來時，先問故事裡的機器改變了誰，再鎖街景。",
    },
    {
        "name": "Authors First",
        "pillar": "文學",
        "lesson": "官方案例是故事板在短時間內轉成影像。文學集採用這個順序：句子、分鏡、靜幀、再動畫。不要把受保護的原文貼進提示詞。",
    },
    {
        "hf_username": "tambv",
        "pillar": "時裝、音樂錄影、藝術",
        "lesson": "同一位創作者同時做動畫、時尚商業與音樂影像。跨領域的那一集（時裝乘趨勢、藝術乘電影）看他怎麼讓風格統一，而不是看他怎麼接客戶。",
    },
    {
        "name": "One of One Studio",
        "pillar": "時裝、廣告",
        "lesson": "官方案例是把授權商品做成一個世界，而不是單張海報。自有系列若要做服裝世界觀，研究「世界先於單品」。沒有公開的可複製提示詞。",
    },
    {
        "name": "Boxel Studio",
        "pillar": "電影、科技",
        "lesson": "產業預製：Cinema Studio、Seedance、Kling、Veo 被用來縮短預視覺化，藝術家仍做決定。方法論集講「工業級」時，指的是這種分工，不是把四個模型各抽一次。",
    },
]


def load_creators(path: Path) -> tuple[dict, list[dict]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    creators = payload["creators"]
    if len(creators) != 79:
        raise ValueError(f"預期 79 人，讀到 {len(creators)}")
    return payload["meta"], creators


def creator_key(creator: dict) -> tuple[int, str]:
    category = CATEGORY_ORDER.get(creator.get("category") or "", 9)
    return category, creator["name"].casefold()


def find_creator(creators: list[dict], spec: dict) -> dict:
    if "hf_username" in spec:
        matches = [
            creator
            for creator in creators
            if creator.get("hf_username") == spec["hf_username"]
        ]
    else:
        matches = [creator for creator in creators if creator["name"] == spec["name"]]
    if len(matches) != 1:
        raise ValueError(f"學習隊列對不到唯一創作者：{spec}")
    return matches[0]


def format_link(url: str) -> str:
    return f"<{url}>"


def profile_line(creator: dict) -> str:
    username = creator.get("hf_username")
    url = creator.get("hf_url")
    if url:
        return f"[{username}]({url})"
    if username:
        return f"`{username}`（研究註記：當下沒有可用的公開頁）"
    return "無 higgsfield.ai 使用者名稱"


def social_line(creator: dict) -> str:
    socials = creator.get("socials") or {}
    if not socials:
        return "無"
    parts = [f"{key}: {format_link(value)}" for key, value in socials.items()]
    return " · ".join(parts)


def source_line(creator: dict) -> str:
    sources = creator.get("sources") or []
    if not sources:
        return "無"
    return " · ".join(format_link(url) for url in sources)


def render_creator(creator: dict) -> str:
    domains = ", ".join(creator.get("domains") or [])
    confidence = creator.get("confidence") or ""
    category = CATEGORY_LABELS.get(creator.get("category") or "", creator.get("category"))
    lines = [
        f"### {creator['name']}",
        "",
        f"- 頁面：{profile_line(creator)}",
        f"- 分類：{category}／信心：{confidence}",
        f"- 領域：{domains}",
        f"- 定位：{creator.get('niche') or ''}",
        f"- 身份：{creator.get('award') or ''}",
        f"- 代表：{creator.get('notable') or ''}",
        f"- 社群：{social_line(creator)}",
        f"- 來源：{source_line(creator)}",
    ]
    note = (creator.get("socials_note") or "").strip()
    if note:
        lines.append(f"- 研究註記：{note}")
    lines.append("")
    return "\n".join(lines)


def render_index(meta: dict, creators: list[dict]) -> str:
    counts = meta.get("counts") or {}
    lines = [
        "# 創作者索引",
        "",
        "由 `research/creators.json` 產生。改資料後重跑 `python3 creators/generate_index.py`。不要手改本檔。",
        "",
        f"- 資料日期：{meta.get('as_of')}（{meta.get('timezone')}）",
        f"- 列入：{counts.get('total_listed')}。其中 verified {counts.get('verified')}，只有使用者名稱 {counts.get('verified_username_only')}，轉述帳號 {counts.get('reported_handle')}。",
        "- 一個人可以出現在多個領域。學習順序見 [study-queue.md](study-queue.md)。",
        "- 原始方法說明在 `research/README.md`。此處不新增研究裡沒有的人。",
        "",
    ]
    by_domain: dict[str, list[dict]] = {domain: [] for domain in DOMAIN_ORDER}
    unknown: list[str] = []
    for creator in creators:
        for domain in creator.get("domains") or []:
            if domain not in by_domain:
                unknown.append(f"{creator['name']}:{domain}")
                continue
            by_domain[domain].append(creator)
    if unknown:
        raise ValueError(f"未知領域 {unknown}")
    for domain in DOMAIN_ORDER:
        group = sorted(by_domain[domain], key=creator_key)
        lines.append(f"## {DOMAIN_LABELS[domain]}（{len(group)}）")
        lines.append("")
        if not group:
            lines.append("（無）")
            lines.append("")
            continue
        for creator in group:
            lines.append(render_creator(creator))
    return "\n".join(lines).rstrip() + "\n"


def render_queue(creators: list[dict]) -> str:
    lines = [
        "# 學習隊列",
        "",
        "前十名是給這個頻道的課表，不是獎金榜。動作片得獎者很多，若按獎金排，時裝、文學與日常會消失。",
        "",
        "挑選規則：",
        "",
        "1. 優先 `verified`。",
        "2. 十個位子要蓋住藝術、時裝、電影、文學、科技、科幻，並留下日常短影與音樂錄影的入口。",
        "3. 有公開教學或官方案例的人優先，因為方法論系列要講得出步驟。",
        "4. 研究流程與完成度。不複製成片、角色、台詞或未授權的客戶素材。",
        "",
        "事實欄位來自 `research/creators.json`。每個人的「這一季要看什麼」是本庫的課表，不是對方的自我介紹。",
        "",
    ]
    for rank, spec in enumerate(STUDY_QUEUE, start=1):
        creator = find_creator(creators, spec)
        domains = ", ".join(creator.get("domains") or [])
        lines.extend(
            [
                f"## {rank}. {creator['name']}",
                "",
                f"- 這一季：{spec['pillar']}",
                f"- 看什麼：{spec['lesson']}",
                f"- 頁面：{profile_line(creator)}",
                f"- 領域：{domains}",
                f"- 定位：{creator.get('niche')}",
                f"- 身份：{creator.get('award')}",
                f"- 信心：{creator.get('confidence')}",
                f"- 代表：{creator.get('notable')}",
                f"- 來源：{source_line(creator)}",
                "",
            ]
        )
    lines.extend(
        [
            "## 接著看，但不佔這十個位子",
            "",
            "- Double Shots：官方案例是用 Cinema Studio 做音樂錄影帶。音樂錄影集若要產業流程，排在 TAMBV 之後。",
            "- Stephan Vasement：珠寶與氣氛產品。廣告桶要做靜物時再看。",
            "- Yenlik：Soul Photodump 的社交預設。帳號信心是 `reported_handle`，所以沒有放進前十。",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    meta, creators = load_creators(SOURCE)
    INDEX.write_text(render_index(meta, creators), encoding="utf-8")
    QUEUE.write_text(render_queue(creators), encoding="utf-8")
    print(f"wrote {INDEX}")
    print(f"wrote {QUEUE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
