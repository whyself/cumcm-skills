# 整合来源与调整

原始资料位于 preMCM 的 `skill/` 目录。以下路径用于维护溯源，不是运行依赖；本 Skill 拷贝到其他目录后无需访问它们。

| 原始路径 | 吸收内容 | 本包实质调整 |
|---|---|---|
| `nature-skills/skills/nature-academic-search/references/search-strategy.md` 与 `references/workflows/wf1-multi-source-search.md` | 概念扩词、多源检索、统一输出、回退 | 改为按学科和实际可用性选源，不机械按 T1/T2/T3 排序或固定配额 |
| `nature-skills/skills/nature-academic-search/scripts/academic_search.py` | 标准库直接调用、OpenAlex 摘要重建和书目字段 | 新增 Key 读取，不沿用名义上的“无 Key 即可规模检索”；不按引文量硬过滤 |
| `math-modeling-skill/tools/paper_search/scripts/` | 来源并发、书目融合、可追溯记录 | 不强制 AnySearch；统一错误状态、保守去重和每来源记录保留，取消词面硬淘汰 |
| `cumcm-step-review/tools/paper_search/scripts/` | 同上 | 与上项对应脚本相同，不重复引入 |
| `nature-skills/skills/nature-academic-search/mcp-server/sources/{crossref,arxiv,pubmed}.py` | 对应 API 请求字段、Atom/XML 元数据映射 | 使用统一标准库 HTTP 和配置层，不要求 MCP、requests 或 pybliometrics |
| `nature-skills/skills/nature-citation/references/search-strategy.md` | 对象/关系/情境拆分、同义词与宽泛查询 | 不限制 Nature/CNS，不把候选文献当作主张支撑 |
| `nature-skills/skills/nature-literature-pipeline/` | 初筛、来源降级、证据层级、检索记录 | 不加入定时推送、强制六维打分、全文精读或“零命中证实空白” |
| `nature-skills/skills/nature-ref-verifier/` | 标题/作者/年份/DOI 对应检查 | Crossref 未收录时用 DataCite 补查，并保留未解析状态，不判定 DOI 必错 |
| `nature-skills/skills/nature-downloader/scripts/lib/open-access.mjs` | Unpaywall DOI 查询与 OA 位置字段 | 只定位链接，不自动下载；统一邮箱，取消中文仅 CNKI 路由 |
| `Enhanced-mathmodel-Codex-skills/skills/authoritative-data-harvester/SKILL.md` | API 优先、参数记录、限速与失败区分 | 面向文献字段，不引入数据清洗/写论文/强制记忆更新流程 |

代码按上述字段映射和流程重新整合为自包含实现，未直接复制整套上游服务器。Semantic Scholar 适配器、统一六项配置、隐藏输入、Windows 环境准备和行为测试用于补齐现有缺口。

设计同时遵循项目 `研究成果/数模skill制作原则.md`：模型自行判断相关性与检索覆盖；不将库列表变成封闭清单，不添加逐项审批或固定篇数门槛。

接口参数可能随服务更新而变化。修改时以实时官方文档与小规模接口检查为准，不在 Skill 固定承诺免费额度或响应速度。OpenAlex 鉴权参考 https://help.openalex.org/api/authentication/ ；其余官方入口在环境与来源表中。

## 2026-09-08 验证记录

- Windows / Python 3.13.7：`setup.ps1` 检测现有 Python 与离线自检成功；未实测无 Python 机器上的 winget 安装分支。
- 21 项离线行为测试通过：配置优先级与保密、元数据解析、DOI/版本去重、部分失败、Key 传递、共享邮箱、DOI 注册机构回退、输出防覆盖与限流处理。
- 无 Key 实时查询：OpenAlex、Crossref、arXiv 成功；`robust vehicle routing` 每源获取 3 条，共输出 9 条待筛候选。候选已检查能保留完整来源摘要及缺失字段，相关性仍由使用 Skill 的模型判断。
- Crossref DOI 查询 `10.1038/nature14539` 成功，返回标题 Deep learning、三名作者及年份 2015。
- Semantic Scholar 匿名请求返回 429；PubMed 因缺统一邮箱返回 `needs_configuration`；Unpaywall 因同一原因未请求。这些来源的带凭据实时能力尚未验证，不能把离线样例测试当作真实账号联通。
- Skill 元数据校验与内部 Markdown 链接检查通过。此记录是当时环境快照，后续使用以 `doctor` 和实际请求为准。
