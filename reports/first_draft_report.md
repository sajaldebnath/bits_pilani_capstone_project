# First Draft Report
## Demand Forecasting and Retail Intelligence for Inventory Optimization

### 1. Abstract

This capstone project began as a demand forecasting exercise but evolved into a broader **retail intelligence system** for practical inventory and shelf decision support. In a real retail setting, the best product to stock is not always the one with the highest sales volume. Shelf capacity, profit density, shelf life, supplier reliability, and replenishment risk all affect whether an item should receive high stocking priority.

The current repository implements a multi-model FastAPI application with a dashboard interface. It includes:

- stocking-priority classification
- daily sales prediction
- historical querying and category comparisons
- recommendation ranking under multiple business goals
- scenario simulation for what-if analysis
- Model Insights for explaining the AI/ML pipeline
- Model Lab for showcasing additional Week 4 benchmark models

The project therefore now functions as both an operational prototype and an academic demonstration of how explainable machine learning can support retail inventory decisions.

### 2. Problem Statement

The central business problem addressed by this project is:

> How can a retailer decide which items deserve **Low**, **Medium**, or **High** stocking priority while balancing demand, profitability, shelf efficiency, and operational risk?

This framing is more useful than demand forecasting alone because several business realities matter simultaneously:

- high sales alone are not enough
- bulky products can consume valuable shelf space
- perishable products create spoilage risk
- supplier delay and poor fill rate can weaken replenishment confidence
- profit per shelf unit may matter more than total sales volume

The project therefore reframes a forecasting problem into a **retail decision-support problem**.

### 3. System Scope in the Current Repository

The current implementation in `bits_pilani_capstone_project` includes both operational workflows and presentation-oriented AI/ML explainability layers.

#### Operational workflows

1. `Stocking Priority Prediction`
2. `Sales Prediction`
3. `Recommendation Engine`
4. `Historical Query`
5. `Scenario Simulator`

#### AI/ML explainer workflows

6. `Model Insights`
7. `Model Lab`

This means the project is no longer just an API wrapper around a single classifier. It is now a more complete coordinator-facing retail intelligence application.

### 4. Dataset Overview

According to the current precomputed insights artifacts, the working retail dataset contains:

- **2,000 rows**
- **64 columns**

The feature space combines product, pricing, promotion, supply-chain, demand, and engagement information.

#### Main feature groups

| Feature Group | Count | Description |
|:--|--:|:--|
| Product and category metadata | 8 | Category, sub-category, product, brand, brand tier, festival, and store descriptors |
| Pricing and promotion | 8 | Price, discount, competitor price, promotion type, and marketing support |
| Shelf and supply-chain signals | 8 | Shelf capacity, shelf life, lead time, fill rate, supplier delay, stock context |
| Demand and engagement signals | 12 | Daily demand, traffic, loyalty, basket size, and trend proxies |

#### Targets used

The current application uses two targets:

| Target | Type | Purpose |
|:--|:--|:--|
| `Stocking_Priority_Class` | Classification | Used by the stocking-priority model |
| `Daily_Units_Sold` | Regression | Used by the sales prediction model |

#### Class distribution

The stocking-priority target is intentionally balanced:

| Class | Count | Percentage |
|:--|--:|--:|
| Low | 667 | 33.35% |
| Medium | 666 | 33.30% |
| High | 667 | 33.35% |

### 5. Target Construction and Feature Engineering

#### 5.1 Business-Oriented Target Construction

The stocking-priority target is not a directly observed business label. It is an engineered target built to reflect practical merchandising priorities.

The following business quantities are created:

- **Unit Margin** = `Current_Price - Unit_Cost`
- **Gross Profit** = `Unit_Margin × Daily_Units_Sold`
- **Profit Density** = `Gross_Profit / Shelf_Capacity`

A normalized composite score then combines:

- profit density
- shelf life
- fill rate
- supplier delay
- backorder risk

This score is binned into:

- Low
- Medium
- High

This target design helps the model learn stocking priority as a business decision rather than a pure sales signal.

#### 5.2 Text Template Design

To let a lightweight model capture product semantics without a heavy transformer dependency, the project creates a column-aware text template:

`Category: ... | Product: ... | SubCategory: ... | Brand: ... | BrandTier: ... | Promotion: ... | Festival: ... | StoreType: ...`

This allows the deployed logistic model to use category, product, brand, and promotion context together with numeric features.

#### 5.3 Numeric Features Used by the Operational Models

The main numeric features include:

- current price
- shelf capacity
- lead time
- marketing spend
- shelf life
- fill rate
- supplier delay
- discount percentage
- competitor price
- footfall and traffic signals
- website visits
- loyalty usage
- repeat purchase rate
- average basket size

#### 5.4 Leakage Control

The current repository explicitly avoids important sources of leakage:

- the classification model does **not** use `Daily_Units_Sold`, `Unit_Margin`, `Gross_Profit`, `Profit_Density`, or the final stocking-priority score as input features
- the sales model does **not** use post-outcome columns such as online and in-store realized sales splits
- recommendation scores are calculated **after** prediction, not fed back into model training

This is an important strength of the current implementation.

### 6. Operational Models Used in the App

#### 6.1 Stocking Priority Classifier

- Model family: **Hybrid Logistic Regression**
- Purpose: predict `Low`, `Medium`, or `High` stocking priority
- Inputs: text template plus structured numeric retail features
- Deployment endpoint: `POST /predict`

This model was retained because it is:

- explainable
- lightweight to serve
- stable in FastAPI
- strong enough for a near-term demo

#### 6.2 Sales Prediction Model

- Model family: **Log-transformed Ridge Regression**
- Purpose: predict `Daily_Units_Sold`
- Inputs: same business and product features used by the classifier
- Deployment endpoint: `POST /predict/sales`

This model supports downstream business workflows such as:

- recommendation ranking
- profit estimation
- scenario simulation

### 7. Additional Models Showcased in Model Lab

The project also documents explored Week 4 model families through the new `Model Lab` tab.

| Model | Scope in App | Status |
|:--|:--|:--|
| Logistic Regression (text-only) | Live side-by-side comparison | Available |
| Logistic Regression (numeric-only) | Live side-by-side comparison | Available |
| Logistic Regression (hybrid) | Live side-by-side comparison and deployed family | Available |
| Custom Deep Learning Model | Benchmark summary only | Research candidate |
| Hugging Face Transformer Model | Benchmark summary only | Research candidate |

The custom deep learning and Hugging Face models are intentionally shown as **benchmark-only** in the current application because no production-ready serving artifact is attached to the app runtime.

### 8. Performance Summary

The repository now exposes two complementary evaluation views:

1. **Model Insights experiments** for the current operational app
2. **Model Lab benchmarks** for the broader Week 4 model comparison story

These views support different presentation goals, so they should be read as complementary rather than as one single identical benchmark pipeline.

#### 8.1 Stocking-Priority Classification Experiments from Model Insights

The current precomputed Model Insights artifact compares a numeric-only logistic baseline with a small hybrid logistic sweep.

| Model Variant | Accuracy | Weighted F1 | Notes |
|:--|--:|--:|:--|
| Logistic Regression (numeric-only baseline) | 0.8200 | 0.8204 | Strong structured baseline |
| Hybrid Logistic Regression (`C=0.5`) | 0.8150 | 0.8155 | Best hybrid experiment in the current sweep |
| Hybrid Logistic Regression (`C=1.0`) | 0.8100 | 0.8098 | Close to deployed configuration |
| Hybrid Logistic Regression (`C=1.5`) | 0.8050 | 0.8052 | Slight decline |
| Hybrid Logistic Regression (`C=2.0`) | 0.7975 | 0.7978 | Larger regularization relaxation reduced stability |

The stored confusion matrix for this operational experiment view is:

| True / Predicted | Low | Medium | High |
|:--|--:|--:|--:|
| Low | 118 | 15 | 0 |
| Medium | 20 | 98 | 15 |
| High | 0 | 24 | 110 |

This indicates that the hardest class boundary remains the **Medium** class, which is reasonable because Medium represents the middle tradeoff region between risk and attractiveness.

#### 8.2 Sales Regression Experiments from Model Insights

The current sales model comparison uses a lightweight offline Ridge alpha sweep.

| Model Variant | MAE | RMSE | R² |
|:--|--:|--:|--:|
| Ridge `alpha=5.0` | 9.5546 | 11.9143 | 0.8193 |
| Ridge `alpha=2.0` | 9.6470 | 12.0334 | 0.8157 |
| Ridge `alpha=1.0` | 9.7055 | 12.1191 | 0.8130 |
| Ridge `alpha=0.5` | 9.7627 | 12.2001 | 0.8105 |

The app currently uses the Ridge family as a stable, explainable demand baseline. The performance pattern shows that the regression task is learnable without resorting to a more complex time-series or deep learning stack.

#### 8.3 Week 4 Model Comparison from Model Lab

The Model Lab artifact summarizes the broader explored classification models.

| Model | Accuracy | Weighted F1 | Runtime Status |
|:--|--:|--:|:--|
| Logistic Regression (hybrid) | 0.7567 | 0.7563 | Live compare and deployed family |
| Logistic Regression (numeric-only) | 0.7433 | 0.7441 | Live compare |
| Custom Deep Learning Model | 0.4833 | 0.4589 | Benchmark-only |
| Logistic Regression (text-only) | 0.4400 | 0.4314 | Live compare |
| Hugging Face Transformer Model | 0.4267 | 0.3666 | Benchmark-only |

In the current repository, the hybrid logistic model is the strongest practical benchmark in the Model Lab comparison and remains the selected deployed family because it offers:

- the best balanced benchmark within that experiment view
- interpretability through coefficients and simple preprocessing
- low serving complexity
- stable behavior inside the FastAPI app

### 9. Interpretability and Business Drivers

Because both deployed operational models are linear, coefficient-based interpretation is a useful part of the current app.

#### 9.1 Drivers of High Stocking Priority

The current feature-importance artifact highlights the following major numeric drivers for the High class:

| Feature | Coefficient | Business Interpretation |
|:--|--:|:--|
| Fill Rate Pct | 3.4453 | Higher supplier reliability supports higher stocking confidence |
| Shelf Life Days | 3.2460 | Longer shelf life reduces spoilage risk |
| Current Price | 1.1707 | Higher-value items can support better stocking economics |
| Website Visits | 0.0811 | Broader attention signal |

#### 9.2 Drivers of Low Stocking Priority

Key numeric drivers for the Low class include:

| Feature | Coefficient | Business Interpretation |
|:--|--:|:--|
| Supplier Delay Days | 1.3503 | Delivery delays weaken replenishment confidence |
| Competitor Price | 1.0146 | Relative pricing pressure can reduce attractiveness |
| Discount Percentage | 0.7038 | Heavy discounting may not offset weaker economics |
| Shelf Capacity | 0.2812 | Large space requirements can make an item less efficient |

#### 9.3 Drivers of Higher Sales

For the sales model, the top numeric sales drivers include:

- footfall index
- competitor price
- loyalty program usage count
- average basket size
- website visits
- app traffic index

These drivers align well with the business story that store traffic, digital demand signals, and customer engagement should influence expected daily demand.

### 10. Business Findings from the Current Artifacts

#### 10.1 Category-Level Findings

The current business findings artifact shows that the categories with the highest share of High-priority records are:

| Category | Records | High Priority Share (%) | Avg Profit Density | Avg Shelf Life Days |
|:--|--:|--:|--:|--:|
| Home | 391 | 75.45 | 22.38 | 2222.06 |
| Clothing | 378 | 34.13 | 28.07 | 943.53 |
| Electronics | 387 | 33.59 | 25.79 | 1394.49 |
| Beauty | 402 | 20.15 | 31.51 | 530.91 |
| Grocery | 442 | 7.24 | 24.23 | 42.65 |

This reinforces an important business lesson:

- categories with longer shelf life and stronger operational stability can receive higher stocking priority even when other categories also have good demand

#### 10.2 Perishability and Supply Risk

The current risk findings show:

- **8.1%** of records fall below the short shelf-life threshold
- **33.45%** fall below the fill-rate threshold
- **38.75%** carry at least one major risk flag

This supports the idea that recommendations should not simply maximize demand. They must also account for spoilage and replenishment risk.

### 11. Recommendation Engine Logic

The recommendation engine combines outputs from both operational models with rule-based business logic. It does not treat sales volume as the only answer.

The engine can optimize for:

- `maximize_sales`
- `maximize_profit`
- `maximize_profit_density`
- `minimize_perishability_risk`

Its scoring combines:

- predicted sales
- expected profit
- profit per shelf unit
- stocking-priority confidence
- operational stability

This is one of the strongest practical aspects of the current application because it makes the system look like a true retail decision-support tool instead of a single-model academic demo.

### 12. Application and Deployment Architecture

The current FastAPI application includes:

- `/predict`
- `/predict/batch`
- `/predict/sales`
- `/recommend`
- `/query/historical`
- `/simulate`
- `/insights/summary`
- `/insights/model-performance`
- `/insights/feature-importance`
- `/insights/business-findings`
- `/insights/model-comparison`
- `/predict/compare-models`
- `/ui`

The frontend is now organized into seven tabs and is designed to be coordinator-friendly, stable, and visually understandable.

An important engineering improvement in the current codebase is the runtime fallback for incompatible serialized scikit-learn artifacts. If a saved model cannot be loaded due to environment mismatch, the app can rebuild the operational models from the local dataset instead of failing immediately.

### 13. Current Limitations

Although the project is now much stronger than the earlier single-model version, some limitations remain.

1. The stocking-priority label is still an engineered target rather than a directly observed business label.
2. The custom deep learning and Hugging Face models are benchmark-only in the current runtime.
3. The dashboard is API-tested but does not yet include a dedicated browser-level end-to-end test.
4. Some experiment views are generated for different presentation purposes, so future work should unify them under one benchmark protocol for complete comparability.
5. The project currently favors explainability and stability over the most complex possible modeling approach.

### 14. Future Work

The most useful next steps are:

1. unify the operational and Model Lab benchmarking workflow under a single evaluation protocol
2. add lightweight end-to-end UI smoke testing for the dashboard
3. export manager-ready recommendation summaries as downloadable reports
4. add model warm-up or preflight validation before live demos
5. optionally package the deep learning or transformer models for live inference only if that remains practical and stable
6. add more visuals and formal ablation plots to the final written report

### 15. Conclusion

The project has successfully evolved from a basic demand forecasting idea into a richer **retail intelligence capstone**. It now combines interpretable machine learning, business-oriented target design, multiple decision-support workflows, and academic-facing AI/ML explanation layers.

The deployed hybrid logistic regression and sales regression models are suitable choices for the current demo and submission context because they balance:

- practical predictive value
- interpretability
- deployment simplicity
- runtime stability

The addition of Model Insights and Model Lab also strengthens the academic quality of the project by making the full modeling workflow visible rather than hiding it behind a single endpoint. Overall, the current repository represents a substantially more complete and defensible capstone system than the earlier stocking-priority-only version.
