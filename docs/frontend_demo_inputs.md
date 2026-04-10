# Frontend Demo Inputs

## Tab 1: Stocking Priority Prediction
- High / Flags Off:
  - Samsung Computers 1018
  - Predicted High priority
  - No caution flags
- Medium / Flag On:
  - Tupperware Bedding 1017
  - Predicted Medium priority
  - Low fill rate caution flag
- Low / Flags On:
  - Tata Spices 1016
  - Predicted Low priority
  - Short shelf life and low fill rate caution flags

## Tab 2: Sales Prediction
- Home demo:
  - Storage Box Set
  - Mid tier
  - Seasonal Discount
  - Shelf life 1800 days
  - Shelf capacity 45
- Coordinator talking point:
  - Compare predicted daily units with profit-per-shelf-unit and capacity utilization

## Tab 3: Recommendation Engine
- Core portfolio demo:
  - Sony Headphones
  - Lakme Lipstick
  - Nestle Biscuits Pack
  - Storage Box Set
  - Premium Polo Shirt
- Use these optimization goals live:
  - Maximize Profit
  - Maximize Sales
  - Maximize Profit Density
  - Minimize Perishability Risk

## Tab 4: Historical Query
- Grocery risk query:
  - Category = Grocery
  - Brand tier = Budget
  - Promotion = BOGO
  - Shelf life max = 30
  - Sort by = Units Sold
- Premium profit query:
  - Brand tier = Premium
  - Promotion = Flash Sale
  - Price min = 20
  - Sort by = Profit Density

## Tab 5: Scenario Simulator
- Flash sale demo:
  - Base product = Lakme Lipstick
  - Compare No Promotion vs Flash Sale vs Festival Push
- Shelf-life demo:
  - Compare long shelf life vs tighter shelf life vs perishable risk

## Tab 6: Model Insights
- Start with Dataset Overview:
  - point out rows, columns, and the two targets
- Move to Feature Engineering:
  - show the text template and leakage exclusions
- Use Models Used:
  - explain why Hybrid Logistic Regression and Sales Regression were deployed
- Use Performance Comparison:
  - mention the hybrid classifier outperformed the numeric-only baseline
  - mention the sales model uses precomputed offline experiments, not live tuning
- Use Feature Importance:
  - highlight fill rate, shelf life, supplier delay, and marketing-related drivers
- End with Business Findings:
  - show which categories dominate High priority
  - explain why perishability and fill rate remain business constraints

## Tab 7: Model Lab
- Use Electronics Compare:
  - show the three live logistic variants side by side
  - point out that the deep learning and Hugging Face models are benchmark-only in the current local app
- Use the benchmark summary:
  - Hybrid Logistic Regression weighted F1 = 0.4670
  - Custom Deep Learning weighted F1 = 0.4589
  - Hugging Face DistilBERT weighted F1 = 0.3666
- Use the deployment section:
  - explain that the deployed choice balanced performance, interpretability, stability, and deployment ease

## Recommended coordinator flow
1. Start on Stocking Priority and click the High / Medium / Low sample buttons to show the full spread of outcomes.
2. Move to Sales Prediction to show that demand alone is now estimated explicitly.
3. Open Recommendation Engine and switch goals to show business trade-offs.
4. Use Historical Query to prove recommendations are supported by data slices.
5. Finish with Scenario Simulator for promotion and shelf-life what-if analysis.
6. Open Model Insights to explain the AI/ML design, experiments, and coordinator-facing evidence.
7. Finish in Model Lab to show the full Week 4 experimentation story and justify why the hybrid logistic model was deployed.
