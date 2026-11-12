# liangkeban-zine · 两克伴杂志卡片 Skill

把文章、报告、访谈或论文整理成中文杂志卡片，导出 PNG 与可编辑 HTML/CSS。项目在 [su-zine](https://github.com/doublesq97-ui/su-zine) 的构建、渲染和模板基础上扩展，新增两克伴版式、六套配色与布局检查。上游保留部分、改编部分和新增功能的区别，见下方“来源与许可”。

## 能做什么

- 两克伴杂志模式：1080 × 1920（9:16），双栏文字、图表、封面和紧凑页脚；并非默认 3:4。
- 右上角固定品牌 `「两克伴」出品`，右下角独立页码。
- 原版兼容模式：保留 su-zine 模板与 JSON 模块，1200px 宽、自然高度。
- 原版配色之外提供瓷青蓝、森林墨绿、经典墨黑、牛皮纸棕、克莱因蓝、安全橙。
- 以安全结构化节点组合内容，支持本地图片；导出前检查溢出、重叠、缺图、品牌和页脚。
- 可编辑中间文件、来源说明、署名与许可随输出一起保存。

这不是一键抓文章的网站，也不会自动上传或发布内容。脚本只负责本地排版与渲染；资料收集、内容整理及可选插画生成由使用 Skill 的智能体和用户完成。

## 安装

需要 Python 3.10+、Node.js 20+、npm，以及 Google Chrome 或 Playwright Chromium。推荐中文字体 Noto Sans SC 和 Songti SC；字体不随仓库分发，不同系统可能有排版差异。

安装到 Codex 的个人 Skill 目录（目标目录已有文件时不要覆盖）：

```bash
git clone https://github.com/kingqiu/liangkeban-zine.git ~/.codex/skills/liangkeban-zine
cd ~/.codex/skills/liangkeban-zine
npm ci --ignore-scripts --no-audit --no-fund
```

macOS 会优先使用 `/Applications/Google Chrome.app`。其他系统可安装 Playwright Chromium：

```bash
npx playwright install chromium
```

也可以通过 `CHROMIUM_PATH` 指定浏览器可执行文件。打开新的 Codex 会话后，明确要求“用 liangkeban-zine 做卡片”。Skill 名称和触发说明在 [SKILL.md](SKILL.md)。

**写作依赖：** 整理或改写正文时，Skill 要求加载用户自行安装的 `writing-styles`；本仓库不包含它，也不提供其授权。如果没有该依赖，应明确说明，不能声称使用过。直接渲染已有 JSON 或纯换色不需要改写正文。

## 快速试跑（不需要 API key）

在仓库根目录运行：

```bash
python3 scripts/build.py examples/demo/content.json --out output/demo --theme indigo-porcelain
node scripts/render.cjs output/demo --scale 1
```

查看 `output/demo/page-01.png`、`page-02.png` 及同名 HTML。`qa-phone/` 保存手机尺寸预览；`render-report.json` 保存布局检查结果。示例图是通用示意图，不含私人文章或真实统计数据。

输出目录必须全新或为空。再次运行使用新目录，例如 `output/demo-v2`；不要盲目覆盖已有成稿。`--scale 2` 输出 2160 × 3840 PNG，版式比例不变。

## 配色

| 名称 | --theme 参数 |
| --- | --- |
| 原版 | original |
| 瓷青蓝 | indigo-porcelain |
| 森林墨绿 | forest-ink |
| 经典墨黑 | ink-classic |
| 牛皮纸棕 | kraft-paper |
| 克莱因蓝 | ikb |
| 安全橙 | safety-orange |

换配色只改变样式，不改变已确认文案、图表数据和页面顺序。位图插画中的颜色不会随 CSS 自动改变。完整色值见 [palettes.json](assets/palettes.json)。

## 原版模式

```bash
python3 scripts/build.py source/su-zine/assets/example.json --profile original --out output/original
node scripts/render.cjs output/original --scale 1
```

原版入口和上游说明保存在 [source/su-zine](source/su-zine)。上游快照固定为 `a877f7f76adb64278d22716f31e28138bfc6724c`，不会自动更新。

## 自己准备内容

从 `examples/demo/content.json` 复制到独立工作目录，再替换标题、正文、图片和每页 `source`。图片放在该 JSON 旁的 `assets/` 中，支持 PNG、JPEG、WebP。禁止绝对路径、目录穿越、外部软链接和网页脚本。

- [内容格式与运行方式](references/production.md)
- [组件](references/components.md)
- [封面构图变化](references/cover-variety.md)
- [写作边界](references/writing-boundaries.md)
- [原版 JSON 格式](source/su-zine/references/content-schema.md)

正式交付仍需逐页看大图和手机预览，核对来源、数据口径、专名与引语。脚本检查不能替代事实核查和人工视觉检查。

## 目录

```text
SKILL.md              Skill 入口
agents/               Codex 展示配置
assets/               样式与配色
scripts/              构建器、渲染器、组件辅助函数
references/           工作规范、格式与上游哈希清单
examples/demo/        可公开的两页演示
source/su-zine/       完整上游快照（保留原许可）
tests/                本地回归测试
LICENSES/             完整许可及第三方声明
```

## 测试

```bash
npm test
python3 -m unittest discover -s source/su-zine/tests -v
node --test source/su-zine/tests/render.test.cjs
```

上游浏览器测试不会自动选择 macOS Chrome。如果未安装 Playwright Chromium，可运行 `CHROMIUM_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" node --test source/su-zine/tests/render.test.cjs`。

`npm test` 包含上游快照哈希检查和本地节点/路径安全检查。布局渲染检查通过上面的 build + render 命令完成。此发布版验证范围见 [QA.md](QA.md)。

## 隐私与密钥

本地构建和渲染**不需要 API key，也没有内置付费模型调用**。可选的模型/生图工具由宿主自行配置，不要将其密钥写入本仓库或 content.json。

仓库不包含 node_modules、用户的私人文章/发布文案/封面、浏览器会话或本地缓存；`.gitignore` 排除常见凭据和输出文件。忽略规则不能替代检查，详见 [PRIVACY.md](PRIVACY.md)。

## 来源与许可

### 哪些来自上游，哪些是本项目新增

- **原样保留：** `source/su-zine/` 包含 Su（@Sukiea1008）的 su-zine 固定版本，共 45 个文件，涵盖源码、模板、文档、示例、测试和许可。文件内容保持不变，仅将上游 Skill 入口改名为 `UPSTREAM-SKILL.md`。版本与哈希记录见 [upstream-manifest.json](references/upstream-manifest.json)。
- **基于上游改编或复用：** 根目录的构建器仍调用上游构建与模板逻辑，并复用上游 CSS；渲染器在上游基础上增加了检查与导出能力。因此，这不是完全从零编写、与上游无关的实现。
- **本项目新增的功能与内容：** 两克伴品牌和杂志版式、紧凑页脚、结构化布局节点、六套配色适配、封面构图规则、附加校验，以及通用演示与使用说明。这些增量应与上游贡献区分；“新增功能”不意味着其中复用的代码或模板脱离原许可。详细改动及配色来源见 [MODIFICATIONS.md](MODIFICATIONS.md)。

### 适用许可

- 上游代码和模板，以及本项目对其改编、复用的部分，保留 [PolyForm Noncommercial 1.0.0](LICENSES/PolyForm-Noncommercial-1.0.0.txt) 的适用条件。
- 上游原文档、示例文字及其改编部分，保留 [CC BY-NC 4.0](LICENSES/CC-BY-NC-4.0.txt) 的适用条件。
- 新增文件、混合输出和第三方材料的具体范围按现有 [LICENSE-SCOPE.md](LICENSE-SCOPE.md) 与 [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) 执行。这份说明不改变已有许可，也不把新增独立内容的权利归给上游作者。

由于项目包含上述非商业许可材料，不能将整个仓库视为可自由商用或符合 OSI 定义的开源项目。超出适用许可范围的用途，需要向相应权利人另行取得授权。

### 署名与素材权利

Required Notice: 分享自 Su 𝕏 @Sukiea1008

对外分享包含上游材料或其改编内容的代码、模板和卡片时，应保留适用许可和署名；卡片的配文或随附说明需包含上述 Required Notice。页脚的许可链接不能代替作者署名。完整要求见 [NOTICE.md](NOTICE.md) 和对应许可正文。

用户自己的独立文章、品牌内容及第三方素材各自保留原权利，不因使用本工具而归属于 Su；使用渲染器也不会自动取得文章、图片或字体的使用许可。

这是独立维护的改编项目，不代表 Su 对本项目的认可或背书。
