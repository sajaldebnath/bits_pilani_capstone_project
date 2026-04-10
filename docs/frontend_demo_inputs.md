# Frontend Demo Inputs

## Tab 1: Business Demo Dashboard
- Default landing page:
  - Open `/demo` or `/ui`
  - Demo Mode starts enabled and the Business Demo Dashboard is active by default
- Quick scenarios:
  - High-demand premium electronics
  - Perishable grocery item
  - High-promotion beauty product
  - Low-margin bulky product
  - High-risk delayed-supply item
- Recommended coordinator talking points:
  - Start from the executive overview
  - Click one quick scenario card
  - Show the unified output cards for priority, sales, recommendation, and risk
  - Use the side-by-side scenario comparison buttons
  - Finish with the built-in Model Insights Summary

## Tab 2: Stocking Priority Prediction
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

## Tab 3: Sales Prediction
- Home demo:
  - Storage Box Set
  - Mid tier
  - Seasonal Discount
  - Shelf life 1800 days
  - Shelf capacity 45
- Coordinator talking point:
  - Compare predicted daily units with profit-per-shelf-unit and capacity utilization

## Tab 4: Recommendation Engine
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

## Tab 5: Historical Query
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

## Tab 6: Scenario Simulator
- Flash sale demo:
  - Base product = Lakme Lipstick
  - Compare No Promotion vs Flash Sale vs Festival Push
- Shelf-life demo:
  - Compare long shelf life vs tighter shelf life vs perishable risk

## Tab 7: Model Insights
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

## Tab 8: Model Lab
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
1. Start on Business Demo Dashboard and click one of the quick scenarios.
2. Explain the full Input → Prediction → Recommendation → Insight story from the top-level cards.
3. Use the scenario comparison buttons to show business trade-offs on the same product.
4. Use the built-in Model Insights Summary before moving anywhere else.
5. If needed, open the technical tabs for deeper endpoint-level validation.
