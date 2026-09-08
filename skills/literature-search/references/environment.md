# 安装与配置

## 基础环境

只需 Python 3.10+ 和能访问所选来源的网络，推荐仍受支持的 Python 3.13。脚本没有第三方 Python 依赖，因此不需要 requirements.txt、pip 安装或专用虚拟环境。可以使用已有 Python 或 uv 管理的 Python。

官方安装包不随 Skill 分发，以免版本过时或混入平台不匹配的二进制。

| 环境 | 操作 |
|---|---|
| Windows，已有 Python | 在 Skill 目录执行 `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/setup.ps1` |
| Windows，没有 Python | 执行同一命令并加 `-InstallPython`；脚本通过 winget 安装用户级 Python 3.13 |
| Windows，没有 winget 或安装失败 | 提醒用户从 https://www.python.org/downloads/windows/ 安装并勾选 PATH，然后重新打开终端/宿主程序 |
| macOS | 使用 https://www.python.org/downloads/macos/ 的官方安装包，已有 Homebrew 时也可 `brew install python` |
| Linux | 使用发行版包管理器安装 Python 3.10+；例如适用版本的 Debian/Ubuntu 可 `sudo apt-get install python3`，安装后确认版本 |
| 只有 `python3` 命令 | 将 Skill 示例中的 `python` 换为 `python3` |

`ExecutionPolicy Bypass` 只作用于该次 PowerShell 进程，不要求修改系统执行策略。安装程序、提升权限或组织管控失败时，说明实际原因并给用户官方安装入口，不假定程序已经装好。

## 收拢后的六项配置

| 环境变量 | 私有 JSON 字段 | 必要性及用途 | 获取方式 |
|---|---|---|---|
| `LITERATURE_EMAIL` | `email` | 推荐先配；PubMed 和 Unpaywall 分支需要，Crossref 用于联系标识 | 用户真实邮箱，一个邮箱供三个源共用 |
| `OPENALEX_API_KEY` | `openalex_api_key` | 推荐先配，基础匿名请求可先运行 | https://openalex.org/settings/api |
| `SEMANTIC_SCHOLAR_API_KEY` | `semantic_scholar_api_key` | 可选；缺失时可尝试匿名访问，遇限流切换来源 | https://www.semanticscholar.org/product/api ，申请与审核由用户完成 |
| `NCBI_API_KEY` | `ncbi_api_key` | 可选；PubMed 的 API 额度增强 | https://www.ncbi.nlm.nih.gov/account/ ，登录账号设置创建 |
| `HTTP_PROXY` | `http_proxy` | 网络需要时配置 | 用户实际 HTTP 代理地址，不假定端口 |
| `HTTPS_PROXY` | `https_proxy` | 网络需要时配置 | 用户实际 HTTPS 请求代理地址，值通常也以 `http://` 开头 |

“6 个变量”是最大配置接口，不是六个都必须填写。推荐先填邮箱和 OpenAlex Key，后续按需要再加。无需分别设置 `PUBMED_EMAIL`、`UNPAYWALL_EMAIL`、`OPENALEX_MAILTO` 和 `CROSSREF_MAILTO`；这份新 Skill 不读取这些旧变量，也不改动旧技能的配置。

Python 标准库直接支持 HTTP/HTTPS 代理；SOCKS 地址不在本包支持范围，提醒用户提供 HTTP 代理端口或使用可用的其他网络路径。不要关闭 TLS 证书校验来解决网络问题。

## 推荐：写入用户私有配置

配置默认存放在 `~/.config/literature-search/config.json`，不放在 Skill、Git 仓库或候选文献目录。以当前 Windows 用户为例，`~` 是该用户的主目录。

```powershell
python scripts/configure.py --init
python scripts/configure.py --set email
python scripts/configure.py --set openalex_api_key
python scripts/configure.py --show
python scripts/literature_search.py doctor
```

`--set` 在交互终端使用隐藏输入，空值取消，修改一个字段时保留其他字段。模型应提示用户在自己的终端完成输入，不要在无人可输入的工具会话里等待隐藏提示。`--show` 和 `doctor` 只输出配置是否存在，不显示值。

也可使用用户本地编辑器填写 [config.example.json](../config.example.json) 所示的六个字段，但实际配置必须另存到私有位置；不要把密钥填进分发模板。

非交互、远程或已经统一管理环境变量的环境，可直接注入上表变量。**非空环境变量优先于配置文件**。配置脚本不修改用户/系统环境变量。它以私有文件代替重复设置多个邮箱变量；POSIX 上写入时使用 `0600`，Windows 继承用户目录 ACL，不声称 `chmod` 能代替 Windows ACL。

自定义文件通过 `--config` 指定，无需新增第七个环境变量：

```powershell
python scripts/configure.py --config "<私有目录>/config.json" --init
python scripts/literature_search.py --config "<私有目录>/config.json" doctor
```

本包**不加载 `.env` 文件**。不将密钥放入命令行值、检索计划、运行日志或候选 JSON；不要打印整个环境。

## 实际连通性检查

```powershell
python scripts/literature_search.py doctor --live --sources openalex crossref arxiv
python scripts/literature_search.py doctor --live --sources semantic pubmed
```

离线 `doctor` 只验证运行环境和配置存在性；实时模式每源进行一次小规模检索，PubMed 会再请求一次详情，可能计入服务额度。它不会检查机构权限、登录状态或全部接口；Unpaywall 在有具体 DOI 和邮箱时用 `resolve` 检验。

主要连接地址：

- OpenAlex：`api.openalex.org`
- Crossref：`api.crossref.org`
- arXiv：`export.arxiv.org`
- Semantic Scholar：`api.semanticscholar.org`
- PubMed：`eutils.ncbi.nlm.nih.gov`
- DOI 兜底：`api.datacite.org`、`doi.org`
- 开放全文链接：`api.unpaywall.org`，实际原文链接还可能位于出版商或仓储域名

脚本对每个来源限速，默认超时 20 秒、最多重试一次；429 或服务端故障有限重试，较长 Retry-After 交回模型处理。缓存仅存在于本次进程内，避免同一运行重复请求，不写带 Key 的请求 URL 到磁盘。检索结果和每轮日志写到项目目录，增量检索时读取前轮记录减少重复劳动。

| 状态 | 模型应做什么 |
|---|---|
| `needs_configuration` | 指明缺少字段和设置命令，只影响该来源，其他可用源继续 |
| `unauthorized` | 提醒核对该来源 Key；不打印值，也不反复重试 |
| `forbidden` | 说明可能涉及接口权限或访问限制，不能仅凭 403 判断 Key 错误 |
| `rate_limited` | 遵守服务提示稍后再试，或先换源，不循环轰炸接口 |
| `network_error` | 检查代理、DNS、TLS、超时；区分本机网络问题与无文献 |
| `invalid_query` / `invalid_response` | 检查检索语法或适配器变化；不伪装为零命中 |
| `empty` | 该查询正常完成但无返回，可扩词或换源 |
| `partial` | 保留已获取文献，同时报告失败来源和覆盖缺口 |

`search` 的退出码：0 表示至少一个来源正常完成（可能部分失败或结果为空），2 表示全部失败或输入/文件错误；调用方还必须读取 JSON 的 `status` 与 `search_log`。实时 `doctor` 只要所选源有失败便返回 2。`resolve` 至少找到一条元数据或全文位置才返回 0；字段缺失与失败详情在输出 JSON 中。

## 不能封装成通用安装包的部分

中文数据库和机构资源不是基础环境依赖，只在主题需要时启用。

| 来源/程序 | 是否内置 | 何时提醒用户、提醒什么 |
|---|---|---|
| 知网、万方、维普 | 网站选源提示；无内置自动检索适配器 | 中文主题需要补充而当前工具不可访问时，请用户提供实际图书馆数据库入口；需要时在受控浏览器登录 |
| Google Scholar、百度学术 | 无内置官方搜索 API | 先检查已有网页搜索/浏览器工具；不可用时说明缺口，提供可执行检索式，不假定配置一个 Key 即可解决 |
| Scopus、ScienceDirect | 本包不接入 pybliometrics | 用户需要该源且现有工具不支持时，说明需 Elsevier 开发者 Key、API 授权；网页全文还可能需机构权限 |
| IEEE Xplore、ACM DL、其他出版商 | 优先通过可用网页工具访问 | 需要机构全文时提示登录或授权；元数据 Key 不等于全文权限 |
| AnySearch | 本包不作为默认依赖 | 仅在环境已经提供可用连接器或用户明确要接入时启用；需单独验证服务、计费、凭据与适配器 |
| 浏览器及其控制工具 | 不随包安装，也不默认打开远程调试端口 | 只有网页分支才需要；沿用宿主提供的工具。确实没有工具时提醒配置受支持的浏览器渠道，而非要求安装本包未使用的驱动 |

机构账号、数据库订阅、Key 审核和用户登录不能由静态 Skill 代办。缺失时给出该来源的具体操作，不要求为了普通公开 API 检索去准备全部这些环境。
