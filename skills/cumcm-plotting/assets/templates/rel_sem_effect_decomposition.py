"""Adaptation reference with demonstration values; replace data and output paths."""

import os as _os
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent
DATA_DIR = TEMPLATE_DIR / "data"
OUTPUT_DIR = TEMPLATE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Force non-interactive rendering for reproducible template execution.
_os.environ["MPLBACKEND"] = "Agg"

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
matplotlib.use("Agg")
plt.rcParams["font.family"] = "Times New Roman"  # 设置全局字体为Times New Roman
plt.rcParams["axes.unicode_minus"] = False  # 允许坐标轴正常显示负号
# 定义分类变量
categories = ["ST", "WS", "SWV", "PRE", "DEM"]
x = np.arange(len(categories))  # 生成横坐标位置
# 定义三类效应值
direct = [-0.17, 0.38, -0.44, 0.27, 0.36]  # 直接效应
indirect = [0.53, 0.16, 0.37, 0.26, 0.55]  # 间接效应
total = [0.47, 0.33, -0.26, 0.44, 0.41]  # 总效应
# 设置柱子的宽度
width = 0.25
# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(9, 5))  # 设置画布大小
# 定义三种颜色
color_direct = "#23B5AF"  # Direct effects 青绿色
color_indirect = "#EC7878"  # Indirect effects 粉红色
color_total = "#43398E"  # Total effects 深蓝色
# 绘制三组柱状图
bar1 = ax.bar(x - width, direct, width, label="Direct effects", color=color_direct)
bar2 = ax.bar(x, indirect, width, label="Indirect effects", color=color_indirect)
bar3 = ax.bar(x + width, total, width, label="Total effects", color=color_total)
# 设置y轴标题，并设置字体大小和加粗
ax.set_ylabel("Standardized Effects", fontsize=14, fontweight="bold")
# 设置x轴刻度标签及其字体大小和加粗
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12, fontweight="bold")
y_ticks = ax.get_yticks()
ax.set_yticks([0, 0.2, 0.4, 0.6, -0.2, -0.4, -0.6])  # 设置y轴刻度为指定的值
ax.set_yticklabels(
    [f"{ytick:.1f}" for ytick in [0, 0.2, 0.4, 0.6, -0.2, -0.4, -0.6]],
    fontsize=12,
    fontweight="bold",
)
# 设置y轴范围
ax.set_ylim(-0.8, 0.8)
# 添加一条y=0的横线
ax.axhline(0, color="black", linewidth=1.2)
# 设置x轴和y轴的刻度参数（字体大小、刻度长度和线宽）
ax.tick_params(axis="both", which="major", labelsize=12, width=1.5, length=6, direction="out")
ax.tick_params(axis="both", which="minor", width=1.2, length=3)
# 设置图框（四个边框线）的线宽
for spine in ax.spines.values():
    spine.set_linewidth(1.5)
# 在柱子上添加数值标签
for bars in [bar1, bar2, bar3]:
    ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=12, fontweight="bold")  # 格式为小数点后两位
# 添加图例，并设置在图的上方
legend = ax.legend(
    loc="lower center",  # 图例位置：底部中间
    bbox_to_anchor=(0.5, 1.0),  # 调整图例整体向上
    ncol=4,  # 设置为一行四列
    frameon=False,  # 去掉图例外框
    fontsize=12,  # 图例字体大小
)
# 图例内容字体加粗
for text in legend.get_texts():
    text.set_fontweight("bold")
legend.set_title("Effect type", prop={"weight": "bold", "size": 13})  # 图例标题加粗并设置字体大小
# 自动调整子图参数，使之填充整个图像区域
plt.tight_layout()
plt.savefig(str(OUTPUT_DIR / "结构方程模型效应图.png"), dpi=300)
# 显示图形
plt.close("all")  # Interactive display removed; assets were exported above.
