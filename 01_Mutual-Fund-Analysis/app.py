
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FundIQ | Mutual Fund Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #0B1120;
        color: #E5E7EB;
    }

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #263247;
    }

    [data-testid="stSidebar"] * {
        color: #E5E7EB;
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -1px;
        margin-bottom: 0;
    }

    .subtitle {
        color: #94A3B8;
        font-size: 14px;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    .metric-card {
        background: linear-gradient(135deg, #172554, #111827);
        border: 1px solid #263B63;
        border-radius: 14px;
        padding: 20px;
        min-height: 120px;
    }

    .metric-label {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 10px;
    }

    .metric-value {
        color: #F8FAFC;
        font-size: 27px;
        font-weight: 800;
    }

    .metric-note {
        color: #60A5FA;
        font-size: 12px;
        margin-top: 8px;
    }

    .section-title {
        color: #F8FAFC;
        font-size: 20px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 12px;
    }

    .info-card {
        background: #111827;
        border: 1px solid #263247;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 10px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #263247;
        border-radius: 10px;
    }

    div.stButton > button {
        background: #2563EB;
        color: white;
        border: none;
        border-radius: 8px;
    }

    div.stButton > button:hover {
        background: #1D4ED8;
        color: white;
    }

    hr {
        border-color: #263247;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

DATA_PATH = (
    Path(__file__).parent
    / "Top_30_Mutual_Funds.xlsx"
)


@st.cache_data
def load_data(file_path):
    data = pd.read_excel(file_path)

    data.columns = data.columns.str.strip().str.lower()

    required_columns = [
        "rank",
        "scheme_name",
        "category",
        "sub_category",
        "amc_name",
        "risk_level",
        "returns_1yr",
        "returns_3yr",
        "returns_5yr",
        "expense_ratio",
        "fund_size_cr",
        "fund_age_yr",
        "final_score",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in Excel file: {missing_columns}"
        )

    return data


if not DATA_PATH.exists():
    st.error(
        "Dataset file not found. Please place "
        "Top_30_Mutual_Funds.xlsx in the project folder."
    )
    st.stop()


try:
    df = load_data(DATA_PATH)

except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()


# --------------------------------------------------
# DATA PREPARATION
# --------------------------------------------------

numeric_columns = [
    "rank",
    "risk_level",
    "returns_1yr",
    "returns_3yr",
    "returns_5yr",
    "expense_ratio",
    "fund_size_cr",
    "fund_age_yr",
    "final_score",
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce",
    )

df = df.dropna(subset=["scheme_name"])

df["scheme_name"] = df["scheme_name"].astype(str)

df = df.sort_values("rank", ascending=True)

df["risk_label"] = df["risk_level"].apply(
    lambda value: (
        "High"
        if value >= 6
        else "Moderate"
        if value >= 4
        else "Low"
    )
    if pd.notna(value)
    else "Unknown"
)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def format_number(value):
    if pd.isna(value):
        return "N/A"

    return f"{value:,.0f}"


def format_percent(value):
    if pd.isna(value):
        return "N/A"

    return f"{value:.2f}%"


def metric_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(
            color="#CBD5E1",
            family="Inter",
        ),
        margin=dict(
            l=20,
            r=20,
            t=45,
            b=20,
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
        ),
    )

    fig.update_xaxes(
        gridcolor="#263247",
        zerolinecolor="#263247",
    )

    fig.update_yaxes(
        gridcolor="#263247",
        zerolinecolor="#263247",
    )

    return fig


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 10px 0 20px 0;">
            <div style="
                font-size: 28px;
                font-weight: 800;
                color: #60A5FA;
            ">
                FundIQ
            </div>

            <div style="
                font-size: 11px;
                letter-spacing: 2px;
                color: #94A3B8;
            ">
                MUTUAL FUND INTELLIGENCE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Fund Explorer",
            "Performance Analysis",
            "Risk Analysis",
            "Top 30 Rankings",
            "About Project",
        ],
    )

    st.markdown("---")

    st.markdown("### Data Filters")

    categories = sorted(
        df["category"].dropna().unique().tolist()
    )

    selected_categories = st.multiselect(
        "Fund Category",
        categories,
        default=categories,
    )

    amcs = sorted(
        df["amc_name"].dropna().unique().tolist()
    )

    selected_amcs = st.multiselect(
        "Asset Management Company",
        amcs,
        default=amcs,
    )

    filtered_df = df[
        df["category"].isin(selected_categories)
        & df["amc_name"].isin(selected_amcs)
    ].copy()

    st.markdown("---")

    st.caption(
        "FundIQ | Mutual Fund Analytics"
    )

    st.caption(
        "Historical data analysis. "
        "Not investment advice."
    )


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.markdown(
    f"""
    <div class="main-title">
        {page}
    </div>

    <div class="subtitle">
        Mutual Fund Analytics Platform
        &nbsp; | &nbsp;
        Explore performance, risk and rankings
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# OVERVIEW PAGE
# --------------------------------------------------

if page == "Overview":

    st.markdown(
        '<div class="section-title">Portfolio Overview</div>',
        unsafe_allow_html=True,
    )

    total_funds = len(filtered_df)

    total_categories = (
        filtered_df["category"].nunique()
    )

    avg_1yr = filtered_df["returns_1yr"].mean()

    avg_3yr = filtered_df["returns_3yr"].mean()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "Total Funds",
            format_number(total_funds),
            "Selected fund universe",
        )

    with col2:
        metric_card(
            "Categories",
            format_number(total_categories),
            "Fund classification",
        )

    with col3:
        metric_card(
            "Average 1Y Return",
            format_percent(avg_1yr),
            "Historical return",
        )

    with col4:
        metric_card(
            "Average 3Y Return",
            format_percent(avg_3yr),
            "Historical return",
        )

    st.markdown("---")

    if filtered_df.empty:

        st.warning(
            "No funds match the selected filters."
        )

    else:

        left, right = st.columns(2)

        with left:

            st.markdown(
                "### Category Distribution"
            )

            category_data = (
                filtered_df["category"]
                .value_counts()
                .reset_index()
            )

            category_data.columns = [
                "Category",
                "Fund Count",
            ]

            fig = px.pie(
                category_data,
                names="Category",
                values="Fund Count",
                hole=0.55,
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

        with right:

            st.markdown(
                "### Top Funds by 3-Year Return"
            )

            top_returns = (
                filtered_df
                .dropna(subset=["returns_3yr"])
                .nlargest(10, "returns_3yr")
                .sort_values("returns_3yr")
            )

            fig = px.bar(
                top_returns,
                x="returns_3yr",
                y="scheme_name",
                orientation="h",
                labels={
                    "returns_3yr": "3-Year Return (%)",
                    "scheme_name": "Fund",
                },
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

        st.markdown(
            "### Highest Ranked Funds"
        )

        display_columns = [
            "rank",
            "scheme_name",
            "category",
            "returns_3yr",
            "returns_5yr",
            "final_score",
        ]

        st.dataframe(
            filtered_df[display_columns].head(10),
            use_container_width=True,
            hide_index=True,
        )


# --------------------------------------------------
# FUND EXPLORER
# --------------------------------------------------

elif page == "Fund Explorer":

    st.markdown(
        "### Explore Mutual Funds"
    )

    search_text = st.text_input(
        "Search by fund name",
        placeholder="Enter mutual fund name...",
    )

    explorer_df = filtered_df.copy()

    if search_text:

        explorer_df = explorer_df[
            explorer_df["scheme_name"]
            .str.contains(
                search_text,
                case=False,
                na=False,
            )
        ]

    st.write(
        f"Showing {len(explorer_df)} funds"
    )

    st.dataframe(
        explorer_df,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        label="Download Filtered Data",
        data=explorer_df.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="filtered_mutual_funds.csv",
        mime="text/csv",
    )


# --------------------------------------------------
# PERFORMANCE ANALYSIS
# --------------------------------------------------

elif page == "Performance Analysis":

    st.markdown(
        "### Historical Performance Analysis"
    )

    if filtered_df.empty:

        st.warning(
            "No funds match the selected filters."
        )

    else:

        performance_metric = st.selectbox(
            "Select Return Period",
            [
                "returns_1yr",
                "returns_3yr",
                "returns_5yr",
            ],
            format_func=lambda value: {
                "returns_1yr": "1-Year Return",
                "returns_3yr": "3-Year Return",
                "returns_5yr": "5-Year Return",
            }[value],
        )

        performance_data = (
            filtered_df
            .dropna(subset=[performance_metric])
            .nlargest(15, performance_metric)
            .sort_values(performance_metric)
        )

        fig = px.bar(
            performance_data,
            x=performance_metric,
            y="scheme_name",
            orientation="h",
            color="category",
            labels={
                performance_metric: "Return (%)",
                "scheme_name": "Fund Name",
            },
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
        )

        st.markdown(
            "### Return Comparison"
        )

        comparison_df = filtered_df[
            [
                "scheme_name",
                "returns_1yr",
                "returns_3yr",
                "returns_5yr",
            ]
        ].copy()

        comparison_df = comparison_df.melt(
            id_vars="scheme_name",
            value_vars=[
                "returns_1yr",
                "returns_3yr",
                "returns_5yr",
            ],
            var_name="Period",
            value_name="Return",
        )

        fig = px.box(
            comparison_df,
            x="Period",
            y="Return",
            color="Period",
            points="all",
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
        )


# --------------------------------------------------
# RISK ANALYSIS
# --------------------------------------------------

elif page == "Risk Analysis":

    st.markdown(
        "### Risk and Return Analysis"
    )

    risk_data = filtered_df.dropna(
        subset=[
            "risk_level",
            "returns_3yr",
        ]
    )

    if risk_data.empty:

        st.warning(
            "No suitable data available for risk analysis."
        )

    else:

        fig = px.scatter(
            risk_data,
            x="risk_level",
            y="returns_3yr",
            color="category",
            size="fund_size_cr",
            hover_name="scheme_name",
            hover_data=[
                "returns_5yr",
                "expense_ratio",
                "final_score",
            ],
            labels={
                "risk_level": "Risk Level",
                "returns_3yr": "3-Year Return (%)",
                "fund_size_cr": "Fund Size (Cr)",
            },
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
        )

        left, right = st.columns(2)

        with left:

            st.markdown(
                "### Risk Level Distribution"
            )

            risk_counts = (
                risk_data["risk_label"]
                .value_counts()
                .reset_index()
            )

            risk_counts.columns = [
                "Risk Level",
                "Fund Count",
            ]

            fig = px.bar(
                risk_counts,
                x="Risk Level",
                y="Fund Count",
                color="Risk Level",
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

        with right:

            st.markdown(
                "### Expense Ratio Comparison"
            )

            expense_data = (
                risk_data
                .dropna(subset=["expense_ratio"])
                .nsmallest(10, "expense_ratio")
            )

            fig = px.bar(
                expense_data,
                x="expense_ratio",
                y="scheme_name",
                orientation="h",
                labels={
                    "expense_ratio": "Expense Ratio (%)",
                    "scheme_name": "Fund",
                },
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )

        st.info(
            "Risk level is based on the risk_level "
            "column available in the dataset. "
            "This is a descriptive analysis, not "
            "a personalized investment recommendation."
        )


# --------------------------------------------------
# TOP 30 RANKINGS
# --------------------------------------------------

elif page == "Top 30 Rankings":

    st.markdown(
        "### Fund Ranking & Scoring"
    )

    ranking_df = (
        filtered_df
        .sort_values(
            "final_score",
            ascending=False,
        )
        .copy()
    )

    st.dataframe(
        ranking_df[
            [
                "rank",
                "scheme_name",
                "category",
                "risk_level",
                "returns_1yr",
                "returns_3yr",
                "returns_5yr",
                "final_score",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        label="Download Ranking Data",
        data=ranking_df.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="mutual_fund_rankings.csv",
        mime="text/csv",
    )

    st.caption(
        "Rankings are based on the existing "
        "final_score values in the dataset."
    )


# --------------------------------------------------
# ABOUT PROJECT
# --------------------------------------------------

elif page == "About Project":

    st.markdown(
        "### About FundIQ"
    )

    st.markdown(
        """
        FundIQ is a Mutual Fund Analysis project
        designed to explore historical fund performance,
        risk indicators, categories and rankings.

        The application transforms a prepared mutual
        fund dataset into an interactive analytics
        dashboard.
        """
    )

    st.markdown(
        "### Project Objectives"
    )

    st.markdown(
        """
        - Analyze historical mutual fund returns.
        - Compare funds across different categories.
        - Explore risk and return characteristics.
        - Understand AMC-wise fund distribution.
        - Present the existing Top 30 fund ranking.
        """
    )

    st.markdown(
        "### Technology Stack"
    )

    st.markdown(
        """
        - Python
        - Pandas
        - Streamlit
        - Plotly
        - Excel
        """
    )

    st.markdown(
        "### Dataset Information"
    )

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.metric(
            "Dataset Records",
            len(df),
        )

    with info_col2:

        st.metric(
            "Dataset Columns",
            len(df.columns),
        )

    st.markdown(
        "### Important Disclaimer"
    )

    st.warning(
        "This application is developed for educational "
        "and analytical purposes. Historical mutual fund "
        "returns do not guarantee future performance. "
        "This application does not provide personalized "
        "investment advice."
    )
