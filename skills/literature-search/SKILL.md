---
name: literature-search
description: 根据主题、关键词或模型提出的检索需求扩展中英文检索词，调用可用学术来源进行多源检索、基本相关性筛选、去重和书目补全，返回标题、作者、年份、摘要、DOI、原文与可获取全文链接。用于查文献、找论文、搜方法出处、扩大候选文献范围；不自动开展全文精读、综述写作或批量下载。
---

# 文献检索

帮助用户获得相关、可追溯的候选文献。模型负责理解需求、扩词、选源和判断相关性；脚本负责请求、解析、去重和记录。保留可能相关但证据不足的候选，不把基础检索变成全文阅读或完整引用审计。

## 先让工具能运行

`SKILL_ROOT` 是本文件所在目录；下面的命令以它为工作目录，结果放到用户项目。安装到其他位置后仍使用本目录内的相对脚本。

首次使用或环境变动时：

```powershell
python scripts/literature_search.py doctor
```

- 唯一基础运行依赖是 **Python 3.10+**，全部脚本使用标准库。无需 pip 安装、Node.js、uv、浏览器驱动或 MCP 服务器。
- Python 不可用或版本不足：Windows 运行 [scripts/setup.ps1](scripts/setup.ps1)，需安装时加 `-InstallPython`；其他系统按 [环境配置](references/environment.md) 安装。
- 只有 **6 个可配置环境变量**，建议先准备 `LITERATURE_EMAIL` 和 `OPENALEX_API_KEY`；另外四个按来源与网络需要配置。没有环境变量也能用用户私有 JSON 配置文件。
- [scripts/configure.py](scripts/configure.py) 提供初始化、隐藏输入和配置状态检查。Key 和邮箱不放入 Skill 源文件、检索计划、结果或对话输出；实际值由本机配置提供。
- `doctor` 只检查运行与配置状态，不代表联网可用。需要验证来源时执行 `doctor --live --sources openalex crossref arxiv`，或者只检查本次要用的源。
- 自检缺少 **可选** Key 时，可用匿名公开来源先继续，不要求用户一次配齐所有账号。PubMed 或 Unpaywall 分支需要邮箱，进入该分支时才提醒补设。
- 需要用户操作时，说明“哪个来源缺什么、在哪里设置、会影响什么”，给出对应命令或官方入口。账号申请、Key 审核、机构授权、交互登录由用户完成；已有配置与授权直接使用，不重复询问。

详细安装、六项变量映射、网络诊断、Key 申请和外部数据库条件统一在 [references/environment.md](references/environment.md)，遇到缺配置或新来源时读取。

## 检索与选源

将研究问题拆为对象、任务、方法与应用场景，补中英文同义词、缩写和全称。优先翻译科学概念，不机械翻译整句。精确查询、同义词查询和放宽查询可逐轮使用，保留用户的硬性时间、语言与文献类型限制。

按学科选择互补来源，参考 [references/sources.md](references/sources.md)。内置直接检索：OpenAlex、Crossref、arXiv、Semantic Scholar、PubMed。中文来源、工程会议库和机构数据库通过实际可用的网页工具补充；网站在参考表里不等于已有可调用接口。

简单查询：

```powershell
python scripts/literature_search.py search --query "robust vehicle routing" --sources openalex crossref arxiv --limit 10 --out "<项目路径>/literature/run-01"
```

不同来源的检索语法不相同。复杂查询使用 [references/search-plan.example.json](references/search-plan.example.json) 的数组结构，模型在项目内另写本次计划，每个条目明确一个来源、一条检索式及可选年份范围：

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

## 脚本与维护

| 文件 | 作用 |
|---|---|
| [scripts/setup.ps1](scripts/setup.ps1) | Windows 检测 Python；显式加参数时安装 Python、初始化配置 |
| [scripts/configure.py](scripts/configure.py) | 创建私有配置、隐藏输入、只显示配置是否存在 |
| [scripts/literature_search.py](scripts/literature_search.py) | `doctor` / `search` / `resolve` 统一入口，结果与日志输出 |
| [scripts/providers.py](scripts/providers.py) | 五个直接检索源，Crossref/DataCite DOI 元数据及 Unpaywall 链接 |
| [scripts/runtime.py](scripts/runtime.py) | 六项配置读取、请求限速、有限重试、进程内请求缓存 |
| [scripts/test_literature_search.py](scripts/test_literature_search.py) | 离线行为测试，无需 Key 或网络 |

修改脚本后运行 `python -m unittest discover -s scripts -p "test_*.py"`，涉及接口时对相应来源做少量实时自检。来源选择见 [references/sources.md](references/sources.md)。
