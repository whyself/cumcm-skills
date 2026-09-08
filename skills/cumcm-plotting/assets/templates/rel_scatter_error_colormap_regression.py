"""Adaptation reference with demonstration values; replace data and output paths."""

import os as _os
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent
DATA_DIR = TEMPLATE_DIR / "data"
OUTPUT_DIR = TEMPLATE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Force non-interactive rendering for reproducible template execution.
_os.environ["MPLBACKEND"] = "Agg"

# =========================================================================================
# ====================================== 1. 库的导入 =========================================
# =========================================================================================
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy import stats

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["axes.unicode_minus"] = False
import matplotlib

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
# =========================================================================================
# ====================================== 2. 颜色库设置===============================
# =========================================================================================
COLOR_SCHEMES = {
    1: "RdPu",
    2: "viridis",
    3: "plasma",
    4: "inferno",
    5: "coolwarm",
    6: "RdBu",
    7: "Greens",
    8: "Blues",
    9: "Oranges",
    10: "PiYG",
    11: "PRGn",
    12: "BrBG",
    13: "PuOr",
    14: "RdYlGn",
    15: "Greys",
    16: "cividis",
    17: "magma",
    18: "YlGnBu",
    19: "Spectral",
    20: "twilight",
}
SELECTED_SCHEME = 20  # 设置选择的颜色方案
selected_cmap = COLOR_SCHEMES.get(SELECTED_SCHEME, "RdPu")  # 获取颜色


# =========================================================================================
# ====================================== 3. 绘图函数====================================
# =========================================================================================
def create_and_save_plot(
    x_data,
    y_data,
    y_error,
    color_data,
    cbar_ticks,
    cmap_name,
):
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.axhline(0, color="gray", linestyle="--", alpha=0.7, lw=1.5)  # y=0灰色水平虚线
    ax.axvline(0, color="gray", linestyle="--", alpha=0.7, lw=1.5)  # x=0灰色垂直虚线
    # 绘制Y轴误差棒
    ax.errorbar(
        x_data,
        y_data,
        yerr=y_error,
        fmt="none",
        ecolor="darkgray",
        elinewidth=1.5,
        capsize=3,
        alpha=0.8,
        zorder=1,
    )
    # 绘制散点图
    scatter = ax.scatter(
        x_data,
        y_data,
        c=color_data,
        cmap=cmap_name,
        s=120,
        edgecolors="black",
        linewidth=1.5,
        zorder=2,
        vmin=min(cbar_ticks),
        vmax=max(cbar_ticks),
    )
    # 执行线性回归，获取斜率、截距、R值、P值和标准误
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_data, y_data)
    x_fit = np.array([-0.005, 0.065])  # 用于绘制拟合线的X坐标点
    y_fit = slope * x_fit + intercept  # 计算拟合线对应的Y坐标点
    # 绘制拟合线
    ax.plot(x_fit, y_fit, color="black", linewidth=2.5, zorder=3)
    annotation_text = f"slope = {slope:.2f}\nr = {r_value:.2f}"  # 图上的文本
    # 添加文本
    ax.text(0.95, 0.95, annotation_text, transform=ax.transAxes, fontsize=14, ha="right", va="top")
    # 在主坐标轴内创建一个内嵌坐标轴，用于放置颜色条
    cbaxes = inset_axes(
        ax,
        width="40%",
        height="4%",
        loc="lower center",
        bbox_to_anchor=(-0.25, 0.2, 1, 1),
        bbox_transform=ax.transAxes,
    )
    # 创建水平颜色条
    cbar = fig.colorbar(scatter, cax=cbaxes, orientation="horizontal", extend="neither")
    cbar.outline.set_edgecolor("black")  # 设置颜色条轮廓线的颜色
    cbar.outline.set_linewidth(1.5)  # 设置颜色条轮廓线的线宽
    cbar.set_label("Trend of SC$_w$ (%/decade)", fontsize=14)  # 设置颜色条的标签文本和字体大小（
    cbar.ax.tick_params(labelsize=12)  # 设置颜色条刻度标签的字体大小
    cbar.set_ticks(cbar_ticks)  # 设置颜色条上需要显示的刻度位置
    ax.set_xlim(-0.01, 0.068)  # 设置X轴的显示范围
    ax.set_ylim(-0.5, 0.2)  # 设置Y轴的显示范围
    ax.set_xlabel("Trend of Δα$_w$ (unitless/decade)", fontsize=16)  # x轴标题
    ax.set_ylabel("Trend of daytime ΔLST$_w$ (K/decade)", fontsize=16)  # y轴标题
    ax.tick_params(axis="both", which="major", labelsize=14)  # 主刻度标签的字体大小
    ax.text(-0.1, 1.02, "d", transform=ax.transAxes, fontsize=24, fontweight="bold")  # 添加子图标题
    # 保存
    plt.savefig(str(OUTPUT_DIR / f"{SELECTED_SCHEME}.png"), dpi=300, bbox_inches="tight")
    plt.savefig(str(OUTPUT_DIR / f"{SELECTED_SCHEME}.pdf"), bbox_inches="tight")


# =========================================================================================
# ====================================== 4.读取数据，执行绘图====================================
# =========================================================================================
if __name__ == "__main__":
    df_data = pd.read_excel(str(DATA_DIR / "simulation_data.xlsx"))  # 读取数据
    x_data = df_data["x_data"].values  # x轴数据
    y_data = df_data["y_data"].values  # y轴数据
    y_error = df_data["y_error"].values  # 误差棒的长度
    color_data = df_data["color_data"].values  # 散点数据
    cbar_ticks = [0, -5, -10, -15]  # 颜色条的刻度值
    # 开始绘图
    create_and_save_plot(
        x_data=x_data,  # x轴数据
        y_data=y_data,  # y轴数据
        y_error=y_error,  # 误差棒的长度数据
        color_data=color_data,  # 散点数据
        cbar_ticks=cbar_ticks,  # 颜色条的刻度值
        cmap_name=selected_cmap,  # 颜色方案
    )
