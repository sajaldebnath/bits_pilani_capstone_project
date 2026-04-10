# First Draft Report
## Demand Forecasting for Retail Inventory Optimization Reframed as Stocking Priority Classification

### 1. Abstract

This project began as a demand forecasting problem but was extended into a more practical retail decision-support problem: predicting **stocking priority** for product instances. Instead of optimizing only for units sold, the revised formulation incorporates margin, shelf capacity, shelf life, and supply-chain risk. A hybrid text-plus-numeric classification model was developed and exposed through a FastAPI endpoint for deployment-ready inference.

The current implementation stage expands the system into a broader **retail intelligence tool** with:

- stocking-priority prediction
- daily sales prediction
- historical filtering and category comparisons
- recommendation ranking based on multiple optimization goals
- scenario simulation for what-if analysis

### 2. Problem Statement

In a real retail setting, the best product to stock is not always the product with the highest sales volume. For example, bulky low-margin products may consume more shelf space, while premium cosmetics or jewelry may generate higher profit density. Perishable items such as biscuits or grocery products may sell often but carry higher spoilage risk due to short shelf life.

The project therefore addresses the question:

> Which products should be assigned **Low**, **Medium**, or **High** stocking priority based on both commercial attractiveness and operational constraints?

### 3. Dataset

The dataset contains **2,000 records and 58 columns** spanning:

- pricing and discounts
- store and product metadata
- promotions and festivals
- demand and traffic signals
- shelf capacity and shelf life
- supply-chain reliability
- customer engagement indicators

### 4. Target Construction

A business-oriented target was created using:

- Unit Margin  
  $
  \text{Unit Margin} = \text{Current Price} - \text{Unit Cost}
  $

- Gross Profit  
  $
  \text{Gross Profit} = \text{Unit Margin} \times \text{Daily Units Sold}
  $

- Profit Density  
  $
  \text{Profit Density} = \frac{\text{Gross Profit}}{\text{Shelf Capacity}}
  $

A normalized scoring function combined:

- profit density
- shelf life
- fill rate
- supplier delay
- backorder risk

The score was then divided into three balanced classes:

- Low
- Medium
- High

### 5. Business Analysis

Category-level analysis showed that the proportion of **High** priority instances differed by category. Based on the current scoring formulation, the highest share of High priority records appeared in:

| Category    |   high_priority_share |
|:------------|----------------------:|
| Home        |             0.754476  |
| Clothing    |             0.34127   |
| Electronics |             0.335917  |
| Beauty      |             0.201493  |
| Grocery     |             0.0723982 |

Shelf-life analysis also revealed large differences across categories:

| Category    |   avg_shelf_life_days |
|:------------|----------------------:|
| Home        |             2222.06   |
| Clothing    |              943.532  |
| Electronics |             1394.49   |
| Beauty      |              530.913  |
| Grocery     |               42.6493 |

This supports the business argument that perishability must be included in stocking decisions.

### 6. Modeling Approach

The deployment-ready baseline model selected for the API is a **hybrid Logistic Regression classifier** using:

- a column-aware text template  
- structured numeric features

The text template is built as:

`Category: ... | Product: ... | SubCategory: ... | Brand: ... | BrandTier: ... | Promotion: ... | Festival: ... | StoreType: ...`

Numeric features include:

- Current Price
- Shelf Capacity
- Lead Time
- Marketing Spend
- Shelf Life
- Fill Rate
- Supplier Delay
- Discount Percentage
- Competitor Price
- Traffic and engagement signals

### 7. Baseline Performance

Using a stratified 80/20 split (random_state=42), the hybrid logistic regression model achieved the following on the held-out test set (400 records). The final artifact saved in `models/` is re-fitted on all 2,000 records after evaluation:

- Accuracy: **0.81**
- Weighted F1: **0.81**
- Macro F1: **0.81**

Confusion matrix:

|        |   Pred Low |   Pred Medium |   Pred High |
|:-------|-----------:|--------------:|------------:|
| Low    |        119 |            14 |           0 |
| Medium |         23 |            95 |          15 |
| High   |          0 |            24 |         110 |

Classification report:

|              |   precision |   recall |   f1-score |   support |
|:-------------|------------:|---------:|-----------:|----------:|
| High         |        0.88 |     0.82 |       0.85 |    134    |
| Low          |        0.84 |     0.89 |       0.87 |    133    |
| Medium       |        0.71 |     0.71 |       0.71 |    133    |
| accuracy     |             |          |       0.81 |       400 |
| macro avg    |        0.81 |     0.81 |       0.81 |    400    |
| weighted avg |        0.81 |     0.81 |       0.81 |    400    |

### 8. API Design

A FastAPI application was created with endpoints for:

- health check
- model metadata
- single prediction
- batch prediction

The API returns:

- predicted stocking priority
- class probabilities
- caution flags for short shelf life, supplier delay, and low fill rate

### 9. Practical Use

The current model can support:

- shelf allocation review
- stocking priority triage
- promotion planning
- risk-aware assortment decisions
- coordinator demo of an inference endpoint

### 10. Limitations

- The current target is engineered rather than sourced from an external business rulebook
- The baseline deployment model favors interpretability over maximum predictive complexity
- Future work should compare the API model with transformer and custom deep learning approaches under a stable deployment framework

### 11. Implementation Progress Update

The latest application version now includes:

1. the original stocking-priority classifier  
2. a sales prediction model for `Daily_Units_Sold`  
3. a historical query engine for filtered comparisons  
4. a recommendation engine that balances profit, sales, shelf density, and risk  
5. a scenario simulator for promotion, marketing, and shelf-life analysis  

### 12. Next Steps

1. Add richer evaluation tables for the sales model  
2. Add exportable manager-ready recommendation reports  
3. Add monitoring for drift in pricing and traffic distributions  
4. Extend the report with visuals and ablation studies
