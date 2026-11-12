# 两克伴组件

复杂卡片使用 `body` 安全节点而非原始网页 HTML。脚本 `scripts/components.py` 提供 node、p、h2、note、rule、columns、box、metric、flow、bars、donut 生成器，可在你编写的本地内容脚本中导入；它只生成 JSON 对象，不发网络请求。

```python
from components import *
body = [
  columns([h2("一句有依据的小标题"), p("解释原文的行动与事实。")],
          [box("适用范围", "必要年份、地区、样本或限制。")]),
  rule(),
  flow(["读取需求", "比较选项", "完成任务"]),
  note("编辑整理的概念流程，不代表测得比例。")
]
```

如果有真实数据，bars 接受 `[(名称, 数值), ...]`，有统一单位；donut 接受 0–100 的真实百分比。没有数据时不要给概念流程加装饰数字。数据必须对应 sources.md 中一条具体证据。

更多可复用样式类在 assets/magazine.css 和 examples/demo/content.json 中：
- columns / equal：解释与图形的双栏，或等宽双栏。
- box + green/purple/blue/rust：原版柔和四色面板。
- metric-pair / mini-metrics：真实指标横向比较。
- endpoint：两个已知时间点，不虚构中间连线。
- botbars / botstack / forecast：按真实数值分区，预测另标。
- case-diagram：任务、协调者和服务的解释性流程。
- opportunity-map / op-block：分类图，不能冒充数据比例。
- test-step：从资料整理的可执行自检。
- cover-image / cover-note / cover-stats：封面插画、摘要与真实指标。

示例复用的是结构，不是事实。替换每个标签、正文、数值、单位、日期、出处以及图片 alt。复杂节点可直接编辑 JSON 或由本地脚本生成；不要把任意文章 HTML 原封不动灌入。
