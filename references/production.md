# 内容格式与执行

从 Skill 根目录执行；路径用实际工作目录，不依赖某次 Downloads 路径。Python 3.10+、Node 20+、Playwright 1.62.1。macOS 自动使用现有 Google Chrome；其他环境设置 CHROMIUM_PATH 或使用 Playwright Chromium。中文字体推荐已安装的 Noto Sans SC 与 Songti SC；字体未随包分发，换机须核对字体，不能承诺跨机器像素完全相同。

安装依赖（确实缺失且当前授权允许时）：
```bash
npm ci --ignore-scripts --no-audit --no-fund
```

## 普通杂志卡片

```bash
python3 scripts/build.py /绝对路径/content.json --out /绝对路径/output-v1
node scripts/render.cjs /绝对路径/output-v1 --scale 1
```

输出 PNG 是 1080×1920；--scale 2 是 2160×3840。同目录保留 HTML、style.css、content.json、build-report.json、render-report.json、qa-phone/、来源与许可证。不得跳过逐张视觉检查。

根对象：series、brand（必须「两克伴」出品）、pages；可选 profile=magazine、theme=original。每页：title、intro、source（单行本篇出处）、section、layout（body/cover），及 body 节点数组或原版 blocks。字符串是纯文本，换行转 br。Source 在每页动态设置，不提供默认 a16z。图表数据必须附上来源 ledger。

安全节点格式：`{"tag":"p","children":["正文"]}`。节点允许 tag/attrs/children，属性白名单拒绝事件、脚本、外链资源。img 只允许 content.json 所在目录 assets/ 下的 PNG/JPG/WebP；不得引用 ../、绝对路径或外部软链接。inline style 只接受 width/height 的 px/% 和十六进制背景色。SVG 数字图形以节点表达，不导入来源网页 HTML。

## 原版复现

原版所有字段详见 [content-schema.md](../source/su-zine/references/content-schema.md)。
```bash
python3 scripts/build.py source/su-zine/assets/example.json --profile original --out /绝对路径/original-v1
node scripts/render.cjs /绝对路径/original-v1 --scale 2
```
original + original 主题调用未改的上游构建器，生成 HTML/CSS 与上游相同；根构建器只另附来源、许可和报告。也可在 source/su-zine 中按原命令运行其原测试。

## 换色

```bash
python3 scripts/build.py content.json --out output-blue --theme indigo-porcelain
```
主题：original / indigo-porcelain / forest-ink / ink-classic / kraft-paper / ikb / safety-orange。中文全名也可。不要为了换色重写数据或文案。所有主题都可用于两种模式，嵌入位图不自动重绘。

## 公开演示

examples/demo/content.json 是独立编写的两页通用示例，含一张本地示意图，不含私人文章或真实统计数据。先复用结构，再替换全部内容与来源。

```bash
python3 scripts/build.py examples/demo/content.json --out output/demo --theme indigo-porcelain
node scripts/render.cjs output/demo
```

脚本拒绝覆盖现有构建。render 只有显式 --overwrite 才重写 PNG；新版本优先使用新目录。
