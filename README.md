# CUMCM Skills · 数学建模技能库

面向国赛（CUMCM）的六个独立 AI 技能，支持从文献检索、建模讨论到论文表达的协作，可按需单独使用或组合使用。

## 功能说明

| 技能 | 功能 |
| --- | --- |
| [literature-search](skills/literature-search/SKILL.md) · 文献检索 | 扩展检索词，在 OpenAlex、Crossref、arXiv、Semantic Scholar、PubMed 中检索，去重并补全书目、摘要及可获取的全文链接。 |
| [cumcm-modeling](skills/cumcm-modeling/SKILL.md) · 建模协作 | 分析题意与附件、比较模型路线、解释假设和公式、细化求解方案。附带 7 类、64 个模型与算法参考条目。 |
| [cumcm-result-verification](skills/cumcm-result-verification/SKILL.md) · 结果核验 | 对照题意、模型、代码和输出，检查约束、数值与统计口径，按需独立复算，说明结果可信度及结论范围。 |
| [cumcm-paper-planning](skills/cumcm-paper-planning/SKILL.md) · 论文规划 | 根据已有大纲、模型和结果，安排各节内容、论证顺序、图表与文献，标明需要补充的材料。 |
| [cumcm-plotting](skills/cumcm-plotting/SKILL.md) · 数据绘图 | 根据数据选图、适配模板，生成可运行代码与图片，并检查成图质量。附带 100 个模板文件、89 张预览图和 8 个辅助脚本。 |
| [cumcm-language-polish](skills/cumcm-language-polish/SKILL.md) · 语言润色 | 改善已有中文论文的表达与衔接，保留原意、数字、公式和结论强度。支持纯文本、Markdown 和 LaTeX 正文。 |

## 安装与环境

使用支持 `SKILL.md` 的 AI 助手。仅进行模型讨论、论文规划或文本润色，无需安装计算依赖；运行绘图与复算需要相应的代码执行环境。

### 安装技能

安装脚本需要 **Python 3.10+**。在仓库根目录运行，将六个技能复制到 `~/.agents/skills/`，已有同名目录会跳过：

```bash
python scripts/install.py
```

macOS/Linux 可使用 `python3`。也可手动将 `skills/` 下所需的完整文件夹复制到客户端的技能目录。Codex 的目录说明见 [官方文档](https://learn.chatgpt.com/docs/build-skills)。安装后可用 `$cumcm-modeling` 等技能名调用。

### 文献检索 Key 配置

检索脚本只需要 **Python 3.10+**，无需额外 pip 包。建议先配置邮箱和 OpenAlex Key，其余按所用来源配置：

| 配置字段 / 对应环境变量 | 用途与获取方式 |
| --- | --- |
| `email` / `LITERATURE_EMAIL` | 你的联系邮箱；本工具的 PubMed、Unpaywall 分支需要，Crossref 也会使用。 |
| `openalex_api_key` / `OPENALEX_API_KEY` | OpenAlex 检索，登录 [OpenAlex API 设置](https://openalex.org/settings/api) 获取。 |
| `semantic_scholar_api_key` / `SEMANTIC_SCHOLAR_API_KEY` | 按需在 [Semantic Scholar API](https://www.semanticscholar.org/product/api) 申请。 |
| `ncbi_api_key` / `NCBI_API_KEY` | 可选，用于提高 PubMed 接口额度，在 [NCBI 账户设置](https://www.ncbi.nlm.nih.gov/account/) 创建。 |

在仓库根目录执行以下命令，按提示在自己的终端输入邮箱与 Key，输入内容不回显：

```bash
python skills/literature-search/scripts/configure.py --init
python skills/literature-search/scripts/configure.py --set email
python skills/literature-search/scripts/configure.py --set openalex_api_key
python skills/literature-search/scripts/configure.py --show
python skills/literature-search/scripts/literature_search.py doctor
```

配置其他 Key 时，将 `--set` 后的字段换为表中对应字段。配置保存在 `~/.config/literature-search/config.json`，不要将实际 Key 写进仓库或 `config.example.json`。非空环境变量优先于配置文件；脚本不自动读取 `.env`。需要代理时配置 `HTTP_PROXY` / `HTTPS_PROXY`，或私有配置中的 `http_proxy` / `https_proxy`。

`doctor` 仅检查配置状态；验证连接可运行 `python skills/literature-search/scripts/literature_search.py doctor --live --sources openalex crossref arxiv`。完整说明见[文献检索环境配置](skills/literature-search/references/environment.md)。

### Python 绘图环境

需要 **Python 3.10+、pip**，以及 `requirements.txt` 中的 NumPy、pandas、Matplotlib、seaborn 和 Pillow。在仓库根目录执行：

**Windows / PowerShell：**

```powershell
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -r requirements.txt
```

**macOS / Linux：**

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
```

运行绘图时使用该虚拟环境的解释器。其他配置按任务需要准备：

- **中文字体**：安装或使用 Microsoft YaHei、Noto Sans CJK SC 等中文字体。
- **额外依赖**：Excel 输入、统计分析、机器学习等按所选代码补装，例如 `openpyxl`、`scipy`、`scikit-learn`；无需安装整个模板库的依赖。
- **求解与复算**：沿用项目的 Python、MATLAB 或 R 环境及所需求解器。

绘图模板需按真实数据适配。详细环境检查与补包方法见[绘图环境说明](skills/cumcm-plotting/references/environment.md)。
