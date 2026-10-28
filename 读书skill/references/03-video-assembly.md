# 阶段五、六、七、八：HyperFrames 动画与最终合成

读取 HyperFrames 入口 skill（`C:\Users\Administrator\.codex\skills\hyperframes\SKILL.md`）和 `hyperframes-core`，再写 HTML。以下为本流程已验证的固定模式。

## 通用工程结构

每个视频一个项目目录（`正片`、`片头`、`连接`）：

```text
<项目>/
|-- index.html
|-- compositions/<名>.html
`-- assets/  （图片、mp3、gsap.min.js）
```

`index.html`（宿主，不套 template）：

```html
<script src="assets/gsap.min.js"></script>
<div id="root" data-composition-id="host" data-width="720" data-height="960" data-duration="<D>">
  <div id="main-slot" class="clip" data-composition-id="main" data-composition-src="compositions/<名>.html" data-start="0" data-duration="<D>" data-width="720" data-height="960" data-track-index="0"></div>
</div>
<script>window.__timelines["host"] = gsap.timeline({ paused: true });</script>
```

`compositions/<名>.html`（套 `<template>`，style/script 都放 template 内，`data-composition-id="main"`）：

```html
<template>
  <style>/* 样式 */</style>
  <div id="root" data-composition-id="main" data-width="720" data-height="960" data-duration="<D>">
    <!-- 内容 -->
    <audio id="narration" src="assets/<名>.mp3" data-start="0" data-duration="<D>" data-track-index="10"></audio>
  </div>
  <script>(function(){ var tl = gsap.timeline({paused:true}); /* tweens */ window.__timelines["main"] = tl; })();</script>
</template>
```

gsap 本地化：复制 `E:\codex_one\正片\assets\gsap.min.js`（或用网络下载 `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js`）到各项目 `assets/`。

## 正片动画

- 总时长 = 正片旁白 mp3 时长。
- 5 张图：`片头.png`、`正文1段.png`…`正文4段.png`。
- 片头图 0 秒显示，0.32 秒淡出；正文1段 0.32 秒淡入。
- 切换点：25%、50%、75% 切正文2/3/4段；交叉淡化约 0.8 秒。
- 每张图 Ken Burns：`scale 1.05→1.22` 并轻微 `xPercent/yPercent` 平移。

图片 clip 示例（Ken Burns 越界加 `data-layout-allow-overflow`）：

```html
<div id="img-1" class="clip" style="z-index:2" data-start="0.32" data-duration="10.84" data-track-index="1">
  <img src="assets/正文1段.png" alt="" data-layout-allow-overflow>
</div>
```

GSAP 交叉淡化 + Ken Burns：

```js
tl.set("#img-1", { opacity: 0 }, 0.32);
tl.to("#img-kaitou", { opacity: 0, duration: 0.8, ease: "none" }, 0.32);
tl.to("#img-1", { opacity: 1, duration: 0.8, ease: "none" }, 0.32);
tl.to("#img-1", { opacity: 0, duration: 0.8, ease: "none" }, S1);
tl.to("#img-2", { opacity: 1, duration: 0.8, ease: "none" }, S1);
tl.fromTo("#img-1 img", { scale: 1.05, xPercent: 0, yPercent: 0 }, { scale: 1.22, xPercent: -6, yPercent: 2, duration: <dur>, ease: "none" }, 0.32);
```

顶部书名/作者（固定显示，左右各 42px，可用 996px，书名距顶部 320px；书名 `fitTextFontSize` 72→63px，作者 51px，下方 24px，黑阴影）；顶部加一层很轻的暗部渐变保证白字可读，但文字元素本身无底色框。

底部字幕（左右各 36px，可用 648px，距底 100px；中文字幕基准 34px 最小 28px，行高 1.12，`white-space:nowrap; word-break:keep-all; overflow-wrap:normal`，粗白字+黑阴影）。每条中文字幕下方显示对应英文翻译（英文 24px、字重 700、白色+黑阴影，类名 `.subtitle-text-en`）。字幕结构用 `.clip subtitle-clip` 包裹 `.subtitle-stack`（竖排：中文 `.subtitle-text` 在上、英文 `.subtitle-text-en` 在下）+ `data-start/data-duration`；超过 12 字的句子按空格/语义拆 2 条，按字数比例分配时间。

## 片头动画

- 总时长 = 片头文案 mp3 时长。
- 画幅固定为 16:11：`1920×1320`，30fps（片头单独使用 16:11，连接和正片是 1080×1920）。
- 片头无声视频从 `E:\素材库\片头` 随机选一个 mp4，复制为 `assets/片头视频.mp4`；画中画副本用另一个文件名 `assets/片头视频副本.mp4`（同源复制一份，避免 duplicate media 警告）。
- 主画面和画中画都用 `<video>`，属性 `autoplay muted loop playsinline`，并给 `data-start="0"`、`data-duration="<D>"`，`object-fit:cover`。
- 0–1.55 秒：主画面 `xPercent -100→0`，画中画 1380×950（16:11 小副本，只比主画面略小）`xPercent 200→0`，`ease:"none"`。
- 1.55–2 秒：画中画 `scale 1.391` 且 `opacity 0`。
- 2 秒起：主画面 video `scale 1→1.10` 直到结束。

视频版 HTML 结构：

```html
<div id="main" data-layout-allow-overflow>
  <video id="main-video" src="assets/片头视频.mp4" autoplay muted loop playsinline
         data-start="0" data-duration="<D>" data-layout-allow-overflow></video>
</div>
<div id="pip" data-layout-allow-overflow>
  <video id="pip-video" src="assets/片头视频副本.mp4" autoplay muted loop playsinline
         data-start="0" data-duration="<D>"></video>
</div>
```

GSAP 缩放对象从 `#main img` 改为 `#main video`。

## 片头字幕（最终合成时用 drawtext 画在下方黑区）

- 片头动画本身不含字幕；字幕在最终合成时用 FFmpeg `drawtext` 画到 720×1280 成片下方黑色区域（y≈895 起）。
- 中文字幕：38px，米白填充 `#FAF5EC` + 淡黄描边 `#FFE9A8`（2px），水平居中。
- 英文翻译：22px，显示在中文字幕下方（y≈950），米白填充 + 淡黄描边（1px），水平居中。
- 字体文件：中文 `C:\Windows\Fonts\msyh.ttc`（微软雅黑常规体，更细）；英文 `C:\Windows\Fonts\msyhbd.ttc`（微软雅黑粗体）。
- 字幕内容来自 `片头文案.txt`，先按口播停顿拆句，中文与英文成对，逐句设置开始/结束时间（用 `enable='between(t,start,end)'`）。

## 连接视频

- 1080×1920、30fps、总时长 1.30 秒，齿轮音效 `assets/齿轮.mp3`。
- 六张书籍封面按顺序，每本 0.20 秒；书名距顶部 320px、作者下方 44px。书名/作者字体填充色 `#E6E6E6`，淡青描边 `#A0C3CA`（书名约 3px、作者约 2px），黑色阴影；书名字号 81→63px 自适应，作者 45px。
- 每张封面 `scale 1.08/y 40 → scale 1.0/y 0`（0.10 秒进入），整页 `opacity 1/y 0 → opacity 0/y -60`（0.10 秒向上淡出）。
- 1.20–1.30 秒加一个黑场 clip：`data-start="1.200" data-duration="0.100"`，`background:#000; z-index:100`。

## 渲染与转码（每个视频）

先 lint，再渲染 webm，最后转 mp4：

```bash
npx hyperframes lint --json
npx hyperframes render --quality high --format webm --output <名>.webm
ffmpeg -y -i <名>.webm -c:v h264_qsv -b:v 8M -c:a aac -b:a 192k -movflags +faststart <名>.MP4
```

## 最终成片合成

片头是 16:11（1920×1320），连接和正片是 1080×1920。合成时先把片头缩放到 720×495，再上下加黑边到 720×1280；连接和正片缩放到 720×1280；然后按顺序拼接，叠加固定背景音乐 `E:\音频\WindHill钢琴版.mp3`（基础音量 1.0，人声放大 1.5 倍；背景音乐比总时长短时用 `-stream_loop -1` 循环）：

```bash
ffmpeg -y -i 片头.MP4 -i 连接.MP4 -i 正片.MP4 -stream_loop -1 -i "E:\音频\WindHill钢琴版.mp3" \
  -filter_complex "[0:v]fps=30,scale=720:495:flags=lanczos,pad=720:1280:0:(oh-ih)/2:black,format=yuv420p,setsar=1,settb=AVTB[v0];[1:v]fps=30,scale=720:1280:flags=lanczos,format=yuv420p,setsar=1,settb=AVTB[v1];[2:v]fps=30,scale=720:1280:flags=lanczos,format=yuv420p,setsar=1,settb=AVTB[v2];[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[a0];[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[a1];[2:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[a2];[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[vc][ac];[ac]volume=1.5[acv];[3:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=1.0,atrim=0:<总时长>[bgm];[acv][bgm]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.95:level=false[aout]" \
  -map "[vc]" -map "[aout]" -c:v h264_qsv -b:v 8M -c:a aac -b:a 192k -ar 48000 -ac 2 -r 30 -movflags +faststart "视频成片/最终成片.mp4"
```

总时长 = 片头 + 连接 + 正片时长之和。输出目录为 `E:\codex_one\视频成片`。

## 验证

- 每个 `.MP4` 用 `ffprobe` 确认：片头是 1920×1320、30fps，连接和正片是 1080×1920、30fps；最终成片是 720×1280、30fps，均为 h264 + AAC，时长合理、文件非空。
- 正片渲染前跑 `npx hyperframes check --json`，清除 lint/runtime/layout 阻断项。
