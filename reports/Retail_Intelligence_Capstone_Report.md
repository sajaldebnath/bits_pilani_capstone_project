---
title: "Retail Intelligence System for Inventory Optimization"
subtitle: "Capstone Project Report"
author: "Sajal Debnath"
date: "April 10, 2026"
---


# Abstract

This capstone project develops a retail intelligence system that goes beyond conventional demand forecasting and instead supports end-to-end inventory decision making. The work began with exploratory analysis of a structured retail dataset and progressively evolved through numerical feature engineering, text representation learning, classical machine learning baselines, deep learning experiments, and a final FastAPI deployment with an interactive dashboard. The resulting system combines a hybrid stocking-priority classifier, a sales prediction model, a recommendation engine, scenario simulation, historical querying, and a business-oriented user interface for demonstration and decision support.

The central academic contribution of the project lies in reframing a forecasting task into a retail decision-support problem. Rather than asking only how many units of a product are likely to sell, the project asks which items should receive low, medium, or high stocking priority after accounting for sales potential, profit density, shelf efficiency, shelf life, fill rate, supplier reliability, and replenishment risk. This required careful target engineering, leakage-aware feature selection, and the combination of semantic and structured features through a hybrid modeling strategy.

The final system is built on a dataset of 2,000 retail records and 64 variables. Exploratory analysis showed that pricing variables were strongly negatively associated with demand, footfall was a major positive demand driver, and operational variables such as shelf life and fill rate were critical in distinguishing commercially attractive items from operationally risky ones. Numerical feature engineering and text-based representations were both explored, including bag-of-words, TF-IDF, Word2Vec-style document representations, and transformer-oriented text inputs. Multiple models were evaluated, including logistic regression variants, regression baselines, a custom deep learning model, and a Hugging Face transformer benchmark.

The deployed system uses two practical models: a hybrid logistic regression classifier for stocking priority and a log-transformed Ridge regression model for demand estimation. These choices were made not simply on raw score, but on a balanced view of interpretability, semantic coverage, stability, and suitability for live deployment in FastAPI. The report documents the complete analytical workflow, presents model comparisons and business insights, and explains how the system supports a business-friendly demonstration through an integrated frontend dashboard.


# 1. Problem Statement

Retail inventory decisions are inherently multi-objective. A product with strong demand may still be a poor stocking candidate if it occupies too much shelf space, has low margin, expires quickly, or is difficult to replenish reliably. Conversely, a product with only moderate demand may deserve a higher stocking priority if it yields strong profit density and can be replenished with minimal operational risk. This makes the practical retail problem substantially richer than a pure demand forecasting problem.

The capstone project addresses the following central question:

**How can a retailer decide which products deserve low, medium, or high stocking priority while balancing demand, profitability, shelf efficiency, perishability, and supply-chain reliability?**

This framing is important for two reasons. First, it reflects the way real inventory and merchandising decisions are made in practice. Second, it creates a natural bridge between academic machine learning work and a deployable decision-support system. Instead of building a single model in isolation, the project develops a pipeline that converts raw data into interpretable inventory recommendations supported by both predictive models and business logic.

The project therefore solves a broader decision-support problem with four connected stages:

1. estimate expected sales for a candidate item
2. infer the stocking priority class of the item
3. translate model outputs into a recommendation with caution flags
4. expose the logic through an API and a business-friendly frontend dashboard

This multi-stage formulation is what makes the final system academically interesting and operationally relevant.

# 2. Objectives

The project was designed around a set of technical and business objectives rather than a single modeling goal.

## 2.1 Primary objectives

1. Analyze the retail dataset to understand the distribution of demand, the role of pricing and traffic variables, and the operational characteristics that influence inventory outcomes.
2. Engineer useful numerical, temporal, interaction, and text-based features without introducing target leakage into the deployed pipeline.
3. Build a business-oriented target for stocking priority so that classification reflects merchandising logic rather than raw sales volume alone.
4. Develop and compare multiple machine learning models for both classification and regression, including classical models, hybrid text-plus-numeric models, and research-oriented deep learning experiments.
5. Select deployable models that balance predictive quality, interpretability, computational efficiency, and runtime robustness.
6. Expose the models through a FastAPI application that supports real-time inference and decision-support workflows.
7. Build a user-facing dashboard that can communicate the system story to a non-technical academic evaluator in a short live demonstration.

## 2.2 Secondary objectives

1. Provide experiment transparency by documenting the models explored even when they are not selected for deployment.
2. Translate model outputs into business-friendly insights such as risk flags, profit density, and scenario comparisons.
3. Preserve academic rigor by explicitly discussing leakage, benchmark comparability, and model-selection trade-offs.

# 3. Dataset Description

The final project uses a structured retail dataset stored in `data/raw/master_retail_dataset_v2.csv`. The dataset contains **2,000 observations** and **64 columns**, combining product descriptors, pricing variables, demand signals, store context, external conditions, and operational inventory variables.

## 3.1 Dataset scope

The dataset contains both commercial and operational views of retail performance:

- product descriptors such as category, sub-category, product name, brand, and brand tier
- pricing and promotion variables such as base price, current price, competitor price, discount percentage, promotion type, and marketing spend
- customer and traffic proxies such as footfall, app traffic, website visits, loyalty usage, repeat purchase rate, and basket size
- operational variables such as shelf capacity, shelf life, supplier delay, stock on hand, fill rate, and safety stock
- temporal and contextual variables such as day of week, month, holiday status, weather, and festival indicators

This breadth makes the dataset suitable for both demand forecasting and inventory intelligence tasks.

## 3.2 Feature groups

The precomputed insights artifacts organize the dataset into four major feature groups.

| Feature Group | Count | Description |
|:--|--:|:--|
| Product and category metadata | 8 | Category, sub-category, product, brand, brand tier, festival, and store descriptors |
| Pricing and promotion | 8 | Base price, current price, discount, competitor price, promotion type, and marketing support |
| Shelf and supply-chain signals | 8 | Shelf capacity, shelf life, lead time, fill rate, delay, stock on hand, and safety stock context |
| Demand and engagement signals | 12 | Daily units sold, digital traffic, loyalty behavior, basket size, and demand proxies |

## 3.3 Targets used in the project

The project uses two distinct targets.

| Target | Type | Purpose |
|:--|:--|:--|
| `Daily_Units_Sold` | Regression | Used for demand forecasting and downstream revenue/profit estimation |
| `Stocking_Priority_Class` | Classification | Engineered target used to classify products into Low, Medium, or High stocking priority |

The demand target is directly observed. The stocking-priority target is engineered from business logic, which is appropriate because real stocking priority is usually a managerial decision variable rather than a naturally labeled field in the source data.

## 3.4 Data quality and preparation

The notebooks and training scripts indicate that the dataset required light but important preparation:

1. binary flags were standardized to numeric indicators
2. selected numeric columns were coerced to numeric and imputed where necessary
3. text-like business columns were normalized and combined into structured text representations
4. date columns were converted into calendar-derived features where relevant

The final dataset is therefore rich enough to support both exploratory analytics and production-style model pipelines.

# 4. Exploratory Data Analysis

Exploratory data analysis established the statistical and business context for the later modeling stages. It also helped determine which variables were structurally informative, which variables were redundant, and which transformations were worth carrying into later experiments.

## 4.1 Distribution of the demand target

The first question was whether the regression target, `Daily_Units_Sold`, had a reasonable distribution for supervised learning.

![Figure 1. Distribution of daily units sold.](./assets/eda_target_distribution.png){ width=90% }

The distribution is centered around a mean of **112.26 units** and a median of **113 units**, with a standard deviation of **28.58 units**. The interquartile range spans from **93** to **133** units. The closeness of the mean and median indicates that the target is not severely skewed, and the density curve suggests that the distribution is reasonably smooth rather than fragmented into disconnected modes. This is favorable for both linear and tree-based regressors.

![Figure 2. Boxplot of daily units sold.](./assets/eda_target_boxplot.png){ width=80% }

The boxplot confirms that the target contains some low and high extremes, but not in a way that suggests pathological outliers. The observed range extends from **17** to **204** units. That spread is wide enough to make forecasting meaningful, yet compact enough that simple regression families remain viable. This finding justified the use of classical baselines such as linear, Ridge, and tree-based regressors in Week 3.

## 4.2 Correlation analysis

Correlation analysis was used to understand which continuous variables moved with demand and which variables likely captured overlapping information.

![Figure 3. Correlation heatmap for selected numeric variables.](./assets/eda_correlation_heatmap.png){ width=95% }

Three insights stand out immediately. First, `Current_Price` has the strongest negative relationship with the target at approximately **-0.80**, which is consistent with basic price elasticity: higher selling prices generally suppress unit movement. Second, `Footfall_Index` has the strongest positive relationship with demand at approximately **0.44**, showing that customer traffic is a major commercial driver. Third, `Discount_Percentage` and `Social_Media_Sentiment` are both positively associated with demand, at roughly **0.23** and **0.22**, suggesting that both promotional pressure and consumer perception contribute to product movement.

The heatmap also reveals very high correlation among pricing variables such as `Base_Price`, `Current_Price`, and `Competitor_Price`. This is not surprising because these variables all describe related aspects of retail pricing. The implication for modeling is that multicollinearity must be handled carefully. Linear models can still be used, but their coefficients require interpretation with awareness of correlated predictors.

## 4.3 Feature importance from a demand perspective

To go beyond linear correlation, the EDA notebook estimated feature importance using a Random Forest regressor and then validated those findings with permutation importance.

![Figure 4. Random Forest feature importance for demand forecasting.](./assets/eda_random_forest_importance.png){ width=90% }

The Random Forest importance ranking is sharply dominated by `Current_Price` (**0.6235**) and `Footfall_Index` (**0.2043**). `Social_Media_Sentiment` follows at **0.0482**, while all remaining variables contribute much less. This indicates that the demand signal is concentrated in a few commercially meaningful drivers rather than being evenly spread across the full feature set.

![Figure 5. Permutation importance on the hold-out set.](./assets/eda_permutation_importance.png){ width=90% }

Permutation importance confirms the same conclusion. `Current_Price` remains the dominant feature with an importance decrease of roughly **1.027**, followed by `Footfall_Index` (**0.395**) and `Social_Media_Sentiment` (**0.061**). The consistency between the two importance methods is important. It shows that the signal is not an artifact of one model family. For the report, this supports a strong business interpretation: pricing discipline, store traffic, and customer perception are the primary drivers of retail demand in this dataset.

## 4.4 PCA and latent structure

Principal Component Analysis was used not as a production requirement, but as an exploratory device to understand whether broad latent factors existed across the numeric feature block.

![Figure 6. Cumulative explained variance from PCA.](./assets/eda_pca_cumulative.png){ width=85% }

The first principal component explains about **26.61%** of the variance. The first five components together explain approximately **65.35%** of the total variance. This implies that the dataset does contain shared latent structure across pricing, traffic, and operational variables, but not so strongly that a tiny component set can replace the original features without information loss. In practical terms, PCA was useful for exploration and dimensionality studies, but not necessary for the final deployed models.

## 4.5 Temporal demand patterns

Although the deployed app is not a classical time-series forecaster, temporal analysis remains useful because retail demand is often shaped by weekdays, weekends, and month-level seasonality.

![Figure 7. Average demand by day of week.](./assets/eda_demand_by_day.png){ width=85% }

Demand is slightly lower mid-week and rises during the weekend. The lowest observed day-level average is around **109.30 units** on Wednesday, while demand peaks at roughly **115.61** on Saturday and **116.49** on Sunday. The pattern is not extreme, but it is meaningful enough to justify retaining weekday and weekend flags in exploratory modeling and feature engineering.

![Figure 8. Average demand by month.](./assets/eda_demand_by_month.png){ width=90% }

Monthly variation is present but moderate. The highest monthly average appears in **July (116.38 units)**, followed by **November (114.28 units)**, while the lower months include **December (110.13 units)** and **February (110.60 units)**. This suggests that demand seasonality exists, but it is not the sole driver of the outcome. It acts more as contextual variation than as a dominant pattern.

## 4.6 Category and store-level segmentation

Category and store-level plots were used to understand whether the dataset exhibits strong structural differences across product classes or retail formats.

![Figure 9. Average demand by category.](./assets/eda_demand_by_category.png){ width=90% }

The category-level averages are relatively close, but still informative. `Grocery` has the highest average demand at **113.40 units**, followed closely by `Clothing` (**113.26**) and `Beauty` (**112.24**). `Electronics` is lowest at **110.69**. The small spread indicates that demand alone does not sharply separate categories. This helps explain why a separate stocking-priority target is valuable: a category may have respectable demand but still be disadvantaged by shelf-life or supply constraints.

![Figure 10. Average demand by store type.](./assets/eda_demand_by_store_type.png){ width=75% }

Urban stores show a marginally higher average demand (**112.46 units**) than rural stores (**111.96 units**). The difference is modest, which suggests that store type is useful context rather than a decisive determinant. This finding is consistent with the eventual modeling choice: store-type context is retained, but it is not treated as a dominant standalone predictor.

## 4.7 EDA summary

The exploratory phase established five strong conclusions:

1. the regression target is well-behaved enough for supervised learning
2. price and footfall are the dominant demand drivers
3. pricing variables are highly collinear and must be interpreted carefully
4. temporal and category-level effects are present, but not overwhelmingly large
5. demand alone cannot explain stocking decisions, which motivates a richer business target

# 5. Feature Engineering

Feature engineering was the most conceptually important part of the project, because it connected raw retail variables to the final business questions being solved.

## 5.1 Business-oriented target engineering

The most important engineered construct in the project is the stocking-priority target itself. Rather than using sales volume alone, the project constructs a business-oriented score from profitability and operational reliability.

The scripts and Week 4 notebook define the following intermediate variables:

1. **Unit Margin** = `Current_Price - Unit_Cost`
2. **Gross Profit** = `Unit_Margin × Daily_Units_Sold`
3. **Profit Density** = `Gross_Profit / Shelf_Capacity`

These variables are then normalized and combined into a stocking-priority score using the following weights:

\[
\text{Score} = 0.45 \cdot \text{ProfitDensity}_n
+ 0.20 \cdot \text{ShelfLife}_n
+ 0.20 \cdot \text{FillRate}_n
- 0.10 \cdot \text{SupplierDelay}_n
- 0.05 \cdot \text{BackorderFlag}_n
\]

This score is divided into three quantile-based classes:

- Low
- Medium
- High

The resulting class distribution is almost perfectly balanced: **667 High**, **667 Low**, and **666 Medium**. This is helpful for classification training, but more importantly it produces a label that reflects realistic merchandising trade-offs rather than raw movement alone.

## 5.2 Numerical feature engineering

The Week 3 feature-engineering notebooks explored a wide range of structured transformations:

1. calendar features such as weekday, month, holiday markers, and weekend flags
2. lag features for prior-demand context
3. rolling statistics for short-term demand behavior
4. price–promotion interaction features
5. store-level and product-level aggregation features
6. customer and supply-chain derived features
7. standardization and PCA on numeric blocks

These transformations were academically valuable because they showed how demand behavior can be enriched through context. However, the final deployed system deliberately uses a narrower numeric feature block. The reason is architectural: live API inference often occurs for a single hypothetical product scenario, where historical lag windows or rolling demand histories may not be available. The deployment therefore favors features that can be supplied directly at inference time.

The final numeric features used in the operational models are:

- current price
- shelf capacity
- lead time
- marketing spend
- shelf life
- fill rate
- supplier delay
- discount percentage
- competitor price
- footfall index
- average temperature
- rainfall
- Google Trends current week
- Google Trends lag 1 week
- app traffic index
- website visits
- loyalty usage count
- repeat purchase rate
- average basket size

This selection creates a strong balance between explanatory richness and deployability.

## 5.3 Text feature engineering

Text representation was explored extensively in Week 3 and Week 4 because product semantics matter in retail. Category, product name, brand, and promotion information all contain useful business cues that are hard to capture with purely numeric models.

The notebooks evaluated four main text-representation strategies:

1. bag-of-words
2. TF-IDF
3. Word2Vec-style embeddings
4. BERT / transformer embeddings

The important insight from this exploration was that unstructured text should not simply be concatenated carelessly. The improved approach was a **column-aware text template**, which preserves the role of each token in business context. The deployed template is:

`Category: ... | Product: ... | SubCategory: ... | Brand: ... | BrandTier: ... | Promotion: ... | Festival: ... | StoreType: ...`

This structure matters because it allows a lightweight TF-IDF + logistic pipeline to distinguish brand, category, and promotion semantics in a more meaningful way than a flat text string.

## 5.4 Scaling and interpretability

Standardization was used for the numeric features in the final deployed models. This serves two purposes:

1. it helps optimization in linear models such as logistic regression and Ridge regression
2. it makes coefficient magnitudes more comparable within a model family

This decision improves interpretability. In the final insight layer, coefficients can be discussed directly as business levers, such as the positive role of fill rate and shelf life or the negative role of supplier delay.

## 5.5 Leakage control

One of the strongest technical features of the final project is that leakage is explicitly acknowledged and controlled.

For the stocking-priority classifier, the following variables are excluded from the live feature set:

- `Daily_Units_Sold`
- `Unit_Margin`
- `Gross_Profit`
- `Profit_Density`
- `Stocking_Priority_Score`
- `Stocking_Priority_Class`

For the deployed sales regression model, post-outcome columns such as `Online_Sales_Units` and `In_Store_Sales_Units` are excluded. This is crucial because the Week 3 regression notebook demonstrated what happens when leakage is present: linear regression produced nearly perfect metrics because sales decomposition variables implicitly revealed the target. That result was analytically useful as a warning sign, but it is not appropriate for deployment.

The final production pipeline is therefore much more defensible than the early baseline experiments because it distinguishes exploratory experimentation from operational modeling.

# 6. Model Development

The modeling phase evolved in stages. Early work emphasized demand forecasting baselines and feature experimentation, while later work focused on the final retail decision-support architecture.

## 6.1 Week 3 regression baselines

The Week 3 notebook compared several baseline regressors on the engineered dataset.

| Model | MAE | RMSE | R² |
|:--|--:|--:|--:|
| Linear Regression | 0.0000 | 0.0000 | 1.0000 |
| Ridge Regression | 0.0441 | 0.0570 | 1.0000 |
| Lasso Regression | 0.1086 | 0.1342 | 1.0000 |
| Random Forest Regressor | 1.0511 | 1.9304 | 0.9955 |

At first glance these numbers appear extraordinary, but they must be interpreted carefully. The same notebook reports very high importance for `In_Store_Sales_Units` and `Online_Sales_Units`. Since those variables are decomposition-level views of the sales outcome, they effectively leak the target into the model. The near-perfect fit therefore reflects information leakage rather than genuine forecasting power.

This stage of the project was still valuable because it revealed exactly why a stricter feature policy was needed. The experience directly informed the final deployed sales model, which removed post-outcome variables and retained only inference-available business features.

## 6.2 Final operational sales model

The final deployed sales model is a **log-transformed Ridge regressor** implemented through `TransformedTargetRegressor` in the training script. The model receives the same column-aware text template used elsewhere, along with the leakage-free numeric business block.

This model was chosen because:

1. Ridge regression is stable under multicollinearity, which is important for price-related variables
2. the log transformation helps manage positive demand targets with moderate spread
3. the model is lightweight, fast, and easy to serve in FastAPI
4. its outputs can be translated into revenue, profit, and shelf-utilization summaries for the frontend

## 6.3 Stocking-priority classification models

The project evaluated multiple logistic-regression variants:

1. text-only logistic regression
2. numeric-only logistic regression
3. hybrid logistic regression combining text and numeric features

The rationale for this family comparison was straightforward. A text-only model can test how much semantic product context matters. A numeric-only model can test the power of structured operational features. A hybrid model can determine whether combining both views produces a more balanced signal.

## 6.4 Custom deep learning model

The Week 4 notebook also implemented a custom deep learning classifier that combined text-style input with structured business context. The academic motivation was clear: a neural architecture could potentially capture non-linear interactions among promotions, category semantics, supply variables, and commercial signals in ways that linear models cannot.

However, the project also recognized the deployment trade-off. A custom deep model increases dependency complexity, tuning burden, runtime overhead, and explainability cost. These issues matter more in a capstone demo environment than in a purely research-oriented notebook.

## 6.5 Hugging Face transformer benchmark

The Hugging Face benchmark was included as a modern NLP comparison point. It tests whether richer language representations help when the business context is encoded as a structured text template.

This was academically useful because it establishes that the project explored contemporary NLP methods rather than relying only on classical pipelines. At the same time, the report must be honest: the transformer setup is text-only, so it underuses structured operational constraints such as fill rate, shelf life, and supplier delay. That mismatch is one reason it was not chosen for deployment.

## 6.6 Final deployed model selection

The final deployed application uses:

- **Hybrid Logistic Regression** for stocking-priority classification
- **Log-Ridge Sales Regression** for demand forecasting

These models were selected because they provide a good balance across four criteria:

1. predictive adequacy
2. business interpretability
3. deployment simplicity
4. runtime stability

This selection logic is important. The project does not claim that the simplest model is always the numerically best model in every experiment. Instead, it argues that the chosen models provide the strongest practical balance for a robust academic demo and decision-support application.

# 7. Model Evaluation

Model evaluation in this project should be interpreted in two layers:

1. **operational experiments** that support the deployed app
2. **broader Week 4 comparisons** that document the full model-exploration story

These two views are complementary, but they are not numerically identical because they arise from different experiment workflows.

## 7.1 Operational classification experiments

The precomputed operational classification results compare a numeric-only logistic baseline against a small sweep of hybrid logistic models.

| Model Variant | Accuracy | Macro F1 | Weighted F1 |
|:--|--:|--:|--:|
| Logistic Regression (numeric-only baseline) | 0.8200 | 0.8203 | 0.8204 |
| Hybrid Logistic Regression (C=0.5) | 0.8150 | 0.8154 | 0.8155 |
| Hybrid Logistic Regression (C=1.0) | 0.8100 | 0.8097 | 0.8098 |
| Hybrid Logistic Regression (C=1.5) | 0.8050 | 0.8051 | 0.8052 |
| Hybrid Logistic Regression (C=2.0) | 0.7975 | 0.7977 | 0.7978 |

![Figure 11. Operational classification experiment comparison.](./assets/models_classification_weighted_f1.png){ width=92% }

The most important observation here is nuanced. In this particular operational sweep, the **numeric-only baseline slightly outperforms the hybrid sweep**. This implies that the engineered stocking-priority label is already heavily explained by structured business variables such as fill rate, shelf life, pricing, and supplier behavior. That is a reasonable result because the label itself was constructed from business quantities derived from those variables.

However, it would be incorrect to conclude from this one table that text is useless. The hybrid model remains valuable for deployment because product semantics, category context, brand cues, and promotion language are useful for live business scenarios and for the broader Week 4 comparison discussed later.

![Figure 12. Confusion matrix for the hybrid logistic classification experiment.](./assets/models_classification_confusion_matrix.png){ width=68% }

The confusion matrix shows that the **Medium** class is the most difficult to identify cleanly. Low and High are classified more confidently, while Medium is often confused with its neighboring classes. This is expected in a three-level merchandising problem because Medium typically represents the boundary zone where attractive and risky signals coexist.

## 7.2 Operational sales regression experiments

The deployed sales model family was evaluated using a Ridge alpha sweep.

| Model Variant | MAE | RMSE | R² |
|:--|--:|--:|--:|
| Ridge alpha=5.0 | 9.5546 | 11.9143 | 0.8193 |
| Ridge alpha=2.0 | 9.6470 | 12.0334 | 0.8157 |
| Ridge alpha=1.0 | 9.7058 | 12.1194 | 0.8130 |
| Ridge alpha=0.5 | 9.7626 | 12.2001 | 0.8105 |

![Figure 13. Sales regression experiment comparison.](./assets/models_regression_rmse.png){ width=82% }

These results are realistic and credible. RMSE stays in a narrow band of about **11.9 to 12.2 units**, while R² remains between **0.81 and 0.82**. This tells us three things. First, the sales task is learnable with a classical linear model. Second, the feature block captures meaningful commercial signal without relying on leakage. Third, more complex demand models are not strictly necessary for a stable deployed demo.

The deployed artifact uses the `alpha=1.0` variant for consistency and simplicity, while the artifact summary also records that the best offline RMSE in the sweep came from `alpha=5.0`.

## 7.3 Week 4 model-lab comparison

The broader Week 4 benchmark compares the major classification families explored in the capstone.

| Model | Accuracy | Weighted F1 | Runtime Status |
|:--|--:|--:|:--|
| Logistic Regression (hybrid) | 0.7567 | 0.7563 | Live compare and deployed family |
| Logistic Regression (numeric-only) | 0.7433 | 0.7441 | Live compare |
| Custom Deep Learning Model | 0.4833 | 0.4589 | Benchmark-only |
| Logistic Regression (text-only) | 0.4400 | 0.4314 | Live compare |
| Hugging Face Transformer Model | 0.4267 | 0.3666 | Benchmark-only |

![Figure 14. Week 4 model-lab comparison.](./assets/models_model_lab_comparison.png){ width=95% }

This benchmark is important because it answers a different research question from the operational sweep. In this broader comparison, the **hybrid logistic model performs best overall**, outperforming both the numeric-only and text-only logistic baselines and dramatically outperforming the text-only transformer benchmark. The deep learning model improves over text-only baselines, but it still falls well below the hybrid logistic model while being far more expensive to operationalize.

The result supports an academically mature conclusion: model sophistication alone does not guarantee better performance. In this retail context, **representation quality and feature alignment with the business problem matter more than architectural complexity**.

## 7.4 Reconciling the two evaluation views

At first glance, the operational classification sweep and the Week 4 model-lab benchmark may seem inconsistent because one shows the numeric-only baseline slightly ahead, while the other shows the hybrid model ahead. This is not an error; it is a consequence of comparing different experimental workflows:

1. the operational sweep is a narrow deployment-focused comparison against the engineered label
2. the model-lab benchmark is a broader representation study across multiple modeling families

The report should therefore avoid over-claiming. The correct interpretation is:

- structured features are extremely informative for the engineered business target
- adding text is still useful when representation design is handled properly
- the hybrid model offers the best practical balance for live deployment and academic explanation

# 8. System Architecture

The final capstone is not only a modeling exercise; it is an integrated software system. The architecture combines data processing, model inference, business-logic translation, API exposure, and a dashboard-oriented frontend.

## 8.1 Layered architecture

| Layer | Main Components | Purpose |
|:--|:--|:--|
| Data and artifacts | `data/raw/`, `data/processed/`, `models/` | Store raw data, precomputed insights, and serialized runtime artifacts |
| Model layer | priority classifier, sales regressor, scenario simulator, recommender | Produce predictions and translate them into business metrics |
| API layer | FastAPI routes in `app/main.py` | Expose prediction, recommendation, history, and insights endpoints |
| Presentation layer | Jinja template, JavaScript dashboard, CSS styling | Provide a business-friendly UI for demonstrations |

The layered organization makes the project easier to explain and maintain. It also aligns well with academic expectations because it clearly separates modeling logic from software delivery logic.

## 8.2 API design

The FastAPI application exposes the following key routes:

| Endpoint | Method | Purpose |
|:--|:--|:--|
| `/predict` | POST | Predict Low/Medium/High stocking priority |
| `/predict/sales` | POST | Predict daily units sold and business metrics |
| `/recommend` | POST | Rank items under business-specific objectives |
| `/query/historical` | POST | Filter historical data for evidence and comparisons |
| `/simulate` | POST | Compare one product across multiple business scenarios |
| `/insights/summary` | GET | Dataset and modeling summary |
| `/insights/model-performance` | GET | Precomputed evaluation tables |
| `/insights/feature-importance` | GET | Coefficient-based and semantic drivers |
| `/insights/business-findings` | GET | Business findings from saved artifacts |
| `/insights/model-comparison` | GET | Week 4 model-lab benchmark summary |
| `/predict/compare-models` | POST | Live scenario comparison across available classification models |
| `/ui` and `/demo` | GET | Frontend interface and demo landing page |

This route design is important because it maps directly onto the business workflow demonstrated in the frontend: input, prediction, recommendation, and insight.

## 8.3 Frontend architecture

The frontend is implemented inside the same FastAPI project using:

- a Jinja template for layout
- JavaScript for orchestration, API calls, and rendering
- CSS for dashboard styling

The upgraded interface includes a **Business Demo Dashboard** that sits on top of the technical views. This is a strong architectural choice for a capstone because it preserves the technical transparency of the API while also making the system intelligible to a non-technical coordinator in under a minute.

## 8.4 Runtime resilience

One practical engineering improvement in the final system is its resilience to serialized model incompatibilities. If a saved scikit-learn artifact cannot be loaded because of an environment mismatch, the application can rebuild the operational model from the local dataset rather than failing outright.

This matters in an academic submission context because it reduces the risk of a live demonstration failing for non-conceptual reasons.

# 9. Results and Business Insights

The final value of the project is not only that it produces predictive scores, but that it translates those scores into business insight.

## 9.1 Category-level stocking-priority patterns

![Figure 15. Share of high-priority records by category.](./assets/business_high_priority_share_by_category.png){ width=90% }

The strongest category-level result is the dominance of **Home**, where approximately **75.45%** of records fall into the High-priority class. In contrast, **Grocery** has only **7.24%** High-priority records. This difference cannot be explained by demand alone, because grocery also has the highest average units sold. The deeper explanation lies in operational context: Home products have very long average shelf life (**2,222 days**) and low spoilage risk, while Grocery has an average shelf life of only **42.65 days**.

This is an important business insight. It shows that the system is doing more than predicting movement. It is identifying products whose commercial upside can actually be converted into reliable inventory decisions.

## 9.2 Profit density and commercial efficiency

The artifact summaries show that **Beauty** has the highest average profit density at **31.51**, followed by **Clothing (28.07)** and **Electronics (25.79)**. Yet Beauty does not dominate the High-priority class in the same way Home does. This means that profit density alone is insufficient. A category may be commercially efficient but still be limited by other operational factors such as shelf life or replenishment variability.

This finding justifies the multi-factor recommendation engine. It would be overly simplistic to rank products only by gross profit or only by demand.

## 9.3 Operational risk signals

The risk findings from the final artifacts are especially revealing:

- **8.1%** of records fall below the short shelf-life threshold used by the business-insight service
- **33.45%** of records fall below the low fill-rate threshold
- **38.75%** of records trigger at least one major risk condition

These values explain why the frontend surfaces caution flags so prominently. In a dataset where more than one-third of records carry operational risk, a demand-only dashboard would be academically incomplete and practically misleading.

## 9.4 Interpretable business drivers

The coefficient-based analysis of the deployed linear models produces clear business levers.

### Drivers of high stocking priority

| Feature | Coefficient | Business Interpretation |
|:--|--:|:--|
| Fill Rate Pct | 3.4453 | Reliable replenishment strongly supports stocking confidence |
| Shelf Life Days | 3.2460 | Longer shelf life lowers spoilage risk |
| Current Price | 1.1707 | Higher-value items can support stronger stocking economics |
| Website Visits | 0.0811 | Customer attention helps reinforce priority |

### Drivers of low stocking priority

| Feature | Coefficient | Business Interpretation |
|:--|--:|:--|
| Supplier Delay Days | 1.3503 | Delays weaken confidence in maintaining availability |
| Competitor Price | 1.0146 | Competitive pricing pressure affects attractiveness |
| Discount Percentage | 0.7038 | Discounting alone does not guarantee a better stocking decision |
| Shelf Capacity | 0.2812 | Large space requirements make an item less efficient |

### Drivers of higher sales

| Feature | Coefficient | Business Interpretation |
|:--|--:|:--|
| Footfall Index | 0.1032 | Customer traffic directly supports volume |
| Competitor Price | 0.0405 | Relative pricing matters for conversion |
| Loyalty Program Usage Count | 0.0394 | Repeat-customer engagement contributes to sales |
| Avg Basket Size | 0.0242 | Larger baskets reflect richer shopping missions |

These tables are valuable academically because they demonstrate that the final deployed system remains explainable. The project does not ask the evaluator to trust black-box outputs without reasoning.

## 9.5 Business interpretation of the integrated system

When the entire system is viewed end-to-end, three major business lessons emerge.

First, **demand and stocking priority are related but not identical**. Grocery can move quickly, but perishability and low fill-rate risk can still make it a weaker stocking candidate than more stable categories.

Second, **semantic product information is useful when it is structured carefully**. Text-only modeling was weak, but the hybrid model showed that semantic retail context can complement structured variables when encoded through a column-aware template.

Third, **deployment-quality systems require more than good notebook metrics**. The capstone matured when it moved from exploratory perfection caused by leakage to realistic, leakage-aware models that can run live inside FastAPI and explain themselves through a dashboard.

# 10. Conclusion

This capstone project successfully transforms a basic retail forecasting exercise into a much richer retail intelligence system for inventory optimization. The work begins with rigorous exploratory analysis, progresses through extensive feature engineering and model experimentation, and culminates in a deployable FastAPI application with a business-oriented frontend.

Several achievements make the final system academically defensible and practically convincing.

1. The project clearly identifies that retail stocking decisions cannot be reduced to sales alone.
2. It constructs a business-oriented target that combines profitability, shelf efficiency, and operational stability.
3. It evaluates multiple classical and modern model families rather than relying on a single convenient baseline.
4. It explicitly recognizes and corrects feature leakage in early regression experiments.
5. It deploys stable, interpretable models that can support live demonstration and business explanation.

The final deployed architecture is well aligned with the capstone objective. The hybrid logistic regression model supports business-aware stocking-priority classification, while the Ridge-based sales model provides realistic demand estimation and downstream profit context. Together, these models power a recommendation and insight layer that is more useful than isolated prediction endpoints.

From an academic standpoint, the strongest aspect of the project is not a single metric value. It is the quality of the overall reasoning: the project shows how to move from EDA to feature engineering, from baseline models to deployment-aware model selection, and from raw predictions to actionable business interpretation.

# 11. Future Work

The project establishes a strong foundation, but several extensions would further improve both academic rigor and production readiness.

## 11.1 Methodological improvements

1. unify the operational evaluation pipeline and the Week 4 model-lab benchmark under a single formal protocol so cross-table comparisons become fully consistent
2. perform more systematic hyperparameter tuning for both the classifier and regressor
3. use time-aware validation for the sales model instead of only random train-test splitting
4. add ablation studies showing the marginal contribution of text features, traffic features, and operational features

## 11.2 Modeling extensions

1. revisit deep learning only after establishing a stronger leakage-free structured baseline for hybrid tabular-text learning
2. explore gradient boosting or CatBoost-style regression for demand prediction
3. incorporate calibrated probabilities for the stocking-priority classifier
4. extend the scenario simulator with promotion elasticity and sensitivity analysis

## 11.3 System and product extensions

1. add downloadable executive reports from the recommendation engine
2. add frontend smoke tests and broader automated end-to-end testing
3. enable live artifact validation and model warm-up before demonstrations
4. integrate richer user roles so the same backend can serve both technical reviewers and business stakeholders

In summary, the current capstone already demonstrates a complete and well-reasoned retail intelligence system. Future work should build on this by tightening evaluation discipline, extending experimentation, and expanding the reporting capabilities of the deployed application.
