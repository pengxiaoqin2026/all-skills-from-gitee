---
name: vibe-award-video
description: Generate a Vibe知识大赏-style knowledge short video from a single topic using the local Hypit pipeline (SVML + custom TypeScript graphics components + headless render + ffmpeg mux). Use when the user asks to "做一个 vibe 知识大赏视频 / vibe大赏 / 科普短片" and gives a topic, or wants to edit/regenerate the existing knowledge-curse project. Do not use for剪映-style edits, talking-head narration, or footage montages.
metadata:
  short-description: 用 Hypit 从主题一键生成 Vibe知识大赏短片
---

# vibe 大赏视频

输入一个主题，产出约 2 分钟、深色电影感、无旁白、双语字幕的 Vibe 知识大赏短片。

## 何时用

用户给一个知识主题并要“做一条 vibe 大赏 / 科普短片”。已有成品和可复用工程在 `E:\vibe大赏\hypit-project`（知识诅咒那条）。

## 总流程

选题核实 → 脚本分镜 → 复制模板工程 → 为主题生成专属图形 → 写 `main.svml` → `hypit check/plan/build` → 混音导出。

1. 选题核实：查证事实，剔除传言；一个视频只讲一个核心问题，结尾留引用位。
2. 脚本分镜：读 references/style-and-narrative.md，按“历史时间线”或“六段式”写中英双语字幕，并为每个画面选定一个“本主题专属图形意象”。
3. 复制模板：把 `E:\vibe大赏\hypit-project` 复制成新项目目录（保留 `packages/tap-wave`、`local`、`hypit.runtime.json`、`recipes.svs`）。
4. 生成专属图形：为本主题新设计并实现一套图形组件（约 8–11 个，贴合主题核心意象），替换模板的通用组件；禁止复用上个视频或模板已用过的图形。做法见 references/hypit-authoring.md 的“图形组件”一节。
5. 写 `main.svml`：读 references/hypit-authoring.md，用本主题的新组件实例化图形，定义 `time:Timeline` 的窗口、`text:Flow` 字幕、`wave:*` 图形实例、`film:Film` 轨道。
6. 渲染：`hypit check` → `hypit build --follow`，成功后 `hypit get <build> --output final.video --to <mp4>`。
7. BGM：默认用 `E:\音乐\We_Never.mp3`（若存在），已在模板的 `media:Audio` + `audio:Track` 里接入；换音乐改 `assets/We_Never.mp3`。

## 铁律

- 事实纪律：数字、人名、文献必须能复核，查不到就换说法或删掉；片尾有引用和免责。
- 无旁白，信息由双语字幕承担；BGM 纯器乐。
- 每个画面一个图形，同一视频内图形不重复。
- 图形必须为主题新生成：每个新主题都要重新设计并实现一套贴合该主题的图形组件，禁止复用模板或上一个视频的图形组件。Wave/Seal/BookCard/Timeline/Perspective/Badge/Knock/Mind/Steps/Bridge/Quote 只是起步代码参考，不是可复用素材库。
- 图形不得遮挡文字：每个画面的图形要放在不压字幕的空白带（居中字幕时优先右侧或下方），或改用描边 + 低透明度填充；图形颜色不得与压在它上面的文字同色（金色图形会吞掉金色标题）。做法见 references/hypit-authoring.md 的“图形与文字避让”一节。
- 元素错峰入场（一个接一个），就位后定格约 3 秒并保留“呼吸/漂浮”微动，不要静止到底。

## 参考

- 写分镜和字幕前读 references/style-and-narrative.md。
- 写 SVML 或加图形组件时读 references/hypit-authoring.md（含语法骨架、组件清单、踩坑记录）。
