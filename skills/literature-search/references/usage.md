# 检索命令与候选处理

执行检索、解析 DOI 或整理字段时，按需读取对应部分。命令以技能目录为工作目录，输出写入用户项目。

## 查询命令

简单查询：

```powershell
python scripts/literature_search.py search --query "robust vehicle routing" --sources openalex crossref arxiv --limit 10 --out "<项目路径>/literature/run-01"
```

不同来源的检索语法不相同。复杂查询使用 [references/search-plan.example.json](search-plan.example.json) 的数组结构，模型在项目内另写本次计划，每个条目明确一个来源、一条检索式及可选年份范围：

```powershell
python scripts/literature_search.py search --plan "<项目路径>/literature/plan.json" --out "<项目路径>/literature/run-02"
```

`--limit` 是每个来源每条查询的获取上限，最大 100，脚本不自动翻遍整个数据库。不把返回数量当数据库总命中数或穷尽性证明。覆盖不足时扩充检索式、来源，或使用实际可用的原生分页工具；达到用户范围或新增相关结果明显减少时收束。

## 从机器结果到候选文献

脚本输出 `candidates.json`、`candidates.md`，保留检索日志、来源状态和原始来源记录。结果是待筛候选，不是已经完成相关性判断的交付物。

- 阅读标题与可用摘要，区分直接相关、方法可借鉴、背景相关、待判断，给出简短理由。不仅按词面匹配淘汰，也不以引用量、期刊名气替代相关性。
- 缺 DOI、摘要或开放全文不自动淘汰。抽取不到的字段写“未获取”；原始摘要、中文译文和模型概述分开，搜索片段不冒充摘要。
- 精确标识符优先去重；无标识符时仅保守匹配规范化标题、完整作者列表、年份和类型。模糊匹配交给模型进一步核对。不同 DOI 保留；预印本与正式版本保留关系、日期与来源记录。
- `matched_records` 只表示记录匹配，不表示论文结论已核实。不同聚合库可能共享上游数据，不能当作独立学术证据。
- 需要核对 DOI 书目或补开放全文链接时，使用：

```powershell
python scripts/literature_search.py resolve --doi "10.1038/nature14539" --out "<项目路径>/literature/doi-details.json"
```

该命令先查 Crossref，未收录时尝试 DataCite；设置统一邮箱后查 Unpaywall。Crossref 404 不是 DOI 无效的证明，仍可沿 DOI 原文页继续核对。脚本不下载全文；`source_reported` 链接仅是来源报告的位置，未验证本机能打开或下载。

交付候选清单时保留标题、完整作者、年份、期刊/会议、摘要、DOI、原文 URL、全文链接、相关理由及来源。大批量可在正文给重点候选，完整字段放文件；需要增补筛选结果时另写 `screened-candidates.json` 或说明文件，保留原始候选与日志。

部分来源失败时交付已有结果并说明缺口，不将失败记作零命中；全部失败时先处理环境。零命中只能说明“在本次来源和检索式下未找到”，不能断言研究空白。
