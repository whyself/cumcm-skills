# 模板目录

需要选择模板时，按图型、分类标题或关键词检索本目录中的相关条目，再查看候选代码与必要预览。已指定图型、模板或只修改已有图时可直接处理，无需通读目录。

普通模板是适配参考：含模拟数值、演示计算或旧路径，不能直接当成用户结果运行。预览仅展示版式。先复制代码到工作目录，再按真实数据修改。

`csv-*` 条目共享一个命令行脚本，以去掉 `csv-` 的名称作为子命令；正式输入用 `--input`，通过 `--help` 查看列参数。其余条目没有统一数据接口，需先阅读适配。

普通绘图请求自行选择合适方案并继续；只有用户明确要求自己选择时才等待选型。无法从材料判断且会改变图意的歧义需要澄清；提供候选时说明必要的取舍及数据需求。

## clustering_reduction

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `clu_pca_correlation_heatmap` 主成分分析（PCA）与相关性热图的组合图 | 用相关性热图和 PCA 载荷网络同时展示变量间相关结构与主成分贡献。 | [代码](../assets/templates/clu_pca_correlation_heatmap.py) | [查看](../assets/previews/clu_pca_correlation_heatmap.webp) |
| `clu_spearman_cluster_heatmap` Spearman层次聚类相关性热图 | 用 Spearman 相关系数、显著性和层次聚类展示两组变量的关联模式。 | [代码](../assets/templates/clu_spearman_cluster_heatmap.py) | [查看](../assets/previews/clu_spearman_cluster_heatmap.webp) |
| `clu_pcoa_permanova` PCoA分析图 | 用 PCoA 坐标、置信椭圆和组间检验展示样本群落或距离矩阵差异。 | [代码](../assets/templates/clu_pcoa_permanova.py) | [查看](../assets/previews/clu_pcoa_permanova.webp) |
| `clu_rda_biplot` RDA冗余分析 | 用 RDA 双标图展示样本、性状和环境因子之间的约束排序关系。 | [代码](../assets/templates/clu_rda_biplot.py) | [查看](../assets/previews/clu_rda_biplot.webp) |

## comparison_ranking

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `cmp_circular_barplot` 环状条形图 | 用环状条形图在极坐标中比较多类别数值大小和排序。 | [代码](../assets/templates/cmp_circular_barplot.py) | [查看](../assets/previews/cmp_circular_barplot.webp) |
| `cmp_ternary_scatter` 三元图 | 用三元散点图展示三个组成部分之和固定时的比例结构与分布。 | [代码](../assets/templates/cmp_ternary_scatter.py) | [查看](../assets/previews/cmp_ternary_scatter.webp) |
| `cmp_correlation_stacked_bar` 相关性分析堆叠条形图 | 用堆叠条形图展示多个因子在不同分组中的相关贡献或构成差异。 | [代码](../assets/templates/cmp_correlation_stacked_bar.py) | [查看](../assets/previews/cmp_correlation_stacked_bar.webp) |
| `cmp_flowing_percentage_stack` 流动趋势百分比堆叠图 | 用流动式百分比堆叠面积图展示分类组成在不同端口或阶段间的变化。 | [代码](../assets/templates/cmp_flowing_percentage_stack.py) | [查看](../assets/previews/cmp_flowing_percentage_stack.webp) |
| `cmp_gradient_single_factor_bar` 渐变单因子条形图 | 用多小图渐变条形图展示单因子效应大小、排序和显著性。 | [代码](../assets/templates/cmp_gradient_single_factor_bar.py) | [查看](../assets/previews/cmp_gradient_single_factor_bar.webp) |
| `cmp_horizontal_percentage_stack` 横轴百分比堆叠图 | 用横向百分比堆叠条形图和连接线展示不同分组的组成比例。 | [代码](../assets/templates/cmp_horizontal_percentage_stack.py) | [查看](../assets/previews/cmp_horizontal_percentage_stack.webp) |
| `cmp_multi_donut_charts` 多组环形图 | 用多组环形图并排展示多个对象的类别占比结构。 | [代码](../assets/templates/cmp_multi_donut_charts.py) | [查看](../assets/previews/cmp_multi_donut_charts.webp) |
| `cmp_multi_metric_radar` 多指标雷达对比图 | 用雷达图比较多个对象在多指标维度上的综合表现。 | [代码](../assets/templates/cmp_multi_metric_radar.py) | [查看](../assets/previews/cmp_multi_metric_radar.webp) |
| `cmp_nightingale_rose_grid` 自由组合南丁格尔玫瑰图 | 用多组南丁格尔玫瑰图展示类别占比或数值在多个对象中的径向分布。 | [代码](../assets/templates/cmp_nightingale_rose_grid.py) | [查看](../assets/previews/cmp_nightingale_rose_grid.webp) |
| `cmp_stack_pie_box_report` 百分比堆叠、内嵌饼图与箱线图报告 | 用百分比堆叠、内嵌饼图和箱线图组合展示多层分类贡献与分布。 | [代码](../assets/templates/cmp_stack_pie_box_report.py) | [查看](../assets/previews/cmp_stack_pie_box_report.webp) |
| `cmp_radial_stacked_bar` 径向堆叠图 | 用径向堆叠条形图展示多类别在多个对象中的分层组成。 | [代码](../assets/templates/cmp_radial_stacked_bar.py) | [查看](../assets/previews/cmp_radial_stacked_bar.webp) |
| `cmp_shap_heatmap_bar_report` SHAP组合分析图 | 用 SHAP 重要性、热图、饼图和箱线图组合展示特征贡献与分组差异。 | [代码](../assets/templates/cmp_shap_heatmap_bar_report.py) | [查看](../assets/previews/cmp_shap_heatmap_bar_report.webp) |
| `cmp_3d_ribbon_chart` 3D条带图 | 用三维条带折线展示多个类别随时间或序列变化的趋势。 | [代码](../assets/templates/cmp_3d_ribbon_chart.py) | [查看](../assets/previews/cmp_3d_ribbon_chart.webp) |
| `cmp_3d_waterfall_distribution` 三维瀑布图 | 用三维瀑布图展示多组分布曲线在连续维度上的层叠变化。 | [代码](../assets/templates/cmp_3d_waterfall_distribution.py) | [查看](../assets/previews/cmp_3d_waterfall_distribution.webp) |
| `cmp_3d_stacked_surface` 三维堆叠图 | 用多层三维堆叠面展示不同平面上的矩阵数值或热力分布。 | [代码](../assets/templates/cmp_3d_stacked_surface.py) | [查看](../assets/previews/cmp_3d_stacked_surface.webp) |
| `cmp_3d_bar_chart` 3D柱状图 | 用三维柱状图展示二维类别网格上的数值高度差异。 | [代码](../assets/templates/cmp_3d_bar_chart.py) | [查看](../assets/previews/cmp_3d_bar_chart.webp) |

## composite_evaluation

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `evl_ml_metric_circular_dashboard` 机器学习多维度评估环形图 | 用多圈环形仪表展示机器学习分类、回归和特征解释的多维度评估结果。 | [代码](../assets/templates/evl_ml_metric_circular_dashboard.py) | [查看](../assets/previews/evl_ml_metric_circular_dashboard.webp) |
| `evl_multiomics_circular_heatmap` 多组学验证环形热图 | 用环形热图展示多组学验证指标在多层分类中的强弱和一致性。 | [代码](../assets/templates/evl_multiomics_circular_heatmap.py) | [查看](../assets/previews/evl_multiomics_circular_heatmap.webp) |

## distribution_uncertainty

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `dis_combined_boxplot_grid` 组合箱线图 | 用多面板箱线图比较多个数据集或指标在分组间的分布差异。 | [代码](../assets/templates/dis_combined_boxplot_grid.py) | [查看](../assets/previews/dis_combined_boxplot_grid.webp) |
| `dis_ridgeline_distribution` 山脊分布图 | 用山脊图展示多个组别连续变量分布的峰形和位置差异。 | [代码](../assets/templates/dis_ridgeline_distribution.py) | [查看](../assets/previews/dis_ridgeline_distribution.webp) |
| `dis_violin_mean_change_grid` 均值变化小提琴图 | 用多面板小提琴图展示多组数据分布形态和均值变化。 | [代码](../assets/templates/dis_violin_mean_change_grid.py) | [查看](../assets/previews/dis_violin_mean_change_grid.webp) |
| `dis_rank_sum_violin_box` 秩和检验分布图 | 用小提琴、箱线和散点展示两组分布差异及秩和检验显著性。 | [代码](../assets/templates/dis_rank_sum_violin_box.py) | [查看](../assets/previews/dis_rank_sum_violin_box.webp) |
| `dis_radial_bar_error_significance` 带显著性标记与误差棒的环形柱状图 | 用环形柱状图、误差棒和显著性标记比较多组均值差异。 | [代码](../assets/templates/dis_radial_bar_error_significance.py) | [查看](../assets/previews/dis_radial_bar_error_significance.webp) |
| `dis_tukey_hsd_violin_grid` Tukey HSD检验小提琴图 | 用多面板小提琴图展示 Tukey HSD 多重比较后的组间差异。 | [代码](../assets/templates/dis_tukey_hsd_violin_grid.py) | [查看](../assets/previews/dis_tukey_hsd_violin_grid.webp) |

## multi_panel_report

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `mpn_rf_importance_correlation` RF变量重要性与相关性分析组合图 | 用随机森林变量重要性、SHAP和相关性矩阵组合展示驱动因子分析结果。 | [代码](../assets/templates/mpn_rf_importance_correlation.py) | [查看](../assets/previews/mpn_rf_importance_correlation.webp) |
| `mpn_scatter_matrix_timeseries_regression` 散点矩阵与时间序列回归报告 | 用散点矩阵、边缘分布和时间序列回归面板展示变量关系与趋势。 | [代码](../assets/templates/mpn_scatter_matrix_timeseries_regression.py) | [查看](../assets/previews/mpn_scatter_matrix_timeseries_regression.webp) |
| `mpn_plot_postprocessing_grid` 绘图结果后处理 | 用图像后处理方式把已有绘图结果统一裁切、拼接成多面板报告。 | [代码](../assets/templates/mpn_plot_postprocessing_grid.py) | [查看](../assets/previews/mpn_plot_postprocessing_grid.webp) |
| `mpn_3d_surface_scatter_report` 三维组合分析图 | 用三维曲面、网格和散点组合展示两个变量与响应值之间的非线性关系。 | [代码](../assets/templates/mpn_3d_surface_scatter_report.py) | [查看](../assets/previews/mpn_3d_surface_scatter_report.webp) |

## network_flow

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `net_chord_relationship` 关系和弦图 | 用和弦图展示实体、类别或物种之间的成对关系和连接强度。 | [代码](../assets/templates/net_chord_relationship.py) | [查看](../assets/previews/net_chord_relationship.webp) |
| `net_multi_set_venn` 多组韦恩图 | 用多组韦恩图展示集合之间的交集、并集和特有元素。 | [代码](../assets/templates/net_multi_set_venn.py) | [查看](../assets/previews/net_multi_set_venn.webp) |

## optimization_decision

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `opt_hants_parameter_selection` HANTS最佳参数选择 | 用拟合散点和回归指标评估 HANTS 时间序列重建的最佳参数组合。 | [代码](../assets/templates/opt_hants_parameter_selection.py) | [查看](../assets/previews/opt_hants_parameter_selection.webp) |

## prediction_evaluation

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `prd_multi_model_roc` 多模型二分类ROC曲线 | 用多模型 ROC 曲线比较二分类模型的判别能力和 AUC。 | [代码](../assets/templates/prd_multi_model_roc.py) | [查看](../assets/previews/prd_multi_model_roc.webp) |
| `prd_multi_model_regression_fit` 多模型回归拟合对比图 | 用多面板预测-实测散点图比较多个回归模型拟合效果。 | [代码](../assets/templates/prd_multi_model_regression_fit.py) | [查看](../assets/previews/prd_multi_model_regression_fit.webp) |
| `prd_regression_learning_curve` 多模型回归学习曲线与预测评估 | 用学习曲线和预测评估面板展示多模型回归的训练样本效应与泛化性能。 | [代码](../assets/templates/prd_regression_learning_curve.py) | [查看](../assets/previews/prd_regression_learning_curve.webp) |
| `prd_grouped_regression_fit` 多组别回归拟合图 | 用分组预测-实测散点图比较训练集和验证集的回归拟合一致性。 | [代码](../assets/templates/prd_grouped_regression_fit.py) | [查看](../assets/previews/prd_grouped_regression_fit.webp) |
| `prd_regression_evaluation_panels` 回归预测评估多面板图 | 用多面板预测散点、残差和边缘分布综合评估多个回归模型。 | [代码](../assets/templates/prd_regression_evaluation_panels.py) | [查看](../assets/previews/prd_regression_evaluation_panels.webp) |
| `prd_taylor_diagram` 泰勒图 | 用泰勒图同时比较模型的相关系数、标准差和中心化误差。 | [代码](../assets/templates/prd_taylor_diagram.py) | [查看](../assets/previews/prd_taylor_diagram.webp) |
| `prd_voting_ensemble_learning_curve` 投票集成学习验证图 | 用学习曲线评估投票集成模型在不同训练样本量下的表现。 | [代码](../assets/templates/prd_voting_ensemble_learning_curve.py) | [查看](../assets/previews/prd_voting_ensemble_learning_curve.webp) |
| `prd_xgboost_binary_shap` XGBoost二分类评估图 | 用 XGBoost 二分类 SHAP 瀑布或贡献图解释单个样本的分类驱动因素。 | [代码](../assets/templates/prd_xgboost_binary_shap.py) | [查看](../assets/previews/prd_xgboost_binary_shap.webp) |
| `prd_xgboost_multiclass_shap` XGBoost多分类评估图 | 用 XGBoost 多分类 SHAP 散点图展示特征对类别判别的影响。 | [代码](../assets/templates/prd_xgboost_multiclass_shap.py) | [查看](../assets/previews/prd_xgboost_multiclass_shap.webp) |
| `prd_xgboost_regression_ale_heatmap` XGBoost回归预测评估图 | 用 XGBoost 回归解释图展示双变量 ALE 或响应面的预测效应。 | [代码](../assets/templates/prd_xgboost_regression_ale_heatmap.py) | [查看](../assets/previews/prd_xgboost_regression_ale_heatmap.webp) |

## relationship_correlation

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `rel_lollipop_bubble_coefficients` 棒棒糖气泡图 | 用棒棒糖气泡图展示标准化回归系数或变量效应大小。 | [代码](../assets/templates/rel_lollipop_bubble_coefficients.py) | [查看](../assets/previews/rel_lollipop_bubble_coefficients.webp) |
| `rel_radial_effect_chart` 环形效应图 | 用环形效应图展示不同变量在多组中的标准化效应方向与大小。 | [代码](../assets/templates/rel_radial_effect_chart.py) | [查看](../assets/previews/rel_radial_effect_chart.webp) |
| `rel_multilayer_encoded_correlation_heatmap` 多层编码相关性热图 | 用多层编码热图同时展示相关系数、显著性和分类属性。 | [代码](../assets/templates/rel_multilayer_encoded_correlation_heatmap.py) | [查看](../assets/previews/rel_multilayer_encoded_correlation_heatmap.webp) |
| `rel_network_correlation_heatmap` 组合式相关性网络热力图 | 用相关性热图和网络连线组合展示变量群之间的关联结构。 | [代码](../assets/templates/rel_network_correlation_heatmap.py) | [查看](../assets/previews/rel_network_correlation_heatmap.webp) |
| `rel_diagonal_split_triangular_heatmap` 图双变量对角线分割组合三角热图 | 用对角线分割三角热图在同一单元中展示双变量关系的两类编码。 | [代码](../assets/templates/rel_diagonal_split_triangular_heatmap.py) | [查看](../assets/previews/rel_diagonal_split_triangular_heatmap.webp) |
| `rel_scatter_error_colormap_regression` 带有误差棒、颜色映射和线性回归线的散点图 | 用带误差棒、颜色映射和线性回归线的散点图展示两个趋势变量的关系。 | [代码](../assets/templates/rel_scatter_error_colormap_regression.py) | [查看](../assets/previews/rel_scatter_error_colormap_regression.webp) |
| `rel_fdr_correlation_heatmap` FDR校正相关性分析图 | 用 FDR 校正后的相关性热图展示多变量显著相关关系。 | [代码](../assets/templates/rel_fdr_correlation_heatmap.py) | [查看](../assets/previews/rel_fdr_correlation_heatmap.webp) |
| `rel_circular_grouped_correlation_heatmap` 环状相关性热图-带有分组标注 | 用环状分组相关性热图展示变量分组、相关强度和显著性。 | [代码](../assets/templates/rel_circular_grouped_correlation_heatmap.py) | [查看](../assets/previews/rel_circular_grouped_correlation_heatmap.webp) |
| `rel_grouped_correlation_heatmap` 分组相关性热图 | 用分组矩阵热图展示变量组内和组间的相关性格局。 | [代码](../assets/templates/rel_grouped_correlation_heatmap.py) | [查看](../assets/previews/rel_grouped_correlation_heatmap.webp) |
| `rel_grouped_correlation_bubble_matrix` 分组相关性气泡矩阵 | 用气泡矩阵展示分组相关系数、显著性和相关方向。 | [代码](../assets/templates/rel_grouped_correlation_bubble_matrix.py) | [查看](../assets/previews/rel_grouped_correlation_bubble_matrix.webp) |
| `rel_bar_association_matrix` 横向条形图与关联矩阵组合图 | 用横向条形图和关联矩阵组合展示单变量重要性与多变量关系。 | [代码](../assets/templates/rel_bar_association_matrix.py) | [查看](../assets/previews/rel_bar_association_matrix.webp) |
| `rel_interaction_bubble_matrix` 交互作用气泡图 | 用交互作用气泡矩阵展示成对因子组合的增强或抑制效应。 | [代码](../assets/templates/rel_interaction_bubble_matrix.py) | [查看](../assets/previews/rel_interaction_bubble_matrix.webp) |
| `rel_mantel_network_heatmap` Mantel网络相关热图 | 用 Mantel 网络和相关热图组合展示距离矩阵或变量组之间的关联。 | [代码](../assets/templates/rel_mantel_network_heatmap.py) | [查看](../assets/previews/rel_mantel_network_heatmap.webp) |
| `rel_multiclass_scatter_matrix` 多类别散点图矩阵 | 用多类别散点图矩阵展示多变量两两关系、分布和组别差异。 | [代码](../assets/templates/rel_multiclass_scatter_matrix.py) | [查看](../assets/previews/rel_multiclass_scatter_matrix.webp) |
| `rel_pearson_correlation_heatmap` Pearson相关性热图 | 用 Pearson 相关性热图展示多变量线性相关强度和方向。 | [代码](../assets/templates/rel_pearson_correlation_heatmap.py) | [查看](../assets/previews/rel_pearson_correlation_heatmap.webp) |
| `rel_petal_correlation_heatmap` 花瓣状相关性热图 | 用花瓣状环形热图展示多组变量相关矩阵和分组注释。 | [代码](../assets/templates/rel_petal_correlation_heatmap.py) | [查看](../assets/previews/rel_petal_correlation_heatmap.webp) |
| `rel_grouped_regression_marginal_scatter` 带有边缘分布的多组回归拟合散点图 | 用边缘分布和分组回归散点图展示两个变量的关系及组别差异。 | [代码](../assets/templates/rel_grouped_regression_marginal_scatter.py) | [查看](../assets/previews/rel_grouped_regression_marginal_scatter.webp) |
| `rel_scatter_matrix_network` 散点矩阵与相关性网络图 | 用散点矩阵和相关性网络组合展示多变量关系、密度和路径连接。 | [代码](../assets/templates/rel_scatter_matrix_network.py) | [查看](../assets/previews/rel_scatter_matrix_network.webp) |
| `rel_pairplot_seamless_heatmap` 散点图矩阵与无缝相关性热图 | 用散点矩阵与无缝相关性热图组合展示多变量关系和相关强度。 | [代码](../assets/templates/rel_pairplot_seamless_heatmap.py) | [查看](../assets/previews/rel_pairplot_seamless_heatmap.webp) |
| `rel_sem_effect_decomposition` 结构方程模型效应分解图 | 用结构方程模型效应分解图展示直接、间接和总效应大小。 | [代码](../assets/templates/rel_sem_effect_decomposition.py) | [查看](../assets/previews/rel_sem_effect_decomposition.webp) |
| `rel_network_radar_report` 相关性网络与雷达报告 | 用相关性网络、矩阵和雷达图组合展示变量关系与综合指标轮廓。 | [代码](../assets/templates/rel_network_radar_report.py) | [查看](../assets/previews/rel_network_radar_report.webp) |

## sensitivity_robustness

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `sen_grouped_rf_shap` 按指标分组的随机森林SHAP分析图 | 用分组 SHAP 条形/点图展示随机森林模型中不同指标组的贡献。 | [代码](../assets/templates/sen_grouped_rf_shap.py) | [查看](../assets/previews/sen_grouped_rf_shap.webp) |
| `sen_grouped_shap_top_features` 分组SHAP重要性与头部特征图 | 用分组 SHAP 重要性条形图和头部特征占比展示关键变量贡献。 | [代码](../assets/templates/sen_grouped_shap_top_features.py) | [查看](../assets/previews/sen_grouped_shap_top_features.webp) |
| `sen_shap_importance_dependence` SHAP特征重要性与依赖组合图 | 用 SHAP 重要性、依赖散点和局部曲线组合展示特征效应。 | [代码](../assets/templates/sen_shap_importance_dependence.py) | [查看](../assets/previews/sen_shap_importance_dependence.webp) |
| `sen_shap_importance_rose` SHAP重要性玫瑰图 | 用 SHAP 重要性玫瑰图和蜂群图展示特征贡献方向与强度。 | [代码](../assets/templates/sen_shap_importance_rose.py) | [查看](../assets/previews/sen_shap_importance_rose.webp) |
| `sen_gam_contour_heatmap` GAM非线性影响等高线热力图 | 用 GAM 二维等高线热力图展示两个变量交互下的非线性响应。 | [代码](../assets/templates/sen_gam_contour_heatmap.py) | [查看](../assets/previews/sen_gam_contour_heatmap.webp) |
| `sen_gam_partial_residual` GAM偏依赖与残差分析图 | 用 GAM 偏依赖曲线和残差诊断面板展示非线性拟合质量。 | [代码](../assets/templates/sen_gam_partial_residual.py) | [查看](../assets/previews/sen_gam_partial_residual.webp) |
| `sen_shap_dependence_distribution_threshold` SHAP依赖、分布与阈值效应图 | 用 SHAP 依赖曲线、分布和阈值标注识别关键特征的响应拐点。 | [代码](../assets/templates/sen_shap_dependence_distribution_threshold.py) | [查看](../assets/previews/sen_shap_dependence_distribution_threshold.webp) |
| `sen_shap_gam_feature_effects` SHAP–GAM特征效应图 | 用 SHAP 与 GAM 曲线组合展示多个特征的平滑非线性效应。 | [代码](../assets/templates/sen_shap_gam_feature_effects.py) | [查看](../assets/previews/sen_shap_gam_feature_effects.webp) |
| `sen_shap_interaction_dependence` SHAP重要性、依赖与交互效应图 | 用 SHAP 重要性、依赖散点和交互颜色编码展示特征间交互效应。 | [代码](../assets/templates/sen_shap_interaction_dependence.py) | [查看](../assets/previews/sen_shap_interaction_dependence.webp) |
| `sen_shap_top_dependence_grid` SHAP重要性与头部依赖图 | 用 SHAP 总结图和头部特征依赖小图展示关键变量的局部效应。 | [代码](../assets/templates/sen_shap_top_dependence_grid.py) | [查看](../assets/previews/sen_shap_top_dependence_grid.webp) |
| `sen_shap_interaction_network` SHAP交互特征网络图 | 用网络图展示 SHAP 交互作用中变量之间的连接强度和方向。 | [代码](../assets/templates/sen_shap_interaction_network.py) | [查看](../assets/previews/sen_shap_interaction_network.webp) |
| `sen_shap_interaction_matrix_heatmap` SHAP交互作用矩阵热图 | 用 SHAP 交互矩阵热图和小蜂群图展示成对特征互作模式。 | [代码](../assets/templates/sen_shap_interaction_matrix_heatmap.py) | [查看](../assets/previews/sen_shap_interaction_matrix_heatmap.webp) |
| `sen_shap_pdp_combo` SHAP与PDP组合图 | 用 SHAP 与 PDP 组合展示特征重要性和平均边际效应。 | [代码](../assets/templates/sen_shap_pdp_combo.py) | [查看](../assets/previews/sen_shap_pdp_combo.webp) |
| `sen_multi_target_shap_polynomial_fit` 多目标SHAP多项式拟合图 | 用多目标 SHAP 多项式拟合图展示不同目标下特征效应曲线和拟合优度。 | [代码](../assets/templates/sen_multi_target_shap_polynomial_fit.py) | [查看](../assets/previews/sen_multi_target_shap_polynomial_fit.webp) |
| `sen_2d_pdp_contour` 2维PDP | 用二维 PDP 等高线图展示两特征交互对模型预测的平均影响。 | [代码](../assets/templates/sen_2d_pdp_contour.py) | [查看](../assets/previews/sen_2d_pdp_contour.webp) |

## spatial_geographic

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `spa_pixelwise_standardized_regression` 逐像元标准化与多元线性回归 | 用逐像元标准化和多元线性回归计算栅格时间序列的驱动系数与主导因子。 | [代码](../assets/templates/spa_pixelwise_standardized_regression.py) | [查看](../assets/previews/spa_pixelwise_standardized_regression.webp) |
| `spa_moving_window_partial_correlation` 空间移动窗口偏相关栅格 | 用空间移动窗口偏相关分析计算栅格变量在局部邻域中的相关关系。 | [代码](../assets/templates/spa_moving_window_partial_correlation.py) | [查看](../assets/previews/spa_moving_window_partial_correlation.webp) |
| `spa_moving_window_rf_shap_drivers` 空间移动窗口随机森林与SHAP驱动因子分析 | 用空间移动窗口随机森林和 SHAP 识别栅格时间序列中的局部主导驱动因子。 | [代码](../assets/templates/spa_moving_window_rf_shap_drivers.py) | [查看](../assets/previews/spa_moving_window_rf_shap_drivers.webp) |
| `spa_xgboost_geoshapley` XGBoost与GeoShapley解释图 | 用 XGBoost 与 GeoShapley 解释空间坐标和环境变量对预测结果的贡献。 | [代码](../assets/templates/spa_xgboost_geoshapley.py) | [查看](../assets/previews/spa_xgboost_geoshapley.webp) |

## trend_time_series

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `trd_dual_axis_bar_line` 双Y轴柱状折线时间序列图 | 用双 Y 轴柱状折线图同时展示容量类指标和功率类指标的时间变化。 | [代码](../assets/templates/trd_dual_axis_bar_line.py) | [查看](../assets/previews/trd_dual_axis_bar_line.webp) |
| `trd_lag_correlation_analysis` 滞后相关性分析图 | 用滞后相关性曲线分析遥感变量相对目标变量的最佳滞后时间。 | [代码](../assets/templates/trd_lag_correlation_analysis.py) | [查看](../assets/previews/trd_lag_correlation_analysis.webp) |
| `trd_smoothed_trend_curves` 平滑趋势曲线 | 用平滑折线图展示多个地区或类别随年份变化的趋势曲线。 | [代码](../assets/templates/trd_smoothed_trend_curves.py) | [查看](../assets/previews/trd_smoothed_trend_curves.webp) |
| `trd_composite_line_bar_dual_axis` 折线图、条形图和双Y轴的复合时间序列图 | 用折线、条形和双 Y 轴组合展示森林、草地等时序指标及趋势统计。 | [代码](../assets/templates/trd_composite_line_bar_dual_axis.py) | [查看](../assets/previews/trd_composite_line_bar_dual_axis.webp) |

## composite_examples

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `multiclass-shap-combo` 多分类 SHAP 组合 | 多分类模型的特征贡献、分布和类别对照 | [代码](../assets/templates/multiclass-shap-combo.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `paired-raincloud` 云雨与均值变化图 | 示例连线连接组均值，没有个体 ID 配对；展示个体变化时需重写配对逻辑，或选 csv-paired | [代码](../assets/templates/paired-raincloud.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `cv-roc-ci` 交叉验证 ROC 与区间 | 分类概率、真实标签和折次的性能与不确定性 | [代码](../assets/templates/cv-roc-ci.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `taylor-diagram` 泰勒图 | 相同观测基准上的相关性、标准差和中心化均方根误差 | [代码](../assets/templates/taylor-diagram.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `correlation-pairgrid` 相关矩阵组合 | 多变量散点、相关系数和边际分布 | [代码](../assets/templates/correlation-pairgrid.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `prediction-marginal-grid` 预测与实测边际组合 | 对齐的预测值、观测值、误差与边际分布 | [代码](../assets/templates/prediction-marginal-grid.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `rf-tpe-surface` 参数优化响应面 | 真实搜索记录中的参数与模型性能；曲面可能含插值 | [代码](../assets/templates/rf-tpe-surface.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `grouped-corr-split-violin` 分组相关与半小提琴 | 两组的相关结构和分布对照 | [代码](../assets/templates/grouped-corr-split-violin.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `grouped-circular-heatmap` 分组环形热图 | 分组指标矩阵，类别多时需检查文字可读性 | [代码](../assets/templates/grouped-circular-heatmap.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `urban-park-cooling-combo` 空间降温效应组合 | 空间或距离信息、温度及分组统计 | [代码](../assets/templates/urban-park-cooling-combo.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `chord-diagram` 和弦关系图 | 组间流量或关系矩阵，说明方向和权重 | [代码](../assets/templates/chord-diagram.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |

## csv_templates

| 标识 / 名称 | 表达内容与数据要求 | 代码 | 预览 |
|---|---|---|---|
| `csv-volcano` 火山图 | 效应量、校正后 p 值、标签；正 p 值检查 | [代码](../scripts/plot_templates.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `csv-roc` ROC 曲线 | FPR 与 TPR 列；范围检查及 AUC 记录 | [代码](../scripts/plot_templates.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `csv-dotplot` 点阵图 | 行列类别、面积变量、颜色变量；类别完整性检查 | [代码](../scripts/plot_templates.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `csv-marginal` 联合与边际分布 | x、y 与可选分组；保留全部观测 | [代码](../scripts/plot_templates.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
| `csv-paired` 配对变化图 | ID、两条件、测量值；重复或不完整配对检查 | [代码](../scripts/plot_templates.py) | 无现成预览，可说明版式或另做标明模拟用途的预览 |
