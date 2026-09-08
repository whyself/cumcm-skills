# 脚本维护

仅在修改或排查检索脚本时读取。

## 脚本与维护

| 文件 | 作用 |
|---|---|
| [scripts/setup.ps1](../scripts/setup.ps1) | Windows 检测 Python；显式加参数时安装 Python、初始化配置 |
| [scripts/configure.py](../scripts/configure.py) | 创建私有配置、隐藏输入、只显示配置是否存在 |
| [scripts/literature_search.py](../scripts/literature_search.py) | `doctor` / `search` / `resolve` 统一入口，结果与日志输出 |
| [scripts/providers.py](../scripts/providers.py) | 五个直接检索源，Crossref/DataCite DOI 元数据及 Unpaywall 链接 |
| [scripts/runtime.py](../scripts/runtime.py) | 六项配置读取、请求限速、有限重试、进程内请求缓存 |
| [scripts/test_literature_search.py](../scripts/test_literature_search.py) | 离线行为测试，无需 Key 或网络 |

修改脚本后运行 `python -m unittest discover -s scripts -p "test_*.py"`，涉及接口时对相应来源做少量实时自检。来源选择见 [references/sources.md](sources.md)。
