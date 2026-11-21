# 01 逆向工程

目的：把參考片拆成可重用的技法，不是複製成片。

## 輸入
- 參考片（自己的、得獎片的公開頁、@tupacabra 這類公開預告）。
- 拆解工具（皆為第三方 MIT 開源，非 Higgsfield 官方）：
  - simcraft 的 `reverse-engineer-video`：https://github.com/dotslashsimran/simcraft （切點、鏡長、運鏡、聲音節拍、contact sheet）
  - open-edits 的 `reverse-engineer`：https://github.com/kevinbadi/open-edits （剪輯風格量測，偏口播短片）
  - video-deconstructor：https://github.com/shivam098/video-deconstructor （yt-dlp + ffmpeg + 多模態；2026-11 時 0 星，先當實驗）

## 產出
- `reference-report.md`：每支參考片的鏡數、中位鏡長、色彩、構圖規律、聲音策略，附來源連結。範本：[../schemas/reference-report.md](../schemas/reference-report.md)
- `style-bible.md`：本片要借的技法清單與禁用清單。範本：[../schemas/style-bible.md](../schemas/style-bible.md)

## 門檻
- 每個技法都有來源連結或標「推論」。
- 禁用清單寫明：不使用對方角色、片段、標題、品牌、真人肖像。
- 下載他人影片只做本地分析，不再發布。
