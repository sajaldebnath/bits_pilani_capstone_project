const numericFields = new Set([
  "current_price",
  "competitor_price",
  "shelf_capacity",
  "lead_time_days",
  "marketing_spend",
  "discount_percentage",
  "shelf_life_days",
  "fill_rate_pct",
  "supplier_delay_days",
  "footfall_index",
  "app_traffic_index",
]);

const productFieldRows = [
  [
    { name: "category", label: "Category", type: "select", options: ["Beauty", "Clothing", "Electronics", "Grocery", "Home"] },
    { name: "product_name", label: "Product Name", type: "text" },
  ],
  [
    { name: "brand_tier", label: "Brand Tier", type: "select", options: ["Budget", "Mid", "Premium"] },
    { name: "promotion_type", label: "Promotion Type", type: "select", options: ["Unknown", "Festival", "Flash Sale", "BOGO", "Loyalty Only", "Seasonal Discount"] },
  ],
  [
    { name: "sub_category", label: "Sub Category", type: "text" },
    { name: "brand_name", label: "Brand Name", type: "text" },
  ],
  [
    { name: "store_type", label: "Store Type", type: "select", options: ["General", "Urban", "Rural"] },
    { name: "festival_name", label: "Festival Name", type: "text" },
  ],
  [
    { name: "current_price", label: "Current Price", type: "number", min: "0", step: "0.01" },
    { name: "competitor_price", label: "Competitor Price", type: "number", min: "0", step: "0.01" },
  ],
  [
    { name: "shelf_capacity", label: "Shelf Capacity", type: "number", min: "0", step: "1" },
    { name: "lead_time_days", label: "Lead Time Days", type: "number", min: "0", step: "1" },
  ],
  [
    { name: "marketing_spend", label: "Marketing Spend", type: "number", min: "0", step: "0.01" },
    { name: "discount_percentage", label: "Discount %", type: "number", min: "0", max: "100", step: "0.01" },
  ],
  [
    { name: "shelf_life_days", label: "Shelf Life Days", type: "number", min: "0", step: "1" },
    { name: "fill_rate_pct", label: "Fill Rate %", type: "number", min: "0", max: "100", step: "0.01" },
  ],
  [
    { name: "supplier_delay_days", label: "Supplier Delay Days", type: "number", min: "0", step: "1" },
    { name: "footfall_index", label: "Footfall Index", type: "number", min: "0", step: "0.1" },
  ],
];

const defaultProductContext = {
  category: "Electronics",
  product_name: "Demo Product",
  brand_tier: "Mid",
  promotion_type: "Unknown",
  sub_category: "General",
  brand_name: "Unknown",
  store_type: "General",
  festival_name: null,
  current_price: 10,
  competitor_price: 10,
  shelf_capacity: 20,
  lead_time_days: 3,
  marketing_spend: 500,
  discount_percentage: 0,
  shelf_life_days: 180,
  fill_rate_pct: 95,
  supplier_delay_days: 1,
  footfall_index: 90,
  app_traffic_index: 50,
};

const baseSamples = {
  priority_high: {
    category: "Electronics",
    product_name: "Samsung Computers 1018",
    brand_tier: "Budget",
    promotion_type: "Unknown",
    sub_category: "Computers",
    brand_name: "Samsung",
    store_type: "Rural",
    festival_name: "",
    current_price: 327.86,
    competitor_price: 348.26,
    shelf_capacity: 44,
    lead_time_days: 14,
    marketing_spend: 924,
    discount_percentage: 0.02,
    shelf_life_days: 1112,
    fill_rate_pct: 91.48,
    supplier_delay_days: 2,
    footfall_index: 55.7,
    app_traffic_index: 50,
  },
  priority_medium: {
    category: "Home",
    product_name: "Tupperware Bedding 1017",
    brand_tier: "Premium",
    promotion_type: "Loyalty Only",
    sub_category: "Bedding",
    brand_name: "Tupperware",
    store_type: "Rural",
    festival_name: "",
    current_price: 33.09,
    competitor_price: 45.11,
    shelf_capacity: 71,
    lead_time_days: 14,
    marketing_spend: 3689,
    discount_percentage: 0.3,
    shelf_life_days: 2810,
    fill_rate_pct: 87.65,
    supplier_delay_days: 3,
    footfall_index: 189.8,
    app_traffic_index: 50,
  },
  priority_low: {
    category: "Grocery",
    product_name: "Tata Spices 1016",
    brand_tier: "Premium",
    promotion_type: "Unknown",
    sub_category: "Spices",
    brand_name: "Tata",
    store_type: "Urban",
    festival_name: "",
    current_price: 240.94,
    competitor_price: 252.64,
    shelf_capacity: 95,
    lead_time_days: 14,
    marketing_spend: 706,
    discount_percentage: 0.14,
    shelf_life_days: 10,
    fill_rate_pct: 89.39,
    supplier_delay_days: 0,
    footfall_index: 185.5,
    app_traffic_index: 50,
  },
  electronics: {
    category: "Electronics",
    product_name: "Sony Headphones",
    brand_tier: "Premium",
    promotion_type: "Festival",
    sub_category: "Audio",
    brand_name: "Sony",
    store_type: "Urban",
    festival_name: "Diwali",
    current_price: 120,
    competitor_price: 128,
    shelf_capacity: 20,
    lead_time_days: 5,
    marketing_spend: 3000,
    discount_percentage: 10,
    shelf_life_days: 900,
    fill_rate_pct: 92,
    supplier_delay_days: 2,
    footfall_index: 130,
    app_traffic_index: 72,
  },
  grocery: {
    category: "Grocery",
    product_name: "Nestle Biscuits Pack",
    brand_tier: "Budget",
    promotion_type: "BOGO",
    sub_category: "Snacks",
    brand_name: "Nestle",
    store_type: "Urban",
    festival_name: "",
    current_price: 5,
    competitor_price: 4.8,
    shelf_capacity: 180,
    lead_time_days: 2,
    marketing_spend: 550,
    discount_percentage: 6,
    shelf_life_days: 15,
    fill_rate_pct: 85,
    supplier_delay_days: 3,
    footfall_index: 128,
    app_traffic_index: 58,
  },
  beauty: {
    category: "Beauty",
    product_name: "Lakme Lipstick",
    brand_tier: "Premium",
    promotion_type: "Flash Sale",
    sub_category: "Makeup",
    brand_name: "Lakme",
    store_type: "Urban",
    festival_name: "New Year",
    current_price: 25,
    competitor_price: 24,
    shelf_capacity: 50,
    lead_time_days: 3,
    marketing_spend: 2000,
    discount_percentage: 12,
    shelf_life_days: 365,
    fill_rate_pct: 95,
    supplier_delay_days: 1,
    footfall_index: 116,
    app_traffic_index: 66,
  },
  home: {
    category: "Home",
    product_name: "Storage Box Set",
    brand_tier: "Mid",
    promotion_type: "Seasonal Discount",
    sub_category: "Organization",
    brand_name: "HomeEase",
    store_type: "Urban",
    festival_name: "",
    current_price: 40,
    competitor_price: 42,
    shelf_capacity: 45,
    lead_time_days: 4,
    marketing_spend: 1200,
    discount_percentage: 8,
    shelf_life_days: 1800,
    fill_rate_pct: 96,
    supplier_delay_days: 2,
    footfall_index: 92,
    app_traffic_index: 48,
  },
};

const samples = {
  ...baseSamples,
  premium_electronics: {
    ...baseSamples.electronics,
    product_name: "Bose Noise-Canceling Headphones",
    brand_name: "Bose",
    current_price: 249,
    competitor_price: 259,
    shelf_capacity: 28,
    lead_time_days: 6,
    marketing_spend: 3600,
    discount_percentage: 8,
    fill_rate_pct: 95,
    supplier_delay_days: 1,
    footfall_index: 142,
    app_traffic_index: 82,
  },
  perishable_grocery: {
    ...baseSamples.grocery,
    product_name: "Fresh Greek Yogurt Cups",
    sub_category: "Dairy",
    brand_name: "FreshDairy",
    brand_tier: "Mid",
    current_price: 4.2,
    competitor_price: 3.9,
    shelf_capacity: 160,
    lead_time_days: 2,
    marketing_spend: 700,
    discount_percentage: 5,
    shelf_life_days: 7,
    fill_rate_pct: 82,
    supplier_delay_days: 3,
    footfall_index: 144,
    app_traffic_index: 54,
  },
  promo_beauty: {
    ...baseSamples.beauty,
    product_name: "Lakme Festival Lip Kit",
    current_price: 29,
    competitor_price: 27,
    shelf_capacity: 56,
    marketing_spend: 2600,
    discount_percentage: 15,
    footfall_index: 123,
    app_traffic_index: 74,
  },
  bulky_home: {
    ...baseSamples.home,
    product_name: "Modular Storage Tower",
    sub_category: "Storage",
    current_price: 58,
    competitor_price: 55,
    shelf_capacity: 18,
    lead_time_days: 8,
    marketing_spend: 650,
    shelf_life_days: 2200,
    fill_rate_pct: 94,
    supplier_delay_days: 3,
    footfall_index: 78,
    app_traffic_index: 41,
  },
  delayed_supply: {
    ...baseSamples.electronics,
    product_name: "Smart Kitchen Mixer",
    category: "Home",
    sub_category: "Appliances",
    brand_name: "KitchenPro",
    brand_tier: "Mid",
    promotion_type: "Unknown",
    current_price: 95,
    competitor_price: 92,
    shelf_capacity: 24,
    lead_time_days: 12,
    marketing_spend: 900,
    discount_percentage: 4,
    shelf_life_days: 720,
    fill_rate_pct: 84,
    supplier_delay_days: 7,
    footfall_index: 87,
    app_traffic_index: 46,
  },
};

const businessDemoScenarios = {
  premium_electronics: {
    payload: samples.premium_electronics,
    goal: "maximize_profit",
    compareKey: "promo",
  },
  perishable_grocery: {
    payload: samples.perishable_grocery,
    goal: "minimize_perishability_risk",
    compareKey: "shelfLife",
  },
  promo_beauty: {
    payload: samples.promo_beauty,
    goal: "maximize_sales",
    compareKey: "promo",
  },
  bulky_home: {
    payload: samples.bulky_home,
    goal: "maximize_profit_density",
    compareKey: "marketing",
  },
  delayed_supply: {
    payload: samples.delayed_supply,
    goal: "minimize_perishability_risk",
    compareKey: "supply",
  },
};

const portfolios = {
  core: [
    samples.electronics,
    samples.grocery,
    samples.beauty,
    samples.home,
    {
      category: "Clothing",
      product_name: "Premium Polo Shirt",
      brand_tier: "Mid",
      promotion_type: "Loyalty Only",
      sub_category: "Menswear",
      brand_name: "UrbanWeave",
      store_type: "Urban",
      festival_name: "",
      current_price: 34,
      competitor_price: 36,
      shelf_capacity: 70,
      lead_time_days: 4,
      marketing_spend: 900,
      discount_percentage: 5,
      shelf_life_days: 1200,
      fill_rate_pct: 94,
      supplier_delay_days: 2,
      footfall_index: 88,
      app_traffic_index: 43,
    },
  ],
  risk: [
    samples.grocery,
    {
      category: "Grocery",
      product_name: "Fresh Juice Bottle",
      brand_tier: "Mid",
      promotion_type: "Flash Sale",
      sub_category: "Beverages",
      brand_name: "FreshSip",
      store_type: "Urban",
      festival_name: "",
      current_price: 3.8,
      competitor_price: 3.6,
      shelf_capacity: 120,
      lead_time_days: 3,
      marketing_spend: 300,
      discount_percentage: 15,
      shelf_life_days: 5,
      fill_rate_pct: 78,
      supplier_delay_days: 5,
      footfall_index: 135,
      app_traffic_index: 44,
    },
    samples.electronics,
    samples.home,
  ],
};

const technicalScenarioSets = {
  promo: [
    { scenario_name: "No Promotion", overrides: { promotion_type: "Unknown", marketing_spend: 800, shelf_life_days: 365, fill_rate_pct: 95 } },
    { scenario_name: "Flash Sale", overrides: { promotion_type: "Flash Sale", marketing_spend: 1800, shelf_life_days: 365, fill_rate_pct: 95 } },
    { scenario_name: "Festival Push", overrides: { promotion_type: "Festival", marketing_spend: 3200, shelf_life_days: 365, fill_rate_pct: 95, festival_name: "Diwali" } },
  ],
  marketing: [
    { scenario_name: "Lean Spend", overrides: { promotion_type: "Unknown", marketing_spend: 400, shelf_life_days: 365, fill_rate_pct: 95 } },
    { scenario_name: "Balanced Spend", overrides: { promotion_type: "Flash Sale", marketing_spend: 1500, shelf_life_days: 365, fill_rate_pct: 95 } },
    { scenario_name: "Heavy Spend", overrides: { promotion_type: "Festival", marketing_spend: 3000, shelf_life_days: 365, fill_rate_pct: 95 } },
  ],
  shelfLife: [
    { scenario_name: "Long Shelf Life", overrides: { promotion_type: "Unknown", marketing_spend: 1200, shelf_life_days: 365, fill_rate_pct: 95 } },
    { scenario_name: "Tighter Shelf Life", overrides: { promotion_type: "Unknown", marketing_spend: 1200, shelf_life_days: 45, fill_rate_pct: 92 } },
    { scenario_name: "Perishable Risk", overrides: { promotion_type: "Flash Sale", marketing_spend: 1200, shelf_life_days: 10, fill_rate_pct: 84 } },
  ],
};

const businessScenarioSets = {
  promo: technicalScenarioSets.promo,
  marketing: technicalScenarioSets.marketing,
  shelfLife: technicalScenarioSets.shelfLife,
  supply: [
    {
      scenario_name: "Stable Supply",
      overrides: {
        promotion_type: "Unknown",
        marketing_spend: 900,
        lead_time_days: 4,
        supplier_delay_days: 1,
        fill_rate_pct: 97,
      },
    },
    {
      scenario_name: "Delayed Supply",
      overrides: {
        promotion_type: "Unknown",
        marketing_spend: 900,
        lead_time_days: 9,
        supplier_delay_days: 5,
        fill_rate_pct: 88,
      },
    },
    {
      scenario_name: "Delayed Supply + Promo",
      overrides: {
        promotion_type: "Flash Sale",
        marketing_spend: 1600,
        lead_time_days: 12,
        supplier_delay_days: 7,
        fill_rate_pct: 82,
      },
    },
  ],
};

let insightsCache = null;
let modelLabCache = null;
const businessState = {
  activeScenario: "premium_electronics",
  activeCompareSet: "promo",
  raw: {},
};

const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2,
});

function escapeHtml(value) {
  const span = document.createElement("span");
  span.textContent = String(value ?? "");
  return span.innerHTML;
}

function formatNumber(value, digits = 2) {
  const numericValue = Number(value);
  if (Number.isNaN(numericValue)) return "n/a";
  return numericValue.toLocaleString("en-US", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

function formatCompactNumber(value, digits = 1) {
  const numericValue = Number(value);
  if (Number.isNaN(numericValue)) return "n/a";
  return numericValue.toLocaleString("en-US", {
    minimumFractionDigits: 0,
    maximumFractionDigits: digits,
  });
}

function formatCurrency(value) {
  const numericValue = Number(value);
  if (Number.isNaN(numericValue)) return "n/a";
  return currencyFormatter.format(numericValue);
}

function formatPercent(value, digits = 1) {
  const numericValue = Number(value);
  if (Number.isNaN(numericValue)) return "n/a";
  return `${numericValue.toFixed(digits)}%`;
}

function titleCaseGoal(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function dedupeFlags(flags) {
  return [...new Set((flags || []).filter(Boolean))];
}

function renderProductForms() {
  document.querySelectorAll(".product-form").forEach((form) => {
    form.innerHTML = productFieldRows.map((row) => `
      <div class="row row-2">
        ${row.map((field) => `
          <div>
            <label for="${form.id}-${field.name}">${field.label}</label>
            ${field.type === "select"
              ? `<select id="${form.id}-${field.name}" name="${field.name}">
                  ${field.options.map((option) => `<option value="${escapeHtml(option)}">${escapeHtml(option)}</option>`).join("")}
                </select>`
              : `<input id="${form.id}-${field.name}" name="${field.name}" type="${field.type}" min="${field.min ?? ""}" max="${field.max ?? ""}" step="${field.step ?? ""}" />`
            }
          </div>
        `).join("")}
      </div>
    `).join("");
  });
}

function setFormValues(formId, values) {
  const form = document.getElementById(formId);
  if (!form) return;
  Object.entries(values).forEach(([key, value]) => {
    const field = form.elements.namedItem(key);
    if (!field) return;
    field.value = value ?? "";
  });
}

function formPayload(formId) {
  const form = document.getElementById(formId);
  const payload = {};
  Array.from(form.elements).forEach((field) => {
    if (!field.name) return;
    let value = field.value;
    if (numericFields.has(field.name)) {
      value = value === "" ? 0 : Number(value);
    }
    if (field.name === "festival_name" && value === "") {
      value = null;
    }
    payload[field.name] = value;
  });
  return payload;
}

function normalizeProductPayload(payload) {
  const merged = {
    ...defaultProductContext,
    ...payload,
  };
  ["category", "product_name", "brand_tier", "promotion_type", "sub_category", "brand_name", "store_type"].forEach((field) => {
    if (!merged[field]) {
      merged[field] = defaultProductContext[field];
    }
  });
  merged.festival_name = merged.festival_name || null;
  merged.current_price = Number(merged.current_price ?? defaultProductContext.current_price);
  merged.competitor_price = Number(merged.competitor_price ?? defaultProductContext.competitor_price);
  merged.shelf_capacity = Number(merged.shelf_capacity ?? defaultProductContext.shelf_capacity);
  merged.lead_time_days = Number(merged.lead_time_days ?? defaultProductContext.lead_time_days);
  merged.marketing_spend = Number(merged.marketing_spend ?? defaultProductContext.marketing_spend);
  merged.discount_percentage = Number(merged.discount_percentage ?? defaultProductContext.discount_percentage);
  merged.shelf_life_days = Number(merged.shelf_life_days ?? defaultProductContext.shelf_life_days);
  merged.fill_rate_pct = Number(merged.fill_rate_pct ?? defaultProductContext.fill_rate_pct);
  merged.supplier_delay_days = Number(merged.supplier_delay_days ?? defaultProductContext.supplier_delay_days);
  merged.footfall_index = Number(merged.footfall_index ?? defaultProductContext.footfall_index);
  merged.app_traffic_index = Number(merged.app_traffic_index ?? defaultProductContext.app_traffic_index);
  return merged;
}

function businessPayload() {
  return normalizeProductPayload(formPayload("business-demo-form"));
}

function priorityPillClass(value) {
  const text = String(value).toLowerCase();
  if (text.includes("high") || text.includes("strong")) return "good";
  if (text.includes("medium") || text.includes("steady") || text.includes("balanced")) return "warn";
  return "risk";
}

function flagsMarkup(flags) {
  if (!flags || !flags.length) {
    return `<div class="pill neutral">No caution flags triggered</div>`;
  }
  return `<ul class="flag-list">${flags.map((flag) => `<li>${escapeHtml(flag)}</li>`).join("")}</ul>`;
}

function flagCardsMarkup(flags) {
  if (!flags || !flags.length) {
    return `
      <div class="warning-card neutral-card">
        <strong>No active caution flags</strong>
        <span>The current scenario did not trigger additional supply or perishability warnings.</span>
      </div>
    `;
  }
  return `
    <div class="warning-grid">
      ${flags.map((flag) => `
        <div class="warning-card">
          <strong>Risk Flag</strong>
          <span>${escapeHtml(flag)}</span>
        </div>
      `).join("")}
    </div>
  `;
}

function probabilityBars(probabilities) {
  return Object.entries(probabilities || {})
    .sort((a, b) => b[1] - a[1])
    .map(([label, value]) => `
      <div class="bar-group">
        <div class="bar-label">
          <span>${escapeHtml(label)}</span>
          <strong>${formatPercent(value * 100, 1)}</strong>
        </div>
        <div class="bar-track">
          <div class="bar-fill" style="width:${Math.max(value * 100, 2)}%"></div>
        </div>
      </div>
    `).join("");
}

function renderPriorityResult(result) {
  const probabilities = result.probabilities || {};
  const confidence = Math.max(...Object.values(probabilities), 0) * 100;
  const narrative = result.predicted_stocking_priority === "High"
    ? "This item is a strong stocking candidate, but still needs a quick risk check."
    : result.predicted_stocking_priority === "Medium"
      ? "This item is viable, but it should compete for space based on the current business context."
      : "This item should be stocked selectively or only with clear supporting business reasons.";

  return `
    <div class="result-card">
      <div class="rank-topline">
        <div>
          <h3>Priority Decision</h3>
          <p class="result-copy">${escapeHtml(narrative)}</p>
        </div>
        <div class="pill ${priorityPillClass(result.predicted_stocking_priority)}">${escapeHtml(result.predicted_stocking_priority)}</div>
      </div>
    </div>
    <div class="summary-grid">
      <div class="summary-card">
        <span class="metric-value">${formatPercent(confidence, 1)}</span>
        <span class="metric-subtle">Highest class confidence</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${escapeHtml(result.model_name)}</span>
        <span class="metric-subtle">Active priority model</span>
      </div>
    </div>
    <div class="result-card">
      <h3>Class Confidence</h3>
      ${probabilityBars(probabilities)}
    </div>
    <div class="result-card">
      <h3>Caution Flags</h3>
      ${flagsMarkup(result.caution_flags)}
    </div>
  `;
}

function renderSalesResult(result) {
  const info = result.supporting_information || {};
  return `
    <div class="summary-grid">
      <div class="summary-card">
        <span class="metric-value">${formatCompactNumber(result.predicted_daily_units_sold)}</span>
        <span class="metric-subtle">Predicted units per day</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${formatCurrency(result.predicted_daily_revenue)}</span>
        <span class="metric-subtle">Expected daily revenue</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${formatCurrency(result.predicted_daily_profit)}</span>
        <span class="metric-subtle">Expected daily profit</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${formatPercent(info.shelf_capacity_utilization_pct ?? 0, 1)}</span>
        <span class="metric-subtle">Shelf capacity utilization</span>
      </div>
    </div>
    <div class="result-card">
      <div class="rank-topline">
        <div>
          <h3>Sales Outlook</h3>
          <p class="result-copy">Demand band: <strong>${escapeHtml(result.sales_band)}</strong></p>
        </div>
        <div class="pill ${priorityPillClass(result.sales_band)}">${escapeHtml(result.sales_band)}</div>
      </div>
      <div class="summary-grid">
        <div class="summary-card">
          <span class="metric-value">${formatCompactNumber(info.category_average_daily_units ?? 0)}</span>
          <span class="metric-subtle">Reference average units</span>
        </div>
        <div class="summary-card">
          <span class="metric-value">${formatPercent(info.comparison_to_reference_pct ?? 0, 1)}</span>
          <span class="metric-subtle">Vs reference group</span>
        </div>
        <div class="summary-card">
          <span class="metric-value">${formatCurrency(info.profit_per_shelf_unit ?? 0)}</span>
          <span class="metric-subtle">Profit per shelf unit</span>
        </div>
        <div class="summary-card">
          <span class="metric-value">${escapeHtml(info.reference_group ?? "n/a")}</span>
          <span class="metric-subtle">Benchmark slice</span>
        </div>
      </div>
    </div>
    <div class="result-card">
      <h3>Caution Flags</h3>
      ${flagsMarkup(result.caution_flags)}
    </div>
  `;
}

function recommendationCards(payload) {
  const recommendations = payload.recommendations || [];
  if (!recommendations.length) {
    return `<div class="empty-state">No recommendations were returned for this portfolio.</div>`;
  }

  return `
    <div class="notice">
      <strong>${escapeHtml(payload.optimization_goal.replaceAll("_", " "))}</strong><br />
      ${escapeHtml(payload.goal_description)}
    </div>
    ${recommendations.map((item) => `
      <div class="rank-card">
        <div class="rank-topline">
          <div>
            <div class="rank-number">${item.rank}</div>
          </div>
          <div style="flex:1;">
            <h3>${escapeHtml(item.product_name)}</h3>
            <div class="rank-meta">
              <span>${escapeHtml(item.category)}</span>
              <span>${escapeHtml(item.brand_tier)}</span>
              <span>${escapeHtml(item.predicted_stocking_priority)}</span>
            </div>
          </div>
          <div class="pill ${priorityPillClass(item.predicted_stocking_priority)}">Score ${formatNumber(item.recommendation_score, 1)}</div>
        </div>
        <div class="summary-grid">
          <div class="summary-card">
            <span class="metric-value">${formatCompactNumber(item.predicted_daily_units_sold)}</span>
            <span class="metric-subtle">Predicted units/day</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${formatCurrency(item.expected_daily_profit)}</span>
            <span class="metric-subtle">Expected daily profit</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${formatCurrency(item.profit_per_shelf_unit)}</span>
            <span class="metric-subtle">Profit per shelf unit</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${formatNumber(item.operational_risk_score, 1)}</span>
            <span class="metric-subtle">Operational risk score</span>
          </div>
        </div>
        <div class="bar-group">
          <div class="bar-label"><span>Recommendation score</span><strong>${formatNumber(item.recommendation_score, 1)}</strong></div>
          <div class="bar-track"><div class="bar-fill" style="width:${Math.max(item.recommendation_score, 4)}%"></div></div>
        </div>
        <div class="notice">${escapeHtml(item.recommendation_reason)}</div>
        <div class="result-card">
          <h4>Caution Flags</h4>
          ${flagsMarkup(item.caution_flags)}
        </div>
      </div>
    `).join("")}
  `;
}

function historicalMarkup(payload) {
  const topProducts = payload.top_products || [];
  const categories = payload.category_comparison || [];
  return `
    <div class="summary-grid">
      <div class="summary-card">
        <span class="metric-value">${payload.total_records}</span>
        <span class="metric-subtle">Matched records</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${formatCompactNumber(payload.summary_cards.avg_daily_units_sold)}</span>
        <span class="metric-subtle">Average units sold</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${formatCurrency(payload.summary_cards.avg_gross_profit)}</span>
        <span class="metric-subtle">Average gross profit</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${formatCurrency(payload.summary_cards.avg_profit_density)}</span>
        <span class="metric-subtle">Average profit density</span>
      </div>
    </div>
    <div class="result-card">
      <h3>Top Products</h3>
      <div class="candidate-table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Product</th>
              <th>Category</th>
              <th>Units</th>
              <th>Gross Profit</th>
              <th>Profit Density</th>
              <th>High Priority %</th>
            </tr>
          </thead>
          <tbody>
            ${topProducts.map((row) => `
              <tr>
                <td>${row.rank}</td>
                <td>${escapeHtml(row.product_name)}</td>
                <td>${escapeHtml(row.category)}</td>
                <td>${formatCompactNumber(row.avg_daily_units_sold)}</td>
                <td>${formatCurrency(row.avg_gross_profit)}</td>
                <td>${formatCurrency(row.avg_profit_density)}</td>
                <td>${formatPercent(row.high_priority_share, 1)}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    </div>
    <div class="result-card">
      <h3>Category Comparison</h3>
      ${categories.map((row) => `
        <div class="bar-group">
          <div class="bar-label">
            <span>${escapeHtml(row.category)} • ${row.records} records</span>
            <strong>${formatCurrency(row.avg_profit_density)}</strong>
          </div>
          <div class="bar-track">
            <div class="bar-fill" style="width:${Math.min(Number(row.avg_profit_density) * 10, 100)}%"></div>
          </div>
        </div>
      `).join("")}
    </div>
  `;
}

function scenarioMarkup(payload) {
  const scenarios = payload.scenarios || [];
  return `
    <div class="summary-grid">
      <div class="summary-card">
        <span class="metric-value">${formatCompactNumber(payload.baseline.predicted_daily_units_sold)}</span>
        <span class="metric-subtle">Baseline units/day</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${formatCurrency(payload.baseline.expected_daily_profit)}</span>
        <span class="metric-subtle">Baseline daily profit</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${formatCurrency(payload.baseline.profit_per_shelf_unit)}</span>
        <span class="metric-subtle">Baseline profit density</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${formatPercent(payload.baseline.priority_probability_high, 1)}</span>
        <span class="metric-subtle">Baseline High-priority confidence</span>
      </div>
    </div>
    <div class="result-card">
      <h3>Baseline Caution Flags</h3>
      ${flagsMarkup(payload.baseline.caution_flags)}
    </div>
    ${scenarios.map((scenario) => `
      <div class="rank-card">
        <div class="rank-topline">
          <div>
            <h3>${escapeHtml(scenario.scenario_name)}</h3>
            <div class="rank-meta">
              <span>${escapeHtml(scenario.predicted_stocking_priority)}</span>
              <span>${escapeHtml(scenario.sales_band)}</span>
            </div>
          </div>
          <div class="pill ${priorityPillClass(scenario.predicted_stocking_priority)}">${formatPercent(scenario.priority_probability_high, 1)} High</div>
        </div>
        <div class="summary-grid">
          <div class="summary-card">
            <span class="metric-value">${formatCompactNumber(scenario.predicted_daily_units_sold)}</span>
            <span class="metric-subtle">Units/day</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${formatCurrency(scenario.expected_daily_profit)}</span>
            <span class="metric-subtle">Daily profit</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${formatCompactNumber(scenario.delta_units_vs_baseline)}</span>
            <span class="metric-subtle">Delta vs baseline units</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${formatCurrency(scenario.delta_profit_vs_baseline)}</span>
            <span class="metric-subtle">Delta vs baseline profit</span>
          </div>
        </div>
        <div class="notice">
          Applied changes:
          ${Object.entries(scenario.applied_changes || {}).map(([key, value]) => `${escapeHtml(key)}=${escapeHtml(value)}`).join(", ")}
        </div>
        <div class="result-card">
          <h4>Caution Flags</h4>
          ${flagsMarkup(scenario.caution_flags)}
        </div>
      </div>
    `).join("")}
  `;
}

function getJSONMetricValue(value) {
  if (value === null || value === undefined) return "n/a";
  if (typeof value === "number") return formatCompactNumber(value, 4);
  return escapeHtml(value);
}

function renderBarRows(items, labelKey, valueKey, suffix = "", metricLabel = "") {
  if (!items || !items.length) {
    return `<div class="empty-state">No chart data available.</div>`;
  }
  const maxValue = Math.max(...items.map((item) => Math.abs(Number(item[valueKey] ?? 0))), 1);
  return items.map((item) => {
    const value = Number(item[valueKey] ?? 0);
    return `
      <div class="bar-group">
        <div class="bar-label">
          <span>${escapeHtml(item[labelKey])}</span>
          <strong>${formatCompactNumber(value, 4)}${escapeHtml(suffix)}${metricLabel ? ` ${escapeHtml(metricLabel)}` : ""}</strong>
        </div>
        <div class="bar-track">
          <div class="bar-fill" style="width:${Math.max((Math.abs(value) / maxValue) * 100, 2)}%"></div>
        </div>
      </div>
    `;
  }).join("");
}

function renderModelCards(models) {
  return `
    <div class="insight-grid">
      ${models.map((model) => `
        <div class="insight-card">
          <div class="pill ${model.status.toLowerCase().includes("deployed") ? "good" : model.status.toLowerCase().includes("benchmark") ? "warn" : "neutral"}">${escapeHtml(model.status)}</div>
          <h4 style="margin-top:10px;">${escapeHtml(model.model_name)}</h4>
          <p class="insight-muted">${escapeHtml(model.purpose)}</p>
          <div class="divider-title">Inputs</div>
          <p>${escapeHtml(model.inputs)}</p>
          <div class="divider-title">Outputs</div>
          <p>${escapeHtml(model.outputs)}</p>
          <div class="divider-title">Strengths</div>
          <p>${escapeHtml(model.strengths)}</p>
          <div class="divider-title">Limitations</div>
          <p>${escapeHtml(model.limitations)}</p>
        </div>
      `).join("")}
    </div>
  `;
}

function renderCompactTable(columns, rows) {
  if (!rows || !rows.length) {
    return `<div class="empty-state">No table rows available.</div>`;
  }
  return `
    <div class="candidate-table-wrap">
      <table class="compact-table">
        <thead>
          <tr>
            ${columns.map((column) => `<th>${escapeHtml(column.label)}</th>`).join("")}
          </tr>
        </thead>
        <tbody>
          ${rows.map((row) => `
            <tr>
              ${columns.map((column) => `<td>${getJSONMetricValue(row[column.key])}</td>`).join("")}
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function renderConfusionMatrix(confusionMatrix) {
  const labels = confusionMatrix.labels || [];
  const matrix = confusionMatrix.matrix || [];
  return `
    <table class="matrix-table">
      <thead>
        <tr>
          <th>Actual \\ Predicted</th>
          ${labels.map((label) => `<th>${escapeHtml(label)}</th>`).join("")}
        </tr>
      </thead>
      <tbody>
        ${matrix.map((row, index) => `
          <tr>
            <th>${escapeHtml(labels[index] || `Row ${index + 1}`)}</th>
            ${row.map((value) => `<td>${escapeHtml(value)}</td>`).join("")}
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
}

function featureListMarkup(rows) {
  return `
    <div class="insight-grid">
      ${rows.map((row) => `
        <div class="insight-card">
          <h4>${escapeHtml(row.feature)}</h4>
          <div class="pill ${Number(row.coefficient) >= 0 ? "good" : "risk"}">Coefficient ${escapeHtml(row.coefficient)}</div>
          ${row.interpretation ? `<p class="insight-muted" style="margin-top:10px;">${escapeHtml(row.interpretation)}</p>` : ""}
        </div>
      `).join("")}
    </div>
  `;
}

function tokenTagMarkup(rows) {
  return `
    <div class="tag-cloud">
      ${rows.map((row) => `<span class="tag">${escapeHtml(row.feature)} (${escapeHtml(row.coefficient)})</span>`).join("")}
    </div>
  `;
}

function experimentSectionMarkup(summary, performance) {
  const selectedKey = document.getElementById("insights-experiment-group")?.value || "classification";
  const selectedGroup = (performance.experiment_groups || []).find((group) => group.group_key === selectedKey) || performance.experiment_groups?.[0];
  const tuning = summary.tuning_summary || {};
  const classification = tuning.classification || {};
  const regression = tuning.regression || {};
  return `
    <div class="insight-grid">
      <div class="insight-card">
        <div class="divider-title">Classification Tuning</div>
        <span class="insight-metric">${escapeHtml(classification.best_weighted_f1 ?? "n/a")}</span>
        <p class="insight-muted">${escapeHtml(classification.note || "")}</p>
      </div>
      <div class="insight-card">
        <div class="divider-title">Regression Tuning</div>
        <span class="insight-metric">${escapeHtml(regression.best_rmse ?? "n/a")}</span>
        <p class="insight-muted">${escapeHtml(regression.note || "")}</p>
      </div>
      <div class="insight-card">
        <div class="divider-title">Formal Status</div>
        <p>${escapeHtml(tuning.formal_tuning_status || "")}</p>
      </div>
    </div>
    <div class="result-card">
      <h3>${escapeHtml(selectedGroup?.title || "Experiments")}</h3>
      <p class="result-copy">${escapeHtml(selectedGroup?.description || "")}</p>
      ${selectedGroup?.group_key === "classification"
        ? renderCompactTable(
            [
              { key: "model_name", label: "Model" },
              { key: "variant", label: "Variant" },
              { key: "accuracy", label: "Accuracy" },
              { key: "f1_macro", label: "Macro F1" },
              { key: "weighted_f1", label: "Weighted F1" },
            ],
            selectedGroup.rows || [],
          )
        : renderCompactTable(
            [
              { key: "model_name", label: "Model" },
              { key: "variant", label: "Variant" },
              { key: "mae", label: "MAE" },
              { key: "rmse", label: "RMSE" },
              { key: "r2", label: "R^2" },
            ],
            selectedGroup.rows || [],
          )}
    </div>
  `;
}

function renderInsightsMarkup(cache) {
  const { summary, performance, featureImportance, businessFindings } = cache;
  const dataset = summary.dataset_overview || {};
  const featureEngineering = summary.feature_engineering || {};
  const classification = performance.classification || {};
  const regression = performance.regression || {};
  const priorityModel = featureImportance.priority_model || {};
  const salesModel = featureImportance.sales_model || {};
  const categoryFindings = businessFindings.category_findings || {};
  const perishability = businessFindings.perishability_findings || {};

  return `
    <section class="insight-section">
      <div class="insight-section-header">
        <h3>A. Dataset Overview</h3>
        <p>The project uses a structured retail dataset with both commercial and operational signals, and supports one classification target plus one regression target.</p>
      </div>
      <div class="summary-grid">
        ${(dataset.summary_cards || []).map((card) => `
          <div class="summary-card">
            <span class="metric-value">${escapeHtml(card.value)}</span>
            <span class="metric-subtle">${escapeHtml(card.label)}</span>
            <div class="small-copy" style="margin-top:6px;">${escapeHtml(card.note || "")}</div>
          </div>
        `).join("")}
      </div>
      <div class="insight-columns">
        <div class="result-card">
          <h3>Class Distribution</h3>
          ${renderBarRows(dataset.class_distribution || [], "label", "count", "", "records")}
        </div>
        <div class="result-card">
          <h3>Feature Groups</h3>
          <div class="insight-grid">
            ${(dataset.feature_groups || []).map((group) => `
              <div class="insight-card">
                <div class="pill neutral">${escapeHtml(group.count)} fields</div>
                <h4 style="margin-top:10px;">${escapeHtml(group.name)}</h4>
                <p class="insight-muted">${escapeHtml(group.description)}</p>
              </div>
            `).join("")}
          </div>
        </div>
      </div>
    </section>

    <section class="insight-section">
      <div class="insight-section-header">
        <h3>B. Feature Engineering</h3>
        <p>The deployed models rely on a shared text template plus structured numeric signals, while engineered profit features are used for target design and analysis rather than as live classification inputs.</p>
      </div>
      <div class="result-card">
        <h3>Text Template Design</h3>
        <div class="code-block">${escapeHtml(featureEngineering.text_template_design?.template || "")}</div>
        <p class="result-copy" style="margin-top:12px;">${escapeHtml(featureEngineering.text_template_design?.why_it_exists || "")}</p>
      </div>
      <div class="result-card">
        <h3>Numeric Features Used</h3>
        <div class="tag-cloud">
          ${(featureEngineering.numeric_features_used || []).map((feature) => `<span class="tag">${escapeHtml(feature)}</span>`).join("")}
        </div>
      </div>
      <div class="insight-columns">
        <div class="result-card">
          <h3>Engineered Features Created</h3>
          <div class="insight-grid">
            ${(featureEngineering.engineered_features_created || []).map((feature) => `
              <div class="insight-card">
                <h4>${escapeHtml(feature.name)}</h4>
                <div class="code-block">${escapeHtml(feature.formula)}</div>
                <p class="insight-muted" style="margin-top:10px;">${escapeHtml(feature.purpose)}</p>
              </div>
            `).join("")}
          </div>
        </div>
        <div class="result-card">
          <h3>Leakage Checks</h3>
          <ul class="insight-list">
            ${(featureEngineering.leakage_checks || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
          </ul>
          <div class="divider-title" style="margin-top:16px;">Excluded or protected columns</div>
          <div class="tag-cloud" style="margin-top:10px;">
            ${(featureEngineering.excluded_features || []).map((item) => `<span class="tag">${escapeHtml(item)}</span>`).join("")}
          </div>
        </div>
      </div>
    </section>

    <section class="insight-section">
      <div class="insight-section-header">
        <h3>C. Models Used</h3>
        <p>The runtime app deploys two stable classical ML models, while the insights view also documents the baseline and research-model options considered for academic discussion.</p>
      </div>
      ${renderModelCards(summary.models_used || [])}
    </section>

    <section class="insight-section">
      <div class="insight-section-header">
        <h3>D. Performance Comparison</h3>
        <p>These metrics come from precomputed offline experiment runs. The UI only reads the saved results and does not retrain models live.</p>
      </div>
      <div class="insight-columns">
        <div class="result-card">
          <h3>Classification Metrics</h3>
          ${renderCompactTable(
            [
              { key: "model_name", label: "Model" },
              { key: "variant", label: "Variant" },
              { key: "accuracy", label: "Accuracy" },
              { key: "precision_macro", label: "Macro Precision" },
              { key: "recall_macro", label: "Macro Recall" },
              { key: "weighted_f1", label: "Weighted F1" },
            ],
            classification.comparison_table || [],
          )}
          <div class="divider-title" style="margin-top:16px;">Weighted F1 comparison</div>
          ${renderBarRows(classification.comparison_chart || [], "label", "value")}
        </div>
        <div class="result-card">
          <h3>Regression Metrics</h3>
          ${renderCompactTable(
            [
              { key: "model_name", label: "Model" },
              { key: "variant", label: "Variant" },
              { key: "mae", label: "MAE" },
              { key: "rmse", label: "RMSE" },
              { key: "r2", label: "R^2" },
            ],
            regression.comparison_table || [],
          )}
          <div class="divider-title" style="margin-top:16px;">R^2 comparison</div>
          ${renderBarRows(regression.comparison_chart || [], "label", "value")}
        </div>
      </div>
      <div class="result-card">
        <h3>Confusion Matrix for Best Classification Model</h3>
        ${renderConfusionMatrix(classification.confusion_matrix || { labels: [], matrix: [] })}
      </div>
    </section>

    <section class="insight-section">
      <div class="insight-section-header">
        <h3>E. Feature Importance / Interpretability</h3>
        <p>The deployed models are linear, which makes coefficient-based interpretation a practical way to explain what is pushing predictions up or down.</p>
      </div>
      <div class="insight-columns">
        <div class="result-card">
          <h3>Priority Model Drivers for High Priority</h3>
          ${featureListMarkup(priorityModel.top_numeric_drivers_for_high_priority || [])}
          <div class="divider-title" style="margin-top:16px;">Top semantic cues</div>
          ${tokenTagMarkup(priorityModel.top_text_tokens_for_high_priority || [])}
        </div>
        <div class="result-card">
          <h3>Priority Model Drivers for Low Priority</h3>
          ${featureListMarkup(priorityModel.top_numeric_drivers_for_low_priority || [])}
        </div>
      </div>
      <div class="result-card">
        <h3>Sales Model Drivers</h3>
        ${featureListMarkup(salesModel.top_numeric_drivers_for_sales || [])}
        <div class="divider-title" style="margin-top:16px;">Top sales-related text cues</div>
        ${tokenTagMarkup(salesModel.top_text_tokens_for_sales || [])}
        <ul class="insight-list" style="margin-top:16px;">
          ${(featureImportance.interpretability_notes || []).map((note) => `<li>${escapeHtml(note)}</li>`).join("")}
        </ul>
      </div>
    </section>

    <section class="insight-section">
      <div class="insight-section-header">
        <h3>F. Business Findings</h3>
        <p>This section translates the modeling work into plain-language business takeaways that an academic coordinator can quickly understand.</p>
      </div>
      <div class="insight-columns">
        <div class="result-card">
          <h3>Categories Most Often High Priority</h3>
          ${renderBarRows(categoryFindings.top_high_priority_categories || [], "category", "high_priority_share", "%")}
        </div>
        <div class="result-card">
          <h3>Perishability and Risk Signals</h3>
          <div class="summary-grid">
            <div class="summary-card">
              <span class="metric-value">${escapeHtml(perishability.short_shelf_life_records_pct ?? "n/a")}%</span>
              <span class="metric-subtle">Short shelf-life records</span>
            </div>
            <div class="summary-card">
              <span class="metric-value">${escapeHtml(perishability.low_fill_rate_records_pct ?? "n/a")}%</span>
              <span class="metric-subtle">Low fill-rate records</span>
            </div>
            <div class="summary-card">
              <span class="metric-value">${escapeHtml(perishability.any_risk_flag_records_pct ?? "n/a")}%</span>
              <span class="metric-subtle">Any risk condition</span>
            </div>
            <div class="summary-card">
              <span class="metric-value">${escapeHtml(perishability.short_life_high_priority_share ?? "n/a")}%</span>
              <span class="metric-subtle">High priority among short-life items</span>
            </div>
          </div>
        </div>
      </div>
      <div class="result-card">
        <h3>Top Recommendation Factors</h3>
        <div class="insight-grid">
          ${(businessFindings.recommendation_factors || []).map((factor) => `
            <div class="insight-card">
              <h4>${escapeHtml(factor.factor)}</h4>
              <div class="pill warn">${escapeHtml(factor.role)}</div>
              <p class="insight-muted" style="margin-top:10px;">${escapeHtml(factor.business_interpretation)}</p>
            </div>
          `).join("")}
        </div>
      </div>
      <div class="result-card">
        <h3>Plain-Language Takeaways</h3>
        <ul class="insight-list">
          ${(businessFindings.plain_language_takeaways || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
      </div>
    </section>

    <section class="insight-section">
      <div class="insight-section-header">
        <h3>G. Tuning / Experiment Summary</h3>
        <p>Only precomputed experiment sweeps are shown here. That gives the coordinator a controlled comparison without exposing unstable live retraining controls.</p>
      </div>
      ${experimentSectionMarkup(summary, performance)}
    </section>
  `;
}

function summarizeSalesOutlook(sales) {
  const pct = Number(sales.supporting_information?.comparison_to_reference_pct ?? 0);
  if (pct >= 10) return "Demand is running above the reference slice, so the item has room to justify shelf space.";
  if (pct >= 0) return "Demand is in line with the reference slice, so the item looks stable rather than explosive.";
  return "Demand is currently below the reference slice, so the item needs stronger justification before expanding shelf space.";
}

function summarizeProfitDensity(recommendation) {
  const profitDensity = Number(recommendation?.profit_per_shelf_unit ?? 0);
  if (profitDensity >= 8) return "Profit density is strong, which means the item uses shelf space efficiently.";
  if (profitDensity >= 3) return "Profit density is acceptable, but shelf-space trade-offs still matter.";
  return "Profit density is modest, so the item may struggle if shelf space is tight.";
}

function summarizePerishability(payload) {
  if (Number(payload.shelf_life_days) <= 14) return "Shelf life is short, so the product needs quick sell-through or cautious stocking.";
  if (Number(payload.shelf_life_days) <= 60) return "Shelf life is moderate, which keeps perishability in view but not at crisis level.";
  return "Shelf life is comfortable, so perishability pressure is relatively low.";
}

function summarizeSupply(payload) {
  if (Number(payload.fill_rate_pct) < 85 || Number(payload.supplier_delay_days) >= 5) {
    return "Supply stability is weak because fill-rate or supplier-delay risk is elevated.";
  }
  if (Number(payload.fill_rate_pct) < 92 || Number(payload.supplier_delay_days) >= 3) {
    return "Supply stability is manageable but should still be monitored.";
  }
  return "Supply stability looks healthy for the current scenario.";
}

function buildBusinessPortfolio(currentItem) {
  const fallbackPortfolio = [
    samples.premium_electronics,
    samples.perishable_grocery,
    samples.promo_beauty,
    samples.bulky_home,
    samples.delayed_supply,
    samples.home,
  ];
  const uniqueItems = new Map();
  [currentItem, ...fallbackPortfolio].forEach((item) => {
    const normalized = normalizeProductPayload(item);
    const key = `${normalized.category}::${normalized.product_name}`;
    if (!uniqueItems.has(key)) {
      uniqueItems.set(key, normalized);
    }
  });
  return Array.from(uniqueItems.values()).slice(0, 5);
}

function findCurrentRecommendation(recommendationPayload, currentItem) {
  const recommendations = recommendationPayload.recommendations || [];
  return recommendations.find(
    (item) => item.product_name === currentItem.product_name && item.category === currentItem.category,
  ) || recommendations[0] || null;
}

function businessDecisionLabel(priority, recommendation, flags) {
  if (!recommendation) return "Needs review";
  if (priority.predicted_stocking_priority === "High" && flags.length <= 1) return "Prioritize for stocking";
  if (priority.predicted_stocking_priority === "Low" || flags.length >= 3) return "Stock selectively";
  return "Review with caution";
}

function businessNarrative(state) {
  const { payload, priority, sales, selectedRecommendation, goal } = state;
  const flags = dedupeFlags([
    ...(priority.caution_flags || []),
    ...(sales.caution_flags || []),
    ...(selectedRecommendation?.caution_flags || []),
  ]);
  const decision = businessDecisionLabel(priority, selectedRecommendation, flags);
  const rankText = selectedRecommendation
    ? `It ranks #${selectedRecommendation.rank} in the ${titleCaseGoal(goal).toLowerCase()} comparison set.`
    : "It has been scored against the comparison set.";
  return `${payload.product_name} is currently a ${priority.predicted_stocking_priority.toLowerCase()}-priority item. ${decision}. Predicted demand is ${formatCompactNumber(sales.predicted_daily_units_sold)} units per day and ${rankText}`;
}

function attractiveSignals(state) {
  const { priority, sales, selectedRecommendation, payload } = state;
  const signals = [];
  if (priority.predicted_stocking_priority === "High") {
    signals.push(`High-priority confidence is ${formatPercent((priority.probabilities?.High || 0) * 100, 1)}.`);
  }
  if (Number(sales.supporting_information?.comparison_to_reference_pct ?? 0) >= 0) {
    signals.push(`Expected demand is ${formatPercent(sales.supporting_information.comparison_to_reference_pct, 1)} versus the reference group.`);
  }
  if (selectedRecommendation) {
    signals.push(`Expected daily profit is ${formatCurrency(selectedRecommendation.expected_daily_profit)}.`);
    signals.push(`Profit density is ${formatCurrency(selectedRecommendation.profit_per_shelf_unit)} per unit of shelf space.`);
  }
  if (Number(payload.fill_rate_pct) >= 92) {
    signals.push(`Fill rate at ${formatPercent(payload.fill_rate_pct, 1)} supports operational stability.`);
  }
  return signals.slice(0, 4);
}

function riskSignals(state) {
  const { payload, selectedRecommendation } = state;
  const signals = [];
  if (Number(payload.shelf_life_days) <= 14) {
    signals.push("Short shelf life compresses the sell-through window.");
  }
  if (Number(payload.fill_rate_pct) < 90) {
    signals.push("Lower fill rate raises the chance of stock disruption.");
  }
  if (Number(payload.supplier_delay_days) >= 4) {
    signals.push("Supplier delay is high enough to affect replenishment confidence.");
  }
  if (selectedRecommendation && Number(selectedRecommendation.operational_risk_score) >= 45) {
    signals.push(`Operational risk score is elevated at ${formatNumber(selectedRecommendation.operational_risk_score, 1)}.`);
  }
  if (!signals.length) {
    signals.push("No major operational risk pattern stands out in the current scenario.");
  }
  return signals.slice(0, 4);
}

function renderBusinessStatusPills(state) {
  const container = document.getElementById("business-status-pills");
  if (!container) return;
  const pills = [
    state.payload.category,
    state.payload.brand_tier,
    titleCaseGoal(state.goal),
    state.sales.sales_band,
  ];
  container.innerHTML = pills.map((pill) => `<span class="pill neutral">${escapeHtml(pill)}</span>`).join("");
}

function renderBusinessOutput(state) {
  const { priority, sales, selectedRecommendation } = state;
  const flags = dedupeFlags([
    ...(priority.caution_flags || []),
    ...(sales.caution_flags || []),
    ...(selectedRecommendation?.caution_flags || []),
  ]);
  const confidence = Math.max(...Object.values(priority.probabilities || {}), 0) * 100;
  const decision = businessDecisionLabel(priority, selectedRecommendation, flags);
  return `
    <div class="summary-grid business-summary-grid">
      <div class="summary-card emphasis-card">
        <span class="metric-subtle">Predicted Stocking Priority</span>
        <div class="badge-stack">
          <span class="business-badge ${priorityPillClass(priority.predicted_stocking_priority)}">${escapeHtml(priority.predicted_stocking_priority)}</span>
          <span class="small-copy">${escapeHtml(decision)}</span>
        </div>
      </div>
      <div class="summary-card">
        <span class="metric-value">${formatCompactNumber(sales.predicted_daily_units_sold)}</span>
        <span class="metric-subtle">Predicted sales per day</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${formatCurrency(sales.predicted_daily_profit)}</span>
        <span class="metric-subtle">Estimated daily profit</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${selectedRecommendation ? formatNumber(selectedRecommendation.recommendation_score, 1) : "n/a"}</span>
        <span class="metric-subtle">Recommendation score</span>
      </div>
    </div>
    <div class="result-card">
      <div class="rank-topline">
        <div>
          <h3>Recommendation Summary</h3>
          <p class="result-copy">${escapeHtml(businessNarrative(state))}</p>
        </div>
        <div class="pill ${priorityPillClass(priority.predicted_stocking_priority)}">${formatPercent(confidence, 1)} confidence</div>
      </div>
    </div>
    <div class="two-col">
      <div class="result-card">
        <h3>Predicted Sales</h3>
        <div class="summary-grid">
          <div class="summary-card">
            <span class="metric-value">${formatCurrency(sales.predicted_daily_revenue)}</span>
            <span class="metric-subtle">Expected daily revenue</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${formatCurrency(sales.supporting_information?.profit_per_shelf_unit ?? 0)}</span>
            <span class="metric-subtle">Profit per shelf unit</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${formatPercent(sales.supporting_information?.comparison_to_reference_pct ?? 0, 1)}</span>
            <span class="metric-subtle">Vs reference group</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${formatPercent(sales.supporting_information?.shelf_capacity_utilization_pct ?? 0, 1)}</span>
            <span class="metric-subtle">Shelf utilization</span>
          </div>
        </div>
      </div>
      <div class="result-card">
        <h3>Probabilities / Confidence</h3>
        ${probabilityBars(priority.probabilities)}
      </div>
    </div>
    <div class="result-card">
      <h3>Caution Flags</h3>
      ${flagCardsMarkup(flags)}
    </div>
  `;
}

function renderBusinessRecommendation(state) {
  const { goal, selectedRecommendation } = state;
  const positives = attractiveSignals(state);
  const risks = riskSignals(state);
  const flags = dedupeFlags([
    ...(state.priority.caution_flags || []),
    ...(state.sales.caution_flags || []),
    ...(selectedRecommendation?.caution_flags || []),
  ]);
  return `
    <div class="two-col">
      <div class="result-card">
        <div class="rank-topline">
          <div>
            <h3>Final Recommendation</h3>
            <p class="result-copy">${escapeHtml(selectedRecommendation?.recommendation_reason || "The current item has been scored for the selected business lens.")}</p>
          </div>
          <div class="pill ${priorityPillClass(state.priority.predicted_stocking_priority)}">${escapeHtml(businessDecisionLabel(state.priority, selectedRecommendation, flags))}</div>
        </div>
        <div class="summary-grid">
          <div class="summary-card">
            <span class="metric-value">${selectedRecommendation ? `#${selectedRecommendation.rank}` : "n/a"}</span>
            <span class="metric-subtle">Rank in portfolio</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${escapeHtml(titleCaseGoal(goal))}</span>
            <span class="metric-subtle">Decision lens</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${selectedRecommendation ? formatCurrency(selectedRecommendation.profit_per_shelf_unit) : "n/a"}</span>
            <span class="metric-subtle">Profit density</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${selectedRecommendation ? formatNumber(selectedRecommendation.operational_risk_score, 1) : "n/a"}</span>
            <span class="metric-subtle">Operational risk score</span>
          </div>
        </div>
      </div>
      <div class="result-card">
        <h3>Why It Looks Attractive</h3>
        <ul class="insight-list">
          ${positives.map((signal) => `<li>${escapeHtml(signal)}</li>`).join("")}
        </ul>
        <div class="divider-title" style="margin-top:16px;">Why It Looks Risky</div>
        <ul class="insight-list" style="margin-top:10px;">
          ${risks.map((signal) => `<li>${escapeHtml(signal)}</li>`).join("")}
        </ul>
      </div>
    </div>
    <div class="summary-grid">
      <div class="summary-card">
        <span class="metric-subtle">Sales interpretation</span>
        <div class="interpretation-copy">${escapeHtml(summarizeSalesOutlook(state.sales))}</div>
      </div>
      <div class="summary-card">
        <span class="metric-subtle">Profit density interpretation</span>
        <div class="interpretation-copy">${escapeHtml(summarizeProfitDensity(selectedRecommendation))}</div>
      </div>
      <div class="summary-card">
        <span class="metric-subtle">Perishability interpretation</span>
        <div class="interpretation-copy">${escapeHtml(summarizePerishability(state.payload))}</div>
      </div>
      <div class="summary-card">
        <span class="metric-subtle">Supply interpretation</span>
        <div class="interpretation-copy">${escapeHtml(summarizeSupply(state.payload))}</div>
      </div>
    </div>
  `;
}

function businessComparisonDecision(record) {
  const flags = record.caution_flags || [];
  if (record.predicted_stocking_priority === "High" && flags.length <= 1) return "Prioritize";
  if (record.predicted_stocking_priority === "Low" || flags.length >= 3) return "Selective";
  return "Watch closely";
}

function comparisonCardMarkup(record, title, subtitle, extraCopy = "") {
  return `
    <div class="comparison-card">
      <div class="rank-topline">
        <div>
          <h3>${escapeHtml(title)}</h3>
          <div class="rank-meta">
            <span>${escapeHtml(subtitle)}</span>
            <span>${escapeHtml(record.sales_band)}</span>
          </div>
        </div>
        <div class="pill ${priorityPillClass(record.predicted_stocking_priority)}">${escapeHtml(record.predicted_stocking_priority)}</div>
      </div>
      <div class="summary-grid">
        <div class="summary-card">
          <span class="metric-value">${formatCompactNumber(record.predicted_daily_units_sold)}</span>
          <span class="metric-subtle">Predicted sales</span>
        </div>
        <div class="summary-card">
          <span class="metric-value">${formatCurrency(record.expected_daily_profit)}</span>
          <span class="metric-subtle">Expected daily profit</span>
        </div>
        <div class="summary-card">
          <span class="metric-value">${formatPercent(record.priority_probability_high, 1)}</span>
          <span class="metric-subtle">High-priority confidence</span>
        </div>
        <div class="summary-card">
          <span class="metric-value">${escapeHtml(businessComparisonDecision(record))}</span>
          <span class="metric-subtle">Recommendation view</span>
        </div>
      </div>
      ${extraCopy ? `<div class="notice">${extraCopy}</div>` : ""}
      <div class="result-card">
        <h4>Risk Flags</h4>
        ${flagsMarkup(record.caution_flags)}
      </div>
    </div>
  `;
}

function renderBusinessComparison(payload) {
  const scenarioCards = (payload.scenarios || []).map((scenario) => {
    const changeSummary = Object.entries(scenario.applied_changes || {})
      .map(([key, value]) => `${key}=${value}`)
      .join(", ");
    return comparisonCardMarkup(
      scenario,
      scenario.scenario_name,
      `${scenario.predicted_stocking_priority} priority`,
      `Applied changes: ${changeSummary}. Delta profit vs baseline: ${formatCurrency(scenario.delta_profit_vs_baseline)}.`,
    );
  }).join("");
  return `
    <div class="comparison-grid">
      ${comparisonCardMarkup(payload.baseline, "Current Baseline", "Starting business case")}
      ${scenarioCards}
    </div>
  `;
}

function businessFeatureRows(rows) {
  return (rows || []).slice(0, 4).map((row) => ({
    feature: row.feature,
    value: Math.abs(Number(row.coefficient ?? 0)),
  }));
}

function renderBusinessInsightsMarkup(cache) {
  const { summary, performance, featureImportance, businessFindings } = cache;
  const deployedModels = (summary.models_used || []).filter((model) => String(model.status || "").toLowerCase().includes("deployed"));
  const classifierRows = (performance.classification?.comparison_table || []).slice(0, 3);
  const regressionRows = (performance.regression?.comparison_table || []).slice(0, 3);
  const priorityDriverRows = businessFeatureRows(featureImportance.priority_model?.top_numeric_drivers_for_high_priority);
  const salesDriverRows = businessFeatureRows(featureImportance.sales_model?.top_numeric_drivers_for_sales);
  const topTakeaways = (businessFindings.plain_language_takeaways || []).slice(0, 4);

  return `
    <div class="summary-grid">
      <div class="summary-card">
        <span class="metric-value">${deployedModels.length}</span>
        <span class="metric-subtle">Deployed models used in the app</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${escapeHtml(deployedModels[0]?.model_name || "n/a")}</span>
        <span class="metric-subtle">Primary classification model</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${escapeHtml(deployedModels[1]?.model_name || "n/a")}</span>
        <span class="metric-subtle">Primary sales model</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${topTakeaways.length}</span>
        <span class="metric-subtle">Key business findings highlighted</span>
      </div>
    </div>
    <div class="insight-columns">
      <div class="result-card">
        <h3>Model Performance Summary Table</h3>
        <div class="divider-title">Classification</div>
        ${renderCompactTable(
          [
            { key: "model_name", label: "Model" },
            { key: "accuracy", label: "Accuracy" },
            { key: "weighted_f1", label: "Weighted F1" },
          ],
          classifierRows,
        )}
        <div class="divider-title" style="margin-top:16px;">Regression</div>
        ${renderCompactTable(
          [
            { key: "model_name", label: "Model" },
            { key: "rmse", label: "RMSE" },
            { key: "r2", label: "R^2" },
          ],
          regressionRows,
        )}
      </div>
      <div class="result-card">
        <h3>Top Business Findings</h3>
        <ul class="insight-list">
          ${topTakeaways.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
      </div>
    </div>
    <div class="insight-columns">
      <div class="result-card">
        <h3>Model Comparison Chart</h3>
        <div class="divider-title">Classification weighted F1</div>
        ${renderBarRows(performance.classification?.comparison_chart || [], "label", "value")}
        <div class="divider-title" style="margin-top:16px;">Regression R^2</div>
        ${renderBarRows(performance.regression?.comparison_chart || [], "label", "value")}
      </div>
      <div class="result-card">
        <h3>Feature Importance Summary</h3>
        <div class="divider-title">Top priority drivers</div>
        ${renderBarRows(priorityDriverRows, "feature", "value")}
        <div class="divider-title" style="margin-top:16px;">Top sales drivers</div>
        ${renderBarRows(salesDriverRows, "feature", "value")}
      </div>
    </div>
  `;
}

function renderInsightsView() {
  if (!insightsCache) return;
  document.getElementById("insights-result").innerHTML = renderInsightsMarkup(insightsCache);
}

async function loadInsightsData(forceRefresh = false) {
  if (insightsCache && !forceRefresh) {
    return insightsCache;
  }
  const [summary, performance, featureImportance, businessFindings] = await Promise.all([
    getJSON("/insights/summary"),
    getJSON("/insights/model-performance"),
    getJSON("/insights/feature-importance"),
    getJSON("/insights/business-findings"),
  ]);
  insightsCache = { summary, performance, featureImportance, businessFindings };
  return insightsCache;
}

async function loadInsights(forceRefresh = false) {
  showLoading("insights-result", "Loading precomputed model insights...");
  try {
    await loadInsightsData(forceRefresh);
    renderInsightsView();
  } catch (error) {
    showError("insights-result", error);
  }
}

async function loadBusinessInsights(forceRefresh = false) {
  showLoading("business-insights", "Loading simplified insight summary...");
  try {
    const cache = await loadInsightsData(forceRefresh);
    document.getElementById("business-insights").innerHTML = renderBusinessInsightsMarkup(cache);
    businessState.raw.insights = cache;
    updateBusinessRawOutput();
    if (document.getElementById("insights-tab").classList.contains("is-active")) {
      renderInsightsView();
    }
  } catch (error) {
    showError("business-insights", error);
  }
}

function modelLabPillClass(model) {
  const status = String(model.status || "").toLowerCase();
  const mode = String(model.compare_mode || "").toLowerCase();
  if (status.includes("deployed")) return "good";
  if (mode.includes("live")) return "warn";
  return "neutral";
}

function metricOrNA(value, digits = 4) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "n/a";
  return Number(value).toFixed(digits);
}

function renderModelLabInsights(cache) {
  const models = cache.models || [];
  const performanceRows = cache.performance_table || [];
  const deployment = cache.deployment_choice || {};
  const selectedMatrix = cache.confusion_matrices?.[cache.selected_confusion_matrix_key] || { labels: [], matrix: [] };

  return `
    <section class="insight-section">
      <div class="insight-section-header">
        <h3>Explored Model Families</h3>
        <p>This lab showcases the Week 4 comparison across logistic baselines, a custom deep learning model, and a Hugging Face transformer benchmark.</p>
      </div>
      <div class="summary-grid">
        <div class="summary-card">
          <span class="metric-value">${models.filter((model) => model.compare_mode === "live").length}</span>
          <span class="metric-subtle">Live compare models</span>
        </div>
        <div class="summary-card">
          <span class="metric-value">${models.filter((model) => model.compare_mode !== "live").length}</span>
          <span class="metric-subtle">Benchmark-only models</span>
        </div>
        <div class="summary-card">
          <span class="metric-value">${escapeHtml(deployment.selected_model_name || "n/a")}</span>
          <span class="metric-subtle">Chosen for deployment</span>
        </div>
      </div>
      <div class="insight-grid">
        ${models.map((model) => `
          <div class="insight-card">
            <div class="pill ${modelLabPillClass(model)}">${escapeHtml(model.status)}</div>
            <h4 style="margin-top:10px;">${escapeHtml(model.model_name)}</h4>
            <p class="insight-muted">${escapeHtml(model.purpose)}</p>
            <div class="divider-title">Inputs</div>
            <p>${escapeHtml(model.inputs)}</p>
            <div class="divider-title">Strengths</div>
            <p>${escapeHtml(model.strengths)}</p>
            <div class="divider-title">Limitations</div>
            <p>${escapeHtml(model.limitations)}</p>
          </div>
        `).join("")}
      </div>
    </section>

    <section class="insight-section">
      <div class="insight-section-header">
        <h3>Performance Comparison</h3>
        <p>The logistic rows are recreated from the Week 4 design on the local dataset, while the custom deep learning and Hugging Face rows come from the saved notebook benchmark outputs.</p>
      </div>
      <div class="result-card">
        <h3>Model Metrics Table</h3>
        ${renderCompactTable(
          [
            { key: "model_name", label: "Model" },
            { key: "status", label: "Status" },
            { key: "accuracy", label: "Accuracy" },
            { key: "precision_macro", label: "Macro Precision" },
            { key: "recall_macro", label: "Macro Recall" },
            { key: "weighted_f1", label: "Weighted F1" },
          ],
          performanceRows,
        )}
      </div>
      <div class="insight-columns">
        <div class="result-card">
          <h3>Weighted F1 Comparison</h3>
          ${renderBarRows(cache.weighted_f1_chart || [], "label", "value")}
        </div>
        <div class="result-card">
          <h3>Accuracy Comparison</h3>
          ${renderBarRows(cache.accuracy_chart || [], "label", "value")}
        </div>
      </div>
      <div class="result-card">
        <h3>Selected Confusion Matrix</h3>
        <p class="lab-note">The hybrid logistic regression confusion matrix is shown because it is the selected deployed family.</p>
        ${renderConfusionMatrix(selectedMatrix)}
      </div>
    </section>

    <section class="insight-section">
      <div class="insight-section-header">
        <h3>Why The Deployed Model Was Selected</h3>
        <p>This section makes the deployment choice explicit in terms of performance, interpretability, stability, and demo readiness.</p>
      </div>
      <div class="notice">
        <strong>${escapeHtml(deployment.headline || "")}</strong><br />
        ${escapeHtml(deployment.deployment_summary || "")}
      </div>
      <div class="result-card">
        <h3>Selection Rationale</h3>
        <ul class="insight-list">
          ${(deployment.why_selected || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
      </div>
      <div class="result-card">
        <h3>Trade-off Matrix</h3>
        <div class="candidate-table-wrap">
          <table class="criterion-table">
            <thead>
              <tr>
                <th>Criterion</th>
                <th>Hybrid Logistic</th>
                <th>Custom DL</th>
                <th>HF Transformer</th>
                <th>Interpretation</th>
              </tr>
            </thead>
            <tbody>
              ${(deployment.selection_matrix || []).map((row) => `
                <tr>
                  <td>${escapeHtml(row.criterion)}</td>
                  <td>${escapeHtml(row.selected_model)}</td>
                  <td>${escapeHtml(row.custom_dl)}</td>
                  <td>${escapeHtml(row.hf_transformer)}</td>
                  <td>${escapeHtml(row.summary)}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
      <div class="result-card">
        <h3>Model Lab Notes</h3>
        <ul class="insight-list">
          ${(cache.compare_notes || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
      </div>
    </section>
  `;
}

function renderModelLabView() {
  if (!modelLabCache) return;
  document.getElementById("model-lab-insights").innerHTML = renderModelLabInsights(modelLabCache);
}

function renderModelComparisonResults(payload) {
  const scenario = payload.scenario_summary || {};
  const compared = payload.compared_models || [];
  return `
    <div class="notice">
      <strong>${escapeHtml(payload.deployment_choice?.selected_model_name || "Selected model")}</strong><br />
      ${escapeHtml(payload.deployment_choice?.deployment_summary || "")}
    </div>
    <div class="summary-grid">
      <div class="summary-card">
        <span class="metric-value">${escapeHtml(scenario.product_name || "Demo Product")}</span>
        <span class="metric-subtle">Scenario product</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${escapeHtml(scenario.category || "n/a")}</span>
        <span class="metric-subtle">Category</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${escapeHtml(scenario.brand_tier || "n/a")}</span>
        <span class="metric-subtle">Brand tier</span>
      </div>
      <div class="summary-card">
        <span class="metric-value">${(payload.defaulted_fields || []).length}</span>
        <span class="metric-subtle">Defaulted context fields</span>
      </div>
    </div>
    <div class="result-card">
      <h3>Context Handling</h3>
      <p class="lab-note">${escapeHtml(payload.default_context_note || "")}</p>
      <div class="tag-cloud" style="margin-top:12px;">
        ${(payload.defaulted_fields || []).slice(0, 16).map((field) => `<span class="tag">${escapeHtml(field)}</span>`).join("")}
      </div>
    </div>
    ${compared.map((model) => `
      <div class="rank-card">
        <div class="rank-topline">
          <div>
            <h3>${escapeHtml(model.model_name)}</h3>
            <div class="rank-meta">
              <span>${escapeHtml(model.inference_status.replaceAll("_", " "))}</span>
              <span>${escapeHtml(model.compare_mode.replaceAll("_", " "))}</span>
            </div>
          </div>
          <div class="pill ${model.compare_mode === "live" ? "good" : "neutral"}">
            ${model.prediction ? `${escapeHtml(model.prediction)} • ${formatPercent(Number(model.top_confidence || 0) * 100, 1)}` : "Benchmark only"}
          </div>
        </div>
        <div class="summary-grid">
          <div class="summary-card">
            <span class="metric-value">${metricOrNA(model.benchmark_accuracy)}</span>
            <span class="metric-subtle">Benchmark accuracy</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${metricOrNA(model.benchmark_weighted_f1)}</span>
            <span class="metric-subtle">Benchmark weighted F1</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${escapeHtml(model.inference_status)}</span>
            <span class="metric-subtle">Inference status</span>
          </div>
          <div class="summary-card">
            <span class="metric-value">${escapeHtml(model.compare_mode)}</span>
            <span class="metric-subtle">Compare mode</span>
          </div>
        </div>
        ${model.probabilities ? `
          <div class="result-card">
            <h4>Class Confidence</h4>
            ${probabilityBars(model.probabilities)}
          </div>
        ` : `
          <div class="notice">No live inference output is attached for this model in the current local project. The benchmark metrics are still shown from the saved Week 4 experiment output.</div>
        `}
        <div class="result-card">
          <h4>Strengths</h4>
          <p>${escapeHtml(model.strengths || "")}</p>
          <div class="divider-title" style="margin-top:16px;">Limitations</div>
          <p>${escapeHtml(model.limitations || "")}</p>
          <div class="divider-title" style="margin-top:16px;">Deployment relevance</div>
          <p>${escapeHtml(model.deployment_relevance || "")}</p>
        </div>
      </div>
    `).join("")}
  `;
}

async function loadModelLab(forceRefresh = false) {
  if (modelLabCache && !forceRefresh) {
    renderModelLabView();
    return;
  }
  showLoading("model-lab-insights", "Loading Model Lab benchmark summary...");
  try {
    modelLabCache = await getJSON("/insights/model-comparison");
    renderModelLabView();
  } catch (error) {
    showError("model-lab-insights", error);
  }
}

function showLoading(targetId, text) {
  const target = document.getElementById(targetId);
  if (!target) return;
  target.innerHTML = `<div class="loading">${escapeHtml(text)}</div>`;
}

function formatError(error) {
  if (typeof error === "string") return error;
  if (error?.detail) return JSON.stringify(error.detail, null, 2);
  return JSON.stringify(error, null, 2);
}

function showError(targetId, error) {
  const detail = formatError(error);
  const target = document.getElementById(targetId);
  if (!target) return;
  target.innerHTML = `<div class="loading error">${escapeHtml(detail)}</div>`;
}

async function postJSON(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok) {
    throw data;
  }
  return data;
}

async function getJSON(url) {
  const response = await fetch(url);
  const data = await response.json();
  if (!response.ok) {
    throw data;
  }
  return data;
}

function normalizeCandidate(product) {
  return normalizeProductPayload(product);
}

function renderCandidateTable(products) {
  const tbody = document.querySelector("#candidate-table tbody");
  if (!tbody) return;
  tbody.innerHTML = products.map((product, index) => {
    const item = normalizeCandidate(product);
    return `
      <tr data-row-index="${index}">
        <td><input data-field="product_name" value="${escapeHtml(item.product_name)}" /></td>
        <td>
          <select data-field="category">
            ${["Beauty", "Clothing", "Electronics", "Grocery", "Home"].map((option) => `<option value="${option}" ${item.category === option ? "selected" : ""}>${option}</option>`).join("")}
          </select>
        </td>
        <td>
          <select data-field="brand_tier">
            ${["Budget", "Mid", "Premium"].map((option) => `<option value="${option}" ${item.brand_tier === option ? "selected" : ""}>${option}</option>`).join("")}
          </select>
        </td>
        <td>
          <select data-field="promotion_type">
            ${["Unknown", "Festival", "Flash Sale", "BOGO", "Loyalty Only", "Seasonal Discount"].map((option) => `<option value="${option}" ${item.promotion_type === option ? "selected" : ""}>${option}</option>`).join("")}
          </select>
        </td>
        <td><input type="number" step="0.01" min="0" data-field="current_price" value="${item.current_price}" /></td>
        <td><input type="number" step="1" min="0" data-field="shelf_capacity" value="${item.shelf_capacity}" /></td>
        <td><input type="number" step="1" min="0" data-field="lead_time_days" value="${item.lead_time_days}" /></td>
        <td><input type="number" step="0.01" min="0" data-field="marketing_spend" value="${item.marketing_spend}" /></td>
        <td><input type="number" step="1" min="0" data-field="shelf_life_days" value="${item.shelf_life_days}" /></td>
        <td><input type="number" step="0.01" min="0" max="100" data-field="fill_rate_pct" value="${item.fill_rate_pct}" /></td>
        <td><input type="number" step="1" min="0" data-field="supplier_delay_days" value="${item.supplier_delay_days}" /></td>
      </tr>
    `;
  }).join("");
}

function readCandidateTable() {
  return Array.from(document.querySelectorAll("#candidate-table tbody tr")).map((row) => {
    const get = (field) => row.querySelector(`[data-field="${field}"]`).value;
    return normalizeCandidate({
      product_name: get("product_name"),
      category: get("category"),
      brand_tier: get("brand_tier"),
      promotion_type: get("promotion_type"),
      current_price: get("current_price"),
      shelf_capacity: get("shelf_capacity"),
      lead_time_days: get("lead_time_days"),
      marketing_spend: get("marketing_spend"),
      shelf_life_days: get("shelf_life_days"),
      fill_rate_pct: get("fill_rate_pct"),
      supplier_delay_days: get("supplier_delay_days"),
    });
  });
}

function renderScenarioTable(items) {
  const tbody = document.querySelector("#scenario-table tbody");
  if (!tbody) return;
  tbody.innerHTML = items.map((scenario, index) => `
    <tr data-row-index="${index}">
      <td><input data-field="scenario_name" value="${escapeHtml(scenario.scenario_name)}" /></td>
      <td>
        <select data-field="promotion_type">
          ${["Unknown", "Festival", "Flash Sale", "BOGO", "Loyalty Only", "Seasonal Discount"].map((option) => `<option value="${option}" ${scenario.overrides.promotion_type === option ? "selected" : ""}>${option}</option>`).join("")}
        </select>
      </td>
      <td><input type="number" min="0" step="0.01" data-field="marketing_spend" value="${Number(scenario.overrides.marketing_spend ?? 0)}" /></td>
      <td><input type="number" min="0" step="1" data-field="shelf_life_days" value="${Number(scenario.overrides.shelf_life_days ?? 0)}" /></td>
      <td><input type="number" min="0" max="100" step="0.01" data-field="fill_rate_pct" value="${Number(scenario.overrides.fill_rate_pct ?? 0)}" /></td>
    </tr>
  `).join("");
}

function readScenarioTable() {
  return Array.from(document.querySelectorAll("#scenario-table tbody tr")).map((row) => {
    const get = (field) => row.querySelector(`[data-field="${field}"]`).value;
    return {
      scenario_name: get("scenario_name"),
      overrides: {
        promotion_type: get("promotion_type"),
        marketing_spend: Number(get("marketing_spend")),
        shelf_life_days: Number(get("shelf_life_days")),
        fill_rate_pct: Number(get("fill_rate_pct")),
      },
    };
  });
}

function historicalPayload() {
  const listOrNull = (value) => (value ? [value] : null);
  const numericOrNull = (value) => (value === "" ? null : Number(value));
  return {
    categories: listOrNull(document.getElementById("history-category").value),
    brand_tiers: listOrNull(document.getElementById("history-brand-tier").value),
    promotion_types: listOrNull(document.getElementById("history-promo").value),
    store_types: listOrNull(document.getElementById("history-store-type").value),
    price_min: numericOrNull(document.getElementById("history-price-min").value),
    price_max: numericOrNull(document.getElementById("history-price-max").value),
    shelf_life_min: numericOrNull(document.getElementById("history-shelf-life-min").value),
    shelf_life_max: numericOrNull(document.getElementById("history-shelf-life-max").value),
    sort_by: document.getElementById("history-sort-by").value,
    top_n: Number(document.getElementById("history-top-n").value || 8),
  };
}

function renderRawSection(title, payload) {
  return `
    <div class="result-card">
      <h3>${escapeHtml(title)}</h3>
      <pre class="code-block">${escapeHtml(JSON.stringify(payload, null, 2))}</pre>
    </div>
  `;
}

function updateBusinessRawOutput() {
  const target = document.getElementById("business-raw-output");
  if (!target) return;
  const sections = [];
  if (businessState.raw.workflow) {
    sections.push(renderRawSection("Workflow Payloads", businessState.raw.workflow));
  }
  if (businessState.raw.scenario) {
    sections.push(renderRawSection("Scenario Comparison Payload", businessState.raw.scenario));
  }
  if (businessState.raw.insights) {
    sections.push(renderRawSection("Insights Summary Payload", businessState.raw.insights));
  }
  target.innerHTML = sections.length
    ? sections.join("")
    : `<div class="empty-state">Raw priority, sales, recommendation, scenario, and insight payloads will appear here for technical review.</div>`;
}

async function activateTab(tabTarget) {
  document.querySelectorAll(".tab-button").forEach((tab) => tab.classList.remove("is-active"));
  document.querySelectorAll(".tab-panel").forEach((panel) => panel.classList.remove("is-active"));

  const button = document.querySelector(`.tab-button[data-tab-target="${tabTarget}"]`);
  const panel = document.getElementById(tabTarget);
  if (button) button.classList.add("is-active");
  if (panel) panel.classList.add("is-active");

  if (tabTarget === "business-demo-tab") {
    await loadBusinessInsights(false);
  }
  if (tabTarget === "insights-tab") {
    await loadInsights(false);
  }
  if (tabTarget === "model-lab-tab") {
    await loadModelLab(false);
  }
}

function bindTabs() {
  document.querySelectorAll(".tab-button").forEach((button) => {
    button.addEventListener("click", async () => {
      await activateTab(button.dataset.tabTarget);
    });
  });
}

function bindOpenTabButtons() {
  document.querySelectorAll("[data-open-tab]").forEach((button) => {
    button.addEventListener("click", async () => {
      await activateTab(button.dataset.openTab);
    });
  });
}

function setDemoMode(isEnabled) {
  document.body.classList.toggle("demo-mode", isEnabled);
  const copy = document.getElementById("demo-mode-copy");
  if (copy) {
    copy.textContent = isEnabled ? "Demo Mode On" : "Technical View On";
  }
  if (isEnabled && document.querySelector(".tab-button.is-active.technical-tab")) {
    void activateTab("business-demo-tab");
  }
}

function bindDemoModeToggle() {
  const toggle = document.getElementById("demo-mode-toggle");
  if (!toggle) return;
  toggle.addEventListener("change", () => {
    setDemoMode(toggle.checked);
  });
}

function bindSampleButtons() {
  document.querySelectorAll("[data-load-sample]").forEach((button) => {
    button.addEventListener("click", () => {
      const [formId, sampleName] = button.dataset.loadSample.split(":");
      setFormValues(formId, samples[sampleName]);
    });
  });
}

function applyBusinessScenario(scenarioKey) {
  const scenario = businessDemoScenarios[scenarioKey];
  if (!scenario) return;
  businessState.activeScenario = scenarioKey;
  businessState.activeCompareSet = scenario.compareKey;
  document.getElementById("business-goal").value = scenario.goal;
  setFormValues("business-demo-form", scenario.payload);
  void runBusinessWorkflow();
}

function bindSpecialButtons() {
  document.getElementById("load-portfolio-core").addEventListener("click", () => renderCandidateTable(portfolios.core));
  document.getElementById("load-portfolio-risk").addEventListener("click", () => renderCandidateTable(portfolios.risk));
  document.getElementById("load-history-grocery").addEventListener("click", () => {
    document.getElementById("history-category").value = "Grocery";
    document.getElementById("history-brand-tier").value = "Budget";
    document.getElementById("history-promo").value = "BOGO";
    document.getElementById("history-store-type").value = "Urban";
    document.getElementById("history-price-min").value = "";
    document.getElementById("history-price-max").value = "20";
    document.getElementById("history-shelf-life-min").value = "";
    document.getElementById("history-shelf-life-max").value = "30";
    document.getElementById("history-sort-by").value = "avg_daily_units_sold";
    document.getElementById("history-top-n").value = "8";
  });
  document.getElementById("load-history-premium").addEventListener("click", () => {
    document.getElementById("history-category").value = "";
    document.getElementById("history-brand-tier").value = "Premium";
    document.getElementById("history-promo").value = "Flash Sale";
    document.getElementById("history-store-type").value = "Urban";
    document.getElementById("history-price-min").value = "20";
    document.getElementById("history-price-max").value = "250";
    document.getElementById("history-shelf-life-min").value = "180";
    document.getElementById("history-shelf-life-max").value = "";
    document.getElementById("history-sort-by").value = "avg_profit_density";
    document.getElementById("history-top-n").value = "8";
  });
  document.getElementById("load-scenario-marketing").addEventListener("click", () => renderScenarioTable(technicalScenarioSets.marketing));
  document.getElementById("load-scenario-shelf-life").addEventListener("click", () => renderScenarioTable(technicalScenarioSets.shelfLife));
  document.getElementById("insights-refresh").addEventListener("click", async () => {
    await loadInsights(true);
  });
  document.getElementById("insights-experiment-group").addEventListener("change", () => {
    renderInsightsView();
  });
  document.getElementById("model-lab-refresh").addEventListener("click", async () => {
    await loadModelLab(true);
  });
  document.getElementById("business-insights-refresh").addEventListener("click", async () => {
    await loadBusinessInsights(true);
  });
  document.getElementById("business-reset-defaults").addEventListener("click", () => {
    applyBusinessScenario("premium_electronics");
  });
  document.querySelectorAll("[data-business-scenario]").forEach((button) => {
    button.addEventListener("click", () => {
      applyBusinessScenario(button.dataset.businessScenario);
    });
  });
  document.querySelectorAll("[data-business-scenario-set]").forEach((button) => {
    button.addEventListener("click", async () => {
      businessState.activeCompareSet = button.dataset.businessScenarioSet;
      showLoading("business-comparison", "Running scenario comparison...");
      try {
        const payload = {
          base_product: businessPayload(),
          scenarios: businessScenarioSets[businessState.activeCompareSet],
        };
        const result = await postJSON("/simulate", payload);
        businessState.raw.scenario = result;
        updateBusinessRawOutput();
        document.getElementById("business-comparison").innerHTML = renderBusinessComparison(result);
      } catch (error) {
        showError("business-comparison", error);
      }
    });
  });
}

async function runBusinessWorkflow() {
  const payload = businessPayload();
  const goal = document.getElementById("business-goal").value;
  const portfolio = buildBusinessPortfolio(payload);
  const scenarioSet = businessScenarioSets[businessState.activeCompareSet] || businessScenarioSets.promo;

  showLoading("business-output", "Running business workflow...");
  showLoading("business-recommendation", "Translating predictions into a recommendation...");
  showLoading("business-comparison", "Running scenario comparison...");

  try {
    const [priority, sales, recommendation, comparison] = await Promise.all([
      postJSON("/predict", payload),
      postJSON("/predict/sales", payload),
      postJSON("/recommend", {
        products: portfolio,
        optimization_goal: goal,
        top_n: portfolio.length,
      }),
      postJSON("/simulate", {
        base_product: payload,
        scenarios: scenarioSet,
      }),
    ]);

    const selectedRecommendation = findCurrentRecommendation(recommendation, payload);
    const state = {
      payload,
      goal,
      priority,
      sales,
      recommendation,
      selectedRecommendation,
    };

    renderBusinessStatusPills(state);
    document.getElementById("business-output").innerHTML = renderBusinessOutput(state);
    document.getElementById("business-recommendation").innerHTML = renderBusinessRecommendation(state);
    document.getElementById("business-comparison").innerHTML = renderBusinessComparison(comparison);

    businessState.raw.workflow = {
      input: payload,
      priority,
      sales,
      recommendation,
      selectedRecommendation,
    };
    businessState.raw.scenario = comparison;
    updateBusinessRawOutput();

    void loadBusinessInsights(false);
  } catch (error) {
    showError("business-output", error);
    showError("business-recommendation", error);
    showError("business-comparison", error);
  }
}

function bindActions() {
  document.getElementById("priority-submit").addEventListener("click", async () => {
    showLoading("priority-result", "Running stocking-priority classification...");
    try {
      const result = await postJSON("/predict", formPayload("priority-form"));
      document.getElementById("priority-result").innerHTML = renderPriorityResult(result);
    } catch (error) {
      showError("priority-result", error);
    }
  });

  document.getElementById("sales-submit").addEventListener("click", async () => {
    showLoading("sales-result", "Running daily sales prediction...");
    try {
      const result = await postJSON("/predict/sales", formPayload("sales-form"));
      document.getElementById("sales-result").innerHTML = renderSalesResult(result);
    } catch (error) {
      showError("sales-result", error);
    }
  });

  document.getElementById("recommend-submit").addEventListener("click", async () => {
    showLoading("recommend-result", "Scoring candidate products...");
    try {
      const payload = {
        products: readCandidateTable(),
        optimization_goal: document.getElementById("recommend-goal").value,
        top_n: Number(document.getElementById("recommend-top-n").value || 5),
      };
      const result = await postJSON("/recommend", payload);
      document.getElementById("recommend-result").innerHTML = recommendationCards(result);
    } catch (error) {
      showError("recommend-result", error);
    }
  });

  document.getElementById("historical-submit").addEventListener("click", async () => {
    showLoading("historical-result", "Filtering historical dataset...");
    try {
      const result = await postJSON("/query/historical", historicalPayload());
      document.getElementById("historical-result").innerHTML = historicalMarkup(result);
    } catch (error) {
      showError("historical-result", error);
    }
  });

  document.getElementById("scenario-submit").addEventListener("click", async () => {
    showLoading("scenario-result", "Running scenario simulation...");
    try {
      const payload = {
        base_product: formPayload("scenario-form"),
        scenarios: readScenarioTable(),
      };
      const result = await postJSON("/simulate", payload);
      document.getElementById("scenario-result").innerHTML = scenarioMarkup(result);
    } catch (error) {
      showError("scenario-result", error);
    }
  });

  document.getElementById("model-lab-submit").addEventListener("click", async () => {
    showLoading("model-lab-result", "Comparing model families on this scenario...");
    try {
      const result = await postJSON("/predict/compare-models", formPayload("model-lab-form"));
      document.getElementById("model-lab-result").innerHTML = renderModelComparisonResults(result);
    } catch (error) {
      showError("model-lab-result", error);
    }
  });

  document.getElementById("business-submit").addEventListener("click", async () => {
    await runBusinessWorkflow();
  });
}

async function bootstrap() {
  renderProductForms();
  bindTabs();
  bindOpenTabButtons();
  bindDemoModeToggle();
  bindSampleButtons();
  bindSpecialButtons();
  bindActions();

  setFormValues("priority-form", samples.priority_high);
  setFormValues("sales-form", samples.home);
  setFormValues("scenario-form", samples.beauty);
  setFormValues("model-lab-form", samples.electronics);
  renderCandidateTable(portfolios.core);
  renderScenarioTable(technicalScenarioSets.promo);

  setFormValues("business-demo-form", businessDemoScenarios.premium_electronics.payload);
  document.getElementById("business-goal").value = businessDemoScenarios.premium_electronics.goal;
  setDemoMode(true);

  await runBusinessWorkflow();
}

void bootstrap();
