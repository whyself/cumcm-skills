"""Adaptation reference with demonstration values; replace data and output paths."""

import os as _os
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent
DATA_DIR = TEMPLATE_DIR / "data"
OUTPUT_DIR = TEMPLATE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Force non-interactive rendering for reproducible template execution.
_os.environ["MPLBACKEND"] = "Agg"

from PIL import Image, ImageEnhance

original_image_path = str(DATA_DIR / "shap_grid_combined.png")  # 输入图像来自模板数据目录
# =========================================================================================
# ======================================饱和度调整===============================
# =========================================================================================
# 加载原始图像
img = Image.open(original_image_path)
# 创建一个颜色增强器
enhancer = ImageEnhance.Color(img)
saturation_factor = 1.5  # 定义一个饱和度增强因子变量，1.5 表示增加50%的饱和度
# 应用增强
img_saturated = enhancer.enhance(saturation_factor)
# 保存路径
saturated_image_path = str(OUTPUT_DIR / "饱和度增强1.png")
# 保存增强后的图像
img_saturated.save(saturated_image_path)

# =========================================================================================
# ======================================对比度调整===============================
# =========================================================================================
img = Image.open(original_image_path)  # 重新打开原始图像文件
enhancer_contrast = ImageEnhance.Contrast(img)  # 基于原始图像创建一个对比度增强器对象
img_contrasted = enhancer_contrast.enhance(1.5)  # 增加对比度
img_contrasted.save(str(OUTPUT_DIR / "增加对比度1.png"))
# =========================================================================================
# ======================================锐度调整===============================
# =========================================================================================
img = Image.open(original_image_path)  # 再次打开
# 调整锐度
enhancer_sharpness = ImageEnhance.Sharpness(img)
img_sharp = enhancer_sharpness.enhance(1.5)  # 增加锐度
img_sharp.save(str(OUTPUT_DIR / "调整锐度1.png"))
# =========================================================================================
# ======================================亮度调整===============================
# =========================================================================================
# 加载
img = Image.open(original_image_path)
# 调整亮度
enhancer_brightness = ImageEnhance.Brightness(img)
img_bright = enhancer_brightness.enhance(1.1)  # 增强亮度
img_bright.save(str(OUTPUT_DIR / "调整亮度1.png"))
# =========================================================================================
# ======================================综合调整调整===============================
# =========================================================================================
img = Image.open(original_image_path)  # 再次打开原始图像
# 增强对比度
enhancer_contrast = ImageEnhance.Contrast(img)
img = enhancer_contrast.enhance(1.15)
# 增强饱和度
enhancer_color = ImageEnhance.Color(img)
img = enhancer_color.enhance(1.3)
# 增强锐度
enhancer_sharpness = ImageEnhance.Sharpness(img)
img = enhancer_sharpness.enhance(1.2)
enhanced_path = str(OUTPUT_DIR / "final_grid_fully_enhanced1.png")
img.save(enhanced_path, dpi=(108, 108))
