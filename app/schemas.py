from typing import Any, Dict, List, Literal, Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class ProductFeatures(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    category: str = Field(
        ...,
        validation_alias=AliasChoices("category", "Category"),
        description="Top-level product category.",
    )
    product_name: str = Field(
        ...,
        validation_alias=AliasChoices("product_name", "Product_Name"),
        description="Product name.",
    )
    brand_tier: str = Field(
        ...,
        validation_alias=AliasChoices("brand_tier", "Brand_Tier"),
        description="Brand tier: Budget, Mid, or Premium.",
    )
    promotion_type: str = Field(
        ...,
        validation_alias=AliasChoices("promotion_type", "Promotion_Type"),
        description="Promotion type. Use 'Unknown' if not applicable.",
    )

    sub_category: str = Field(
        "General",
        validation_alias=AliasChoices("sub_category", "Sub_Category"),
        description="Sub-category of the product.",
    )
    brand_name: str = Field(
        "Unknown",
        validation_alias=AliasChoices("brand_name", "Brand_Name"),
        description="Brand name.",
    )
    festival_name: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("festival_name", "Festival_Name"),
        description="Festival or event name if applicable.",
    )
    store_type: str = Field(
        "General",
        validation_alias=AliasChoices("store_type", "Store_Type"),
        description="Store format such as Urban or Rural.",
    )

    current_price: float = Field(
        ...,
        ge=0,
        validation_alias=AliasChoices("current_price", "Current_Price"),
        description="Current selling price.",
    )
    shelf_capacity: float = Field(
        ...,
        ge=0,
        validation_alias=AliasChoices("shelf_capacity", "Shelf_Capacity"),
        description="Number of units the shelf can hold.",
    )
    lead_time_days: float = Field(
        ...,
        ge=0,
        validation_alias=AliasChoices("lead_time_days", "Lead_Time_Days"),
        description="Supplier lead time in days.",
    )
    marketing_spend: float = Field(
        ...,
        ge=0,
        validation_alias=AliasChoices("marketing_spend", "Marketing_Spend"),
        description="Marketing spend in currency units.",
    )
    shelf_life_days: float = Field(
        ...,
        ge=0,
        validation_alias=AliasChoices("shelf_life_days", "Shelf_Life_Days"),
        description="Product shelf life in days.",
    )
    fill_rate_pct: float = Field(
        ...,
        ge=0,
        le=100,
        validation_alias=AliasChoices("fill_rate_pct", "Fill_Rate_Pct"),
        description="Fill rate as a percentage.",
    )
    supplier_delay_days: float = Field(
        ...,
        ge=0,
        validation_alias=AliasChoices("supplier_delay_days", "Supplier_Delay_Days"),
        description="Average supplier delay in days.",
    )

    discount_percentage: float = Field(
        0.0,
        ge=0,
        le=100,
        validation_alias=AliasChoices("discount_percentage", "Discount_Percentage"),
    )
    competitor_price: float = Field(
        0.0,
        ge=0,
        validation_alias=AliasChoices("competitor_price", "Competitor_Price"),
    )
    footfall_index: float = Field(
        0.0,
        ge=0,
        validation_alias=AliasChoices("footfall_index", "Footfall_Index"),
    )
    avg_temperature: float = Field(
        25.0,
        validation_alias=AliasChoices("avg_temperature", "Avg_Temperature"),
    )
    rainfall_mm: float = Field(
        0.0,
        ge=0,
        validation_alias=AliasChoices("rainfall_mm", "Rainfall_mm"),
    )
    google_trends_current_wk: float = Field(
        50.0,
        ge=0,
        le=100,
        validation_alias=AliasChoices("google_trends_current_wk", "Google_Trends_Current_Wk"),
    )
    google_trends_lag_1w: float = Field(
        50.0,
        ge=0,
        le=100,
        validation_alias=AliasChoices("google_trends_lag_1w", "Google_Trends_Lag_1w"),
    )
    app_traffic_index: float = Field(
        50.0,
        ge=0,
        validation_alias=AliasChoices("app_traffic_index", "App_Traffic_Index"),
    )
    website_visits: float = Field(
        500.0,
        ge=0,
        validation_alias=AliasChoices("website_visits", "Website_Visits"),
    )
    loyalty_program_usage_count: float = Field(
        100.0,
        ge=0,
        validation_alias=AliasChoices(
            "loyalty_program_usage_count",
            "Loyalty_Program_Usage_Count",
        ),
    )
    repeat_purchase_rate: float = Field(
        0.25,
        ge=0,
        le=1,
        validation_alias=AliasChoices("repeat_purchase_rate", "Repeat_Purchase_Rate"),
    )
    avg_basket_size: float = Field(
        3.0,
        ge=0,
        validation_alias=AliasChoices("avg_basket_size", "Avg_Basket_Size"),
    )


class PredictionResponse(BaseModel):
    predicted_stocking_priority: str
    probabilities: Dict[str, float]
    caution_flags: List[str]
    model_name: str


class BatchPredictionRequest(BaseModel):
    items: List[ProductFeatures]


class BatchPredictionResponse(BaseModel):
    results: List[PredictionResponse]


class SalesSupportingInformation(BaseModel):
    reference_group: str
    reference_sample_size: int
    category_average_daily_units: float
    comparison_to_reference_pct: float
    estimated_unit_cost: float
    estimated_unit_margin: float
    profit_per_shelf_unit: float
    shelf_capacity_utilization_pct: float


class SalesPredictionResponse(BaseModel):
    predicted_daily_units_sold: float
    predicted_daily_revenue: float
    predicted_daily_profit: float
    sales_band: str
    supporting_information: SalesSupportingInformation
    caution_flags: List[str]
    model_name: str


class HistoricalQueryRequest(BaseModel):
    categories: Optional[List[str]] = None
    brand_tiers: Optional[List[str]] = None
    promotion_types: Optional[List[str]] = None
    store_types: Optional[List[str]] = None
    festival_names: Optional[List[str]] = None
    sub_categories: Optional[List[str]] = None
    brand_names: Optional[List[str]] = None
    price_min: Optional[float] = Field(None, ge=0)
    price_max: Optional[float] = Field(None, ge=0)
    shelf_life_min: Optional[float] = Field(None, ge=0)
    shelf_life_max: Optional[float] = Field(None, ge=0)
    fill_rate_min: Optional[float] = Field(None, ge=0, le=100)
    fill_rate_max: Optional[float] = Field(None, ge=0, le=100)
    marketing_spend_min: Optional[float] = Field(None, ge=0)
    marketing_spend_max: Optional[float] = Field(None, ge=0)
    supplier_delay_max: Optional[float] = Field(None, ge=0)
    sort_by: Literal[
        "avg_daily_units_sold",
        "avg_gross_profit",
        "avg_profit_density",
        "high_priority_share",
    ] = "avg_profit_density"
    top_n: int = Field(10, ge=1, le=25)


class HistoricalSummaryCards(BaseModel):
    avg_daily_units_sold: float
    avg_gross_profit: float
    avg_profit_density: float
    avg_fill_rate_pct: float
    high_priority_share: float


class HistoricalProductSummary(BaseModel):
    rank: int
    product_name: str
    category: str
    sub_category: str
    brand_name: str
    brand_tier: str
    records: int
    avg_daily_units_sold: float
    avg_current_price: float
    avg_gross_profit: float
    avg_profit_density: float
    avg_fill_rate_pct: float
    avg_shelf_life_days: float
    high_priority_share: float


class CategoryComparisonRow(BaseModel):
    category: str
    records: int
    avg_daily_units_sold: float
    avg_gross_profit: float
    avg_profit_density: float
    avg_fill_rate_pct: float
    avg_shelf_life_days: float
    high_priority_share: float


class HistoricalQueryResponse(BaseModel):
    total_records: int
    filters_applied: Dict[str, Any]
    summary_cards: HistoricalSummaryCards
    top_products: List[HistoricalProductSummary]
    category_comparison: List[CategoryComparisonRow]


class RecommendationRequest(BaseModel):
    products: List[ProductFeatures] = Field(..., min_length=1, max_length=20)
    optimization_goal: Literal[
        "maximize_sales",
        "maximize_profit",
        "maximize_profit_density",
        "minimize_perishability_risk",
    ] = "maximize_profit"
    top_n: int = Field(5, ge=1, le=20)


class RecommendationItem(BaseModel):
    rank: int
    product_name: str
    category: str
    brand_tier: str
    optimization_goal: str
    predicted_stocking_priority: str
    priority_probability_high: float
    predicted_daily_units_sold: float
    expected_daily_revenue: float
    expected_daily_profit: float
    profit_per_shelf_unit: float
    estimated_unit_cost: float
    estimated_unit_margin: float
    shelf_capacity_utilization_pct: float
    operational_risk_score: float
    caution_flags: List[str]
    sales_band: str
    recommendation_score: float
    recommendation_reason: str


class RecommendationResponse(BaseModel):
    optimization_goal: str
    goal_description: str
    recommendations: List[RecommendationItem]


class ScenarioDefinition(BaseModel):
    scenario_name: str
    overrides: Dict[str, Any] = Field(default_factory=dict)


class ScenarioSimulationRequest(BaseModel):
    base_product: ProductFeatures
    scenarios: List[ScenarioDefinition] = Field(..., min_length=1, max_length=10)


class ScenarioBaselineResult(BaseModel):
    predicted_stocking_priority: str
    priority_probability_high: float
    predicted_daily_units_sold: float
    expected_daily_revenue: float
    expected_daily_profit: float
    profit_per_shelf_unit: float
    caution_flags: List[str]
    sales_band: str


class ScenarioComparisonResult(ScenarioBaselineResult):
    scenario_name: str
    applied_changes: Dict[str, Any]
    delta_units_vs_baseline: float
    delta_profit_vs_baseline: float


class ScenarioSimulationResponse(BaseModel):
    baseline: ScenarioBaselineResult
    scenarios: List[ScenarioComparisonResult]


class InsightsSummaryResponse(BaseModel):
    generated_at: str
    dataset_overview: Dict[str, Any]
    feature_engineering: Dict[str, Any]
    models_used: List[Dict[str, Any]]
    tuning_summary: Dict[str, Any]


class InsightsPerformanceResponse(BaseModel):
    generated_at: str
    classification: Dict[str, Any]
    regression: Dict[str, Any]
    experiment_groups: List[Dict[str, Any]]


class InsightsFeatureImportanceResponse(BaseModel):
    generated_at: str
    priority_model: Dict[str, Any]
    sales_model: Dict[str, Any]
    interpretability_notes: List[str]


class InsightsBusinessFindingsResponse(BaseModel):
    generated_at: str
    category_findings: Dict[str, Any]
    perishability_findings: Dict[str, Any]
    recommendation_factors: List[Dict[str, Any]]
    plain_language_takeaways: List[str]


class ModelLabModelCard(BaseModel):
    model_key: str
    model_name: str
    status: str
    compare_mode: str
    purpose: str
    inputs: str
    outputs: str
    strengths: str
    limitations: str
    deployment_relevance: str
    benchmark_source: Optional[str] = None


class ModelLabPerformanceRow(BaseModel):
    model_key: str
    model_name: str
    family: str
    representation: str
    status: str
    compare_mode: str
    benchmark_source: str
    accuracy: float
    precision_macro: Optional[float] = None
    recall_macro: Optional[float] = None
    macro_f1: Optional[float] = None
    weighted_f1: Optional[float] = None
    notes: Optional[str] = None


class ModelLabConfusionMatrix(BaseModel):
    labels: List[str]
    matrix: List[List[int]]


class ModelComparisonInsightResponse(BaseModel):
    generated_at: str
    source_notebooks: List[Dict[str, str]]
    models: List[ModelLabModelCard]
    performance_table: List[ModelLabPerformanceRow]
    weighted_f1_chart: List[Dict[str, Any]]
    accuracy_chart: List[Dict[str, Any]]
    confusion_matrices: Dict[str, ModelLabConfusionMatrix]
    selected_confusion_matrix_key: str
    deployment_choice: Dict[str, Any]
    compare_notes: List[str]


class ModelCompareResult(BaseModel):
    model_key: str
    model_name: str
    inference_status: str
    compare_mode: str
    prediction: Optional[str] = None
    top_confidence: Optional[float] = None
    probabilities: Optional[Dict[str, float]] = None
    benchmark_accuracy: Optional[float] = None
    benchmark_weighted_f1: Optional[float] = None
    benchmark_source: Optional[str] = None
    strengths: str
    limitations: str
    deployment_relevance: str


class ModelComparisonPredictionResponse(BaseModel):
    generated_at: str
    scenario_summary: Dict[str, Any]
    default_context_note: str
    defaulted_fields: List[str]
    deployment_choice: Dict[str, Any]
    compared_models: List[ModelCompareResult]
