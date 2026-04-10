# Model Lab Notes

## Purpose

The `Model Lab` tab is the academic-facing comparison space in the dashboard.

It is designed to answer:

- Which model families were explored beyond the deployed production flow?
- How did the Week 4 benchmark models compare?
- Why was the hybrid logistic regression family chosen for deployment?
- Which models can be compared live inside the app today?

## What is shown live

- Logistic Regression (text-only)
- Logistic Regression (numeric-only)
- Logistic Regression (hybrid)

These three variants support the `POST /predict/compare-models` workflow.

## What is shown as benchmark-only

- Custom Deep Learning Model
- Hugging Face Transformer Model

These are currently displayed from the saved Week 4 notebook benchmark results because no local runtime-serving artifact was attached to the app.

## Demo message

When presenting this tab, the key story is:

1. We explored multiple model families, not just one.
2. The hybrid logistic model produced the best balanced practical performance.
3. The custom deep learning model was promising, but less deployment-friendly.
4. The Hugging Face model was useful as a modern NLP benchmark, but text-only context underused the structured business fields.
5. The deployed choice was made not only on score, but also on interpretability, stability, and simplicity for a near-term demo.
