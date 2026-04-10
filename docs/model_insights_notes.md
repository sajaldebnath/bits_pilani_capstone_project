# Model Insights Demo Notes

Use the **Model Insights** tab as the AI/ML explanation layer for the coordinator.

## Suggested talk track

1. Dataset Overview
   - Explain that the project uses a retail dataset with product, pricing, demand, shelf, and supply-chain features.
   - Point out that the app supports one classification target and one regression target.

2. Feature Engineering
   - Show the text template and explain why it lets a lightweight model use product semantics.
   - Highlight that engineered profit features were used for target construction and offline analysis.
   - Emphasize leakage control by listing excluded features.

3. Models Used
   - Explain that the deployed app intentionally favors interpretable and stable models for demo use.
   - Mention that deep learning and Hugging Face options are documented as research candidates, not live runtime dependencies.

4. Performance Comparison
   - Use the comparison tables to show that hybrid text + numeric modeling outperformed the numeric-only baseline.
   - Point out the confusion matrix and the precomputed regression experiment sweep.

5. Feature Importance
   - Translate coefficients into business language:
     - fill rate and shelf life help
     - supplier delay hurts
     - marketing and traffic signals support sales

6. Business Findings
   - Show category-level high-priority patterns.
   - Explain why perishability and replenishment risk remain important constraints even when demand is strong.

7. Tuning / Experiment Summary
   - Mention that only lightweight offline sweeps were used.
   - Clarify that the coordinator demo does not retrain models live.
