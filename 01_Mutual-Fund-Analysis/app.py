import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FundIQ | Mutual Fund Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
    color: #ffffff;
}

[data-testid="stSidebar"] {
    background-color: #161b22;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #ffffff;
}

.subtitle {
    font-size: 16px;
    color: #aab2bf;
}

.metric-card {
    background-color: #1c2330;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #303846;
}

.metric-label {
    color: #aab2bf;
    font-size: 14px;
}

.metric-value {
    color: #ffffff;
    font-size: 27px;
    font-weight: bold;
}

.section-title {
    font-size: 23px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

DATA_PATH = Path(__file__).parent / "Top_30_Mutual_Funds.xlsx"


@st.cache_data
def load_data():

    data = pd.read_excel(DATA_PATH)

    # Clean column names
    data.columns = (
        data.columns.astype(str)
        .str.strip()
        .str.lower()
    )

    # Create final_score from fund_score
    if "final_score" not in data.columns:

        if "fund_score" in data.columns:
            data["final_score"] = data["fund_score"]

        elif "expense_score" in data.columns:
            data["final_score"] = data["expense_score"]

        else:
            data["final_score"] = 0

    # Create rank automatically
    if "rank" not in data.columns:

        data = data.sort_values(
            by="final_score",
            ascending=False
        ).reset_index(drop=True)

        data.insert(
            0,
            "rank",
            range(1, len(data) + 1)
        )

    return data


try:
    df = load_data()

except FileNotFoundError:

    st.error(
        "Dataset not found. Please upload "
        "Top_30_Mutual_Funds.xlsx in the same folder as app.py."
    )

    st.stop()

except Exception as e:

    st.error(f"Unable to load dataset: {e}")
    st.stop()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">📊 FundIQ</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Mutual Fund Investment Intelligence Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.write("")

st.markdown("---")


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("⚙️ Dashboard Filters")

filtered_df = df.copy()


# Category filter

if "category" in df.columns:

    categories = sorted(
        df["category"].dropna().astype(str).unique()
    )

    selected_categories = st.sidebar.multiselect(
        "Select Category",
        categories,
        default=categories
    )

    filtered_df = filtered_df[
        filtered_df["category"].astype(str).isin(
            selected_categories
        )
    ]


# Sub-category filter

if "sub_category" in filtered_df.columns:

    subcategories = sorted(
        filtered_df["sub_category"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_subcategories = st.sidebar.multiselect(
        "Select Sub-Category",
        subcategories,
        default=subcategories
    )

    filtered_df = filtered_df[
        filtered_df["sub_category"].astype(str).isin(
            selected_subcategories
        )
    ]


# Risk level filter

if "risk_level" in filtered_df.columns:

    risks = sorted(
        filtered_df["risk_level"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_risks = st.sidebar.multiselect(
        "Select Risk Level",
        risks,
        default=risks
    )

    filtered_df = filtered_df[
        filtered_df["risk_level"].astype(str).isin(
            selected_risks
        )
    ]


st.sidebar.markdown("---")

st.sidebar.caption(
    "FundIQ | Mutual Fund Analysis Project"
)


# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📌 Investment Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


total_funds = len(filtered_df)

total_amcs = (
    filtered_df["amc_name"].nunique()
    if "amc_name" in filtered_df.columns else 0
)

avg_rating = (
    filtered_df["rating"].mean()
    if "rating" in filtered_df.columns
    and not filtered_df.empty else 0
)

avg_returns = (
    filtered_df["returns_3yr"].mean()
    if "returns_3yr" in filtered_df.columns
    and not filtered_df.empty else 0
)


with col1:
    st.metric(
        "Total Mutual Funds",
        total_funds
    )

with col2:
    st.metric(
        "Total AMCs",
        total_amcs
    )

with col3:
    st.metric(
        "Average Rating",
        f"{avg_rating:.2f}"
    )

with col4:
    st.metric(
        "Average 3-Year Return",
        f"{avg_returns:.2f}%"
    )


st.markdown("---")


# --------------------------------------------------
# TOP PERFORMING MUTUAL FUNDS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🏆 Top Performing Mutual Funds</div>',
    unsafe_allow_html=True
)

if not filtered_df.empty:

    top_funds = filtered_df.sort_values(
        by="final_score",
        ascending=False
    ).head(10)

    display_columns = [
        col for col in [
            "rank",
            "scheme_name",
            "category",
            "sub_category",
            "rating",
            "risk_level",
            "returns_1yr",
            "returns_3yr",
            "returns_5yr",
            "final_score"
        ]
        if col in top_funds.columns
    ]

    st.dataframe(
        top_funds[display_columns],
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning("No funds available for selected filters.")


st.markdown("---")


# --------------------------------------------------
# RETURNS ANALYSIS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📈 Returns Analysis</div>',
    unsafe_allow_html=True
)

return_columns = [
    col for col in [
        "returns_1yr",
        "returns_3yr",
        "returns_5yr"
    ]
    if col in filtered_df.columns
]

if return_columns and not filtered_df.empty:

    returns_data = filtered_df[
        ["scheme_name"] + return_columns
    ].melt(
        id_vars="scheme_name",
        var_name="Investment Period",
        value_name="Returns"
    )

    fig_returns = px.bar(
        returns_data,
        x="scheme_name",
        y="Returns",
        color="Investment Period",
        barmode="group",
        title="Fund Returns Comparison",
        template="plotly_dark"
    )

    fig_returns.update_layout(
        xaxis_title="Mutual Funds",
        yaxis_title="Returns (%)",
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_returns,
        use_container_width=True
    )

else:

    st.info("Returns data is not available.")


st.markdown("---")


# --------------------------------------------------
# CATEGORY DISTRIBUTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📂 Category Distribution</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    if "category" in filtered_df.columns and not filtered_df.empty:

        category_data = (
            filtered_df["category"]
            .value_counts()
            .reset_index()
        )

        category_data.columns = [
            "Category",
            "Count"
        ]

        fig_category = px.pie(
            category_data,
            names="Category",
            values="Count",
            hole=0.5,
            title="Funds by Category",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )


with col2:

    if "risk_level" in filtered_df.columns and not filtered_df.empty:

        risk_data = (
            filtered_df["risk_level"]
            .value_counts()
            .reset_index()
        )

        risk_data.columns = [
            "Risk Level",
            "Count"
        ]

        fig_risk = px.pie(
            risk_data,
            names="Risk Level",
            values="Count",
            hole=0.5,
            title="Risk Level Distribution",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )


st.markdown("---")


# --------------------------------------------------
# AMC ANALYSIS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🏢 AMC Analysis</div>',
    unsafe_allow_html=True
)

if "amc_name" in filtered_df.columns and not filtered_df.empty:

    amc_data = (
        filtered_df["amc_name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    amc_data.columns = [
        "AMC",
        "Number of Funds"
    ]

    fig_amc = px.bar(
        amc_data,
        x="AMC",
        y="Number of Funds",
        title="Top AMCs by Number of Funds",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_amc,
        use_container_width=True
    )


st.markdown("---")


# --------------------------------------------------
# EXPENSE RATIO ANALYSIS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">💰 Expense Ratio Analysis</div>',
    unsafe_allow_html=True
)

if (
    "expense_ratio" in filtered_df.columns
    and "scheme_name" in filtered_df.columns
    and not filtered_df.empty
):

    expense_data = filtered_df.sort_values(
        by="expense_ratio",
        ascending=True
    )

    fig_expense = px.bar(
        expense_data,
        x="scheme_name",
        y="expense_ratio",
        title="Expense Ratio Comparison",
        template="plotly_dark"
    )

    fig_expense.update_layout(
        xaxis_title="Mutual Funds",
        yaxis_title="Expense Ratio (%)",
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_expense,
        use_container_width=True
    )


st.markdown("---")


# --------------------------------------------------
# FUND SEARCH
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🔍 Search Mutual Funds</div>',
    unsafe_allow_html=True
)

search_query = st.text_input(
    "Enter Mutual Fund Name"
)

if search_query:

    search_results = filtered_df[
        filtered_df["scheme_name"]
        .astype(str)
        .str.contains(
            search_query,
            case=False,
            na=False
        )
    ]

    if not search_results.empty:

        st.dataframe(
            search_results,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning("No matching mutual fund found.")


st.markdown("---")


# --------------------------------------------------
# COMPLETE DATASET
# --------------------------------------------------

with st.expander("📋 View Complete Mutual Fund Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#aab2bf;">

    **FundIQ | Mutual Fund Investment Intelligence**

    Developed as part of an Internship Project

    <br>

    Data-driven insights for informed investment research.

    </div>
    """,
    unsafe_allow_html=True
)
