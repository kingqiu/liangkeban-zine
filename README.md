# liangkeban-zine · 两克伴杂志卡片 Skill

把文章、报告、访谈或论文整理成中文杂志卡片，导出 PNG 与可编辑 HTML/CSS。基于 [su-zine](https://github.com/doublesq97-ui/su-zine) 改编，保留上游完整快照，并增加两克伴版式、六套配色和布局检查。

> 分享自 Su 𝕏 @Sukiea1008。**本项目是非商业源码可见项目，不是 OSI 定义的开源项目，也不授予自由商用权。** 代码和模板适用 PolyForm Noncommercial 1.0.0；原文档和示例文字适用 CC BY-NC 4.0。详见下方许可说明。

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

## 许可与署名

- 代码/模板： [PolyForm Noncommercial 1.0.0](LICENSES/PolyForm-Noncommercial-1.0.0.txt)
- 原文档/示例文字： [CC BY-NC 4.0](LICENSES/CC-BY-NC-4.0.txt)
- 范围：[LICENSE-SCOPE.md](LICENSE-SCOPE.md)；署名：[NOTICE.md](NOTICE.md)
- 改编说明：[MODIFICATIONS.md](MODIFICATIONS.md)；第三方声明：[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)

对外分享卡片时，配文或随附说明须保留 `分享自 Su 𝕏 @Sukiea1008` 和适用许可。页脚的许可链接不能代替作者署名。用户自己的独立内容和第三方素材各自保留原权利；使用渲染器不会自动取得文章、图片或字体的许可。超出许可范围的用途须向相应权利人另行取得授权。

这是独立改编，不代表 Su 对本项目的认可或背书。
