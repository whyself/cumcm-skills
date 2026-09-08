# 环境准备

先沿用项目可运行的解释器与依赖。缺少环境时安装后继续，避免只列安装命令便结束。常规数据绘图不需要 API 密钥，也不要求配置专用环境变量。

## Python

从项目目录执行；`<包目录>` 替换为当前技能目录的实际路径，路径有空格时保留引号。

```powershell
python -m venv .venv
& ./.venv/Scripts/python.exe "<包目录>/scripts/prepare_env.py"
```

已有项目虚拟环境就跳过创建。Linux/macOS 使用 `.venv/bin/python`。若无 Python，先通过当前系统可用的包管理器安装 Python 3.10+，或使用环境提供的已有运行时，验证 `python --version` 后继续。

`prepare_env.py` 在调用它的解释器中检查基础绘图包，仅安装缺失项并重新导入验证。按最终采用的代码安装额外依赖：

```powershell
& ./.venv/Scripts/python.exe "<包目录>/scripts/prepare_env.py" --script ./plot.py --extra openpyxl --report ./outputs/environment.json
```

`--extra` 使用导入名；XLSX 用 `openpyxl`，XLS 用 `xlrd`，统计计算用 `scipy`，交互图用 `plotly`。模板额外包按其 imports 和实际采用的功能确定，不把整个模板库的依赖全部安装。检查器不执行候选模板；未知导入名需核实包名或本地模块后处理。

部分模板用可选环境变量 `CUMCM_FULL_SEARCH=1` 启用完整搜索、分析或导出，默认使用较小的演示计算量。是否开启及实际计算范围以所选模板代码为准。

安装后仍不能导入时检查实际报错和版本冲突，必要时在项目新环境中安装兼容版本并验证。不覆盖项目已有依赖文件，不静默切换语言。工具、网络或权限确实不允许安装时说明失败项与未完成的步骤。

## 字体与导出

用 `python "<包目录>/scripts/setup_style.py" --list-fonts` 检查中文字体。缺失时安装 Noto Sans CJK SC / Source Han Sans SC 等中文字体；也可将合法字体文件放入项目并通过 `matplotlib.font_manager.fontManager.addfont()` 注册。安装或注册后重新执行中文样式设置并渲染，检查中文、负号及上下标。不要把中文改成英文来掩盖缺字。

后台出图可在导入 pyplot 前设置 `matplotlib.use('Agg')`；`MPLBACKEND=Agg` 是可选等效设置。仅遇到字体缓存目录权限问题才指定可写的 `MPLCONFIGDIR`。图幅、DPI、字体、种子和数据路径放在代码参数中。

MATLAB / R 项目使用既有运行时，先安装所选绘图代码需要的工具箱或包；如运行时需要用户持有的许可或无法自动安装，明确说明。包内 Python 配方可供理解图意，但不能冒充该语言已运行的结果。
