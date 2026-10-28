# Hypit 作者化与渲染（踩坑记录）

模板工程：`E:\vibe大赏\hypit-project`。新主题 = 复制整个目录，改 `productions/knowledge-curse/authors/main.svml` 的窗口/字幕/图形，其余保留。

## 关键依赖已就绪

- `@hypit/hypit` 全局已装，`hypit` 命令可用。
- 渲染浏览器：自管 Chrome Headless Shell，`browserDownloadBaseUrl=https://cdn.npmmirror.com/binaries/chrome-for-testing`（见 `local` profile）。
- ffmpeg：本机 ffmpeg 无 libx264，已用 imageio-ffmpeg 自带 ffmpeg（`D:/Program Files (x86)/python/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe`），写入 `local` 的 `ffmpegPath`。
- 中文字体：`productions/knowledge-curse/assets/NotoSansSC-VF.ttf`，用 `media:Font` 引用；不要用 fontsource（CJK 按 unicode-range 切片会加载失败）。

## SVML 骨架（main.svml 要点）

- 头部 `<?svml using="@hypit/markup@1"?>`；imports：film、text（text-fine）、space、time、html、media、mediaop、audio、wave（自定义包 `@knowledge-curse/tap-wave@1`）、look（recipes.svs）。
- `space:Canvas` + `time:Clock` + `time:Timeline`（`end="start+122s"`，内部 `time:Window from/until` 定义每个画面窗口）。
- `media:Font`（本地 TTF）+ `media:Audio` + `mediaop:Normalize`（bgm 归一）。
- `text:Style`（recipe 定 size/weight，`text:Fill/Glow` 定颜色）+ `text:Motion`（`ItemKeyframe` 的 at/x/y/scale/rotate/blur/opacity）+ `text:Flow`（`during` 窗口、`motion` 入场、双语字幕）。
- `audio:Track` + `audio:Clip`（bgm，`fade-out` 用帧，如 105f=3.5s）。
- `film:Film`（`appearance` 底色）+ 每个 `film:Track source={...visual|...audio}`。
- `html:Video id="final"` 发布 `final.video`，run 里 `<target output="final.video"/>`。

## 图形组件（每个新主题都要重新生成，禁止复用）

- 包：`packages/tap-wave`，模块 `@knowledge-curse/tap-wave@1`；SVML 里以 `<wave:*>` 实例化。
- 模板自带的 11 个表面（Wave/Seal/BookCard/Timeline/Perspective/Badge/Knock/Mind/Steps/Bridge/Quote，+ Backdrop 背景）只作**代码结构参考**，不是可复用素材库。每个新主题必须重新设计并实现一套主题专属图形（约 8–11 个），不得沿用模板或上一个视频的图形。
- 每个组件 = `manifest.ts`（type/producer/surface）+ `fragment.ts`（GraphFragment）+ `surface.ts`（decode 路由）+ `component.ts`（render 函数，`sealVisualTrack` 输出 VISUAL_IR）+ `activation.ts`。
- VISUAL_IR 元素仅 box/text/image 等；动画是 `animation.keyframes`（atFrame + style），可动画样式只有 opacity/transform/filter/clip-path 等。
- 生成新图形：
  1. 按主题核心意象列出图形清单（如“手性”主题可用：镜像分子对、左右手、晶体分拣、催化放大曲线、自催化闭环、药物-靶点手套契合等）。
  2. 每个图形照抄一个现有组件的代码骨架，改 `tag`、`manifest.ts` 描述与 `component.ts` 的 render 函数，画出新图形。
  3. 在 `surface.ts` 路由、`index.ts` 导出、`component.ts` 的 producers/validators 里登记新组件。
  4. `cd packages/tap-wave && npm run build`，再回项目根 `hypit build`。
- SVML 里 `<wave:Xxx id="..." timeline={film-time.timeline} within={frame} during={film-time.w-xx}/>` 实例化，并加 `film:Track source={xxx.visual}`。

## 图形与文字避让（必须遵守）

- 字幕（`text:Flow`）是画面主体，图形永远不能压住文字，也不能和文字同色。
- 常用空白带（`space:Frame`）：居中字幕时，大/圆形图形放右侧 `frame-g-right`（left 70% top 22% right 97% bottom 76%）；横向条形、点状或小型图形放下方 `frame-g-wide`（left 10% top 62% right 90% bottom 94%），需要完全避开底部字幕时用更低的 `frame-g-low`（left 10% top 72% right 90% bottom 96%）。
- 实心大图形若必须贴近文字，改成描边风格：`border: 4px solid color` + `background-color: ${color}12`（约 7% 透明填充），不要把整块实心色块垫在文字正后方。
- 颜色避让：图形颜色不得与重叠文字同色（例如金色标题 `#E8C878` 不能叠在金色实心图形上，否则标题会被“吞掉”）。
- 已踩坑：① 标题用了金色实心“左右手”，金标题叠金手掌导致标题不可读 → 改描边 + 低透明度；② “自催化闭环”的环与大圆点居中压住两行字幕 → 移到右侧空白带 `frame-g-right`。
- 渲染后自查：用 ffmpeg 抽关键帧，检查字幕区域不应出现图形颜色像素（例如中心文字区不应有金/青色图形块）。

## 踩坑（必须遵守）

1. Track id 必须全局唯一：同一组件多次实例化时，`sealVisualTrack` 的 `id` 加 `-${window.span.startFrame}` 后缀，否则报 `FilmTrackSet already contains Track id ...`。
2. Present 内 order 必须全局唯一且递增：root order 0，其余元素用同一个计数器递增。
3. 元素坐标相对父级：子元素 left/top 相对其 `parent`，不是画布绝对坐标；root 用 `within.xPx/yPx` 定位。
4. 字体：用 `media:Font src="../assets/NotoSansSC-VF.ttf"`；fontsource 的 CJK 可变字体会渲染失败。
5. 编码器：本机 ffmpeg 无 libx264 会 EPIPE；用 imageio-ffmpeg 的 ffmpeg 写入 profile 的 `ffmpegPath`。
6. 浏览器：系统 Chrome/Edge 常驻时 `--version` 探测被劫持；用自管 headless shell + 镜像。
7. 文本入场：text-fine `ItemKeyframe` 支持 x/y/scale/rotate/skew/blur/clip/opacity；要“依次进入”就加 hold（两帧同值）+ 错开的 at。

## 命令

```bash
cd <project>
hypit check productions/knowledge-curse/runs/render.svrun
hypit plan  productions/knowledge-curse/runs/render.svrun
hypit build productions/knowledge-curse/runs/render.svrun --follow
hypit get <build-id> --output final.video --to <out.mp4>
```

改 `packages/tap-wave` 源码后：`cd packages/tap-wave && npm run build`，再回项目根 `hypit build`。
