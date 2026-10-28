---
name: read-book-video
description: 根据书名和风格选项（电影感/油画感）端到端制作一条竖版读书短视频，包括研究书籍、写配音文案、选图、做字幕时间表、生成片头/连接/正片动画并合成最终成片。
---

# 读书skill（read-book-video）

当用户提供**书名**和**风格选项**（`电影感` 或 `油画感`）并要制作读书短视频时，按本流程端到端执行。风格决定素材库路径，其余流程相同。

## 风格路由

- `油画感` → 素材库 `E:\素材库\油墨画`（3:4 竖版 PNG，油画/油墨风格）
- `电影感` → 素材库 `E:\素材库\电影感`
- 片头无声视频从 `E:\素材库\片头` 随机选择
- 连接视频的六张书籍封面固定从 `E:\codex_one\片头图片` 读取

素材选择通用要求：3:4 竖版（或可居中裁切为 3:4）、顶部和底部留出书名/字幕空间、无文字、无书封、无卡片界面、无水印。正片 5 张图随机抽取：同一视频内 5 张互不相同，且最近 4 个视频用过的图片不得再次使用（连续 4 个视频不重复）；使用记录保存在 `E:\codex_one\选图使用记录.txt`。

## 总流程

1. 研究书籍 → [references/01-book-research.md](references/01-book-research.md)
2. 写配音文案 `文案.txt` → [references/02-copy-and-subtitles.md](references/02-copy-and-subtitles.md)
3. 随机选图并重命名（片头.png、正文1段.png…正文4段.png，见 [references/02-copy-and-subtitles.md](references/02-copy-and-subtitles.md)）
4. 做字幕时间表 `字幕时间清单.txt`（需要正片旁白 mp3）
5. 生成正片动画 `正片.MP4` → [references/03-video-assembly.md](references/03-video-assembly.md)
6. 生成片头 `片头.MP4`
7. 生成连接视频 `连接.MP4`
8. 合成最终成片 `视频成片/最终成片.mp4`
9. 每个阶段结束时把该阶段步骤保存为 `制作<阶段>步骤.md`

## 全局约束

- 连接、正片动画：1080×1920（9:16）；片头动画：1920×1320（16:11）；最终成片输出 720×1280、码率约 8M；均为 30fps、H.264 + AAC。
- 正片书名距顶部 320px，连接书名距顶部 320px；正片字幕距底部 280px，中英双语（中文在上、英文在下）。
- HyperFrames 渲染时，内置 FFmpeg 通常不带 libx264，MP4 会因 `x264-params` 失败；固定做法是先用 HyperFrames 渲染 `--format webm`，再用系统 ffmpeg 的 `h264_qsv` 转码成 `.MP4`。
- 正片/片头/连接都是 HyperFrames 工程：`index.html`（宿主）+ `compositions/<名>.html`（`<template>` 子组合）+ `assets/`。GSAP 从本地 `assets/gsap.min.js` 加载。
- 每个 HyperFrames 组合只注册一条 `window.__timelines["<data-composition-id>"] = gsap.timeline({paused:true})`。
- 媒体 `<audio>` 必须带 `id`；图片 Ken Burns/缩放造成的越界用 `data-layout-allow-overflow` 标注。
- 用户拖入的旁白 mp3 通常在 `E:\tmp`；背景音乐目录 `E:\音频` 或 `E:\音乐`；输出目录 `E:\codex_one`。
- 旁白固定音色：使用 MiniMax TTS 自动生成（复用 `教育skill/scripts/minimax_tts.py`），模型 `speech-02-hd`，克隆音色 `readbook_gentle_female_v03`（专属音色，克隆自用户提供的最新女声，参考音频 `assets/voice/声音1_人声_60s.mp3`），语速约 0.9；`MINIMAX_API_KEY` 从本机已有配置查找，找不到再向用户要。书名行后加句号制造停顿，正文句内空格改逗号。禁止再改用其他音色。
- 背景音乐固定使用 `E:\音频\WindHill钢琴版.mp3`，基础音量 1.0；合成时人声放大 1.5 倍；背景音乐比总时长短时用 `-stream_loop -1` 自动循环。如该文件缺失，再向用户要，不用其他音乐替代。

## 阶段输出与命名

| 阶段 | 输出 |
|------|------|
| 研究 | 书籍信息清单（对话中输出） |
| 文案 | `E:\codex_one\文案.txt` |
| 选图 | `E:\codex_one\{片头,正文1段,正文2段,正文3段,正文4段}.png` + `E:\codex_one\选图使用记录.txt` |
| 字幕 | `E:\codex_one\字幕时间清单.txt` |
| 正片 | `E:\codex_one\正片\正片.MP4` |
| 片头文案 | `E:\codex_one\片头文案.txt` |
| 片头文案模式记录 | `E:\codex_one\片头文案模式记录.txt` |
| 片头 | `E:\codex_one\片头\片头.MP4` |
| 连接 | `E:\codex_one\连接\连接.MP4` |
| 成片 | `E:\codex_one\视频成片\最终成片.mp4` |

执行顺序不能乱：文案必须先于字幕；字幕必须先于正片；正片、片头、连接都完成后才能合成。
