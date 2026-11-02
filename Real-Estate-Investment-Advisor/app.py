
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="EstateIQ | Investment Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR 

# =====================================================
# PREMIUM CSS DESIGN
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #0B1220;
    color: #E8EDF5;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #101B2D;
    border-right: 1px solid #243249;
}

[data-testid="stSidebar"] * {
    color: #DCE5F2;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif;
    color: #F4F6FA !important;
}

.brand {
    font-family: 'Manrope', sans-serif;
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #E7C77B;
    padding: 8px 0;
}

.brand-sub {
    color: #8291A8;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.page-heading {
    font-family: 'Manrope', sans-serif;
    font-size: 34px;
    font-weight: 800;
    color: #F4F6FA;
    letter-spacing: -1.2px;
    margin-bottom: 5px;
}

.page-description {
    color: #8D9BB0;
    font-size: 14px;
    margin-bottom: 25px;
}

.metric-card {
    background: linear-gradient(145deg, #17243A, #121D30);
    border: 1px solid #293951;
    border-radius: 14px;
    padding: 21px;
    min-height: 125px;
}

.metric-label {
    color: #98A8BC;
    font-size: 12px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.metric-value {
    color: #F4F6FA;
    font-family: 'Manrope', sans-serif;
    font-size: 27px;
    font-weight: 800;
    margin-top: 12px;
}

.metric-note {
    color: #D5B66C;
    font-size: 12px;
    margin-top: 5px;
}

.panel {
    background: #121E31;
    border: 1px solid #293951;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 15px;
}

.panel-title {
    color: #F2F5FA;
    font-family: 'Manrope', sans-serif;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 14px;
}

.gold-line {
    height: 3px;
    width: 48px;
    background: #D5B66C;
    border-radius: 5px;
    margin: 12px 0 22px 0;
}

.result-card {
    background: linear-gradient(130deg, #172C42, #142033);
    border: 1px solid #C3A45F;
    border-radius: 15px;
    padding: 25px;
    margin-top: 20px;
}

.result-label {
    color: #B4C0CF;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

.result-value {
    color: #E7C77B;
    font-family: 'Manrope', sans-serif;
    font-size: 28px;
    font-weight: 800;
    margin-top: 10px;
}

div.stButton > button,
div.stFormSubmitButton > button {
    background: #C5A45D;
    color: #111A29;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    min-height: 44px;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background: #E2C77F;
    color: #111A29;
}

.stTabs [data-baseweb="tab"] {
    color: #AAB8C9;
}

.stTabs [aria-selected="true"] {
    color: #E7C77B !important;
}

[data-testid="stMetric"] {
    background: #17243A;
    border: 1px solid #293951;
    padding: 15px;
    border-radius: 12px;
}

[data-testid="stMetricValue"] {
    color: #E7C77B;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #17243A;
    border-color: #35445A;
}

.stCaption {
    color: #8999AE;
}

hr {
    border-color: #293951;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD DATA AND MODELS
# =====================================================

@st.cache_data
def load_data():
    DATASET_URL = "https://huggingface.co/datasets/yashasvi02/real-estate-investment-data/resolve/main/real_estate_ml_dataset.csv"
    return pd.read_csv(DATASET_URL)


@st.cache_resource
def load_models():
    classifier = joblib.load(BASE_DIR / "decision_tree_classifier.pkl")
    regressor = joblib.load(BASE_DIR / "linear_regression.pkl")
    return classifier, regressor

df = load_data()
classifier, regressor = load_models()


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def metric_card(label, value, note):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def page_header(title, description):
    st.markdown(
        f'<div class="page-heading">{title}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="page-description">{description}</div>',
        unsafe_allow_html=True
    )


def chart_layout(fig, height=350):
    fig.update_layout(
        height=height,
        paper_bgcolor="#121E31",
        plot_bgcolor="#121E31",
        font=dict(color="#DCE5F2", family="DM Sans"),
        margin=dict(l=20, r=20, t=35, b=20),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#DCE5F2")
        ),
        xaxis=dict(
            gridcolor="#293951",
            zerolinecolor="#293951"
        ),
        yaxis=dict(
            gridcolor="#293951",
            zerolinecolor="#293951"
        )
    )
    return fig


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">◆ EstateIQ</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-sub">Investment Intelligence</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Property Analyzer",
            "Market Intelligence",
            "Model Analytics",
            "About Project"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("**PROJECT STATUS**")
    st.caption("Machine Learning Models")
    st.caption("Classification + Regression")
    st.caption("MLflow Experiment Tracking")

    st.divider()

    st.caption("ESTATEIQ | 2026")


# =====================================================
# EXECUTIVE OVERVIEW
# =====================================================

if page == "Executive Overview":

    page_header(
        "Executive Overview",
        "Real estate market intelligence and investment analytics platform."
    )

    total = len(df)
    average_price = df["Price_in_Lakhs"].mean()
    average_size = df["Size_in_SqFt"].mean()
    good_investments = int(df["Good_Investment"].sum())

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Total Properties",
            f"{total:,}",
            "Dataset coverage"
        )

    with c2:
        metric_card(
            "Average Property Value",
            f"₹{average_price:,.1f} L",
            "Average listing price"
        )

    with c3:
        metric_card(
            "Average Property Size",
            f"{average_size:,.0f}",
            "Square feet"
        )

    with c4:
        metric_card(
            "Potential Investments",
            f"{good_investments:,}",
            f"{good_investments / total * 100:.1f}% of dataset"
        )

    st.write("")

    left, right = st.columns([1.5, 1])

    with left:

        st.markdown(
            '<div class="panel"><div class="panel-title">Property Price Distribution</div>',
            unsafe_allow_html=True
        )

        fig = px.histogram(
            df,
            x="Price_in_Lakhs",
            nbins=45,
            color_discrete_sequence=["#C5A45D"]
        )

        fig = chart_layout(fig, 340)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.markdown(
            '<div class="panel"><div class="panel-title">Investment Classification</div>',
            unsafe_allow_html=True
        )

        labels = df["Good_Investment"].value_counts().sort_index()

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Other Properties", "Potential Investments"],
                    values=[labels.get(0, 0), labels.get(1, 0)],
                    hole=0.68,
                    marker=dict(
                        colors=["#344A66", "#C5A45D"],
                        line=dict(color="#121E31", width=3)
                    ),
                    textinfo="percent"
                )
            ]
        )

        fig = chart_layout(fig, 340)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="panel"><div class="panel-title">Average Price by Property Type</div>',
            unsafe_allow_html=True
        )

        price_type = (
            df.groupby("Property_Type")["Price_in_Lakhs"]
            .mean().sort_values(ascending=True)
        )

        fig = px.bar(
            x=price_type.values,
            y=price_type.index,
            orientation="h",
            color=price_type.values,
            color_continuous_scale=["#344A66", "#C5A45D"]
        )

        fig = chart_layout(fig, 350)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.markdown(
            '<div class="panel"><div class="panel-title">Average Price by BHK</div>',
            unsafe_allow_html=True
        )

        bhk = df.groupby("BHK")["Price_in_Lakhs"].mean()

        fig = px.line(
            x=bhk.index,
            y=bhk.values,
            markers=True
        )

        fig.update_traces(
            line=dict(color="#C5A45D", width=3),
            marker=dict(size=9)
        )

        fig = chart_layout(fig, 350)
        fig.update_layout(
            xaxis_title="BHK",
            yaxis_title="Average Price (Lakhs)"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# PROPERTY ANALYZER
# =====================================================

elif page == "Property Analyzer":

    page_header(
        "Property Analyzer",
        "Evaluate property investment suitability and estimate its future value."
    )

    st.markdown(
        '<div class="panel"><div class="panel-title">PROPERTY CONFIGURATION</div>',
        unsafe_allow_html=True
    )

    input_values = {}

    input_features = [
        col for col in df.columns
        if col not in [
            "ID",
            "Good_Investment",
            "Future_Price_5_Years"
        ]
    ]

    with st.form("property_analysis_form"):

        st.markdown("#### Property Details")

        columns = st.columns(3)

        for i, col in enumerate(input_features):

            with columns[i % 3]:

                if pd.api.types.is_numeric_dtype(df[col]):

                    default = float(df[col].median())
                    minimum = float(df[col].min())
                    maximum = float(df[col].max())

                    if minimum == maximum:
                        minimum -= 1
                        maximum += 1

                    input_values[col] = st.number_input(
                        col.replace("_", " "),
                        min_value=minimum,
                        max_value=maximum,
                        value=min(max(default, minimum), maximum)
                    )

                else:

                    options = (
                        df[col].dropna().astype(str)
                        .value_counts().head(30).index.tolist()
                    )

                    input_values[col] = st.selectbox(
                        col.replace("_", " "),
                        options
                    )

        submitted = st.form_submit_button(
            "GENERATE INVESTMENT ANALYSIS",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:

        input_df = pd.DataFrame([input_values])

        classifier_input = input_df[
            classifier.feature_names_in_
        ]

        regressor_input = input_df[
            regressor.feature_names_in_
        ]

        prediction = classifier.predict(classifier_input)[0]
        future_price = float(
            regressor.predict(regressor_input)[0]
        )

        st.markdown("### Investment Assessment")

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                '<div class="result-card"><div class="result-label">Investment Screening Result</div>',
                unsafe_allow_html=True
            )

            if prediction == 1:
                st.markdown(
                    '<div class="result-value">Potentially Suitable</div>',
                    unsafe_allow_html=True
                )
                st.success("Property meets the model's screening rule.")
            else:
                st.markdown(
                    '<div class="result-value">Not Qualified</div>',
                    unsafe_allow_html=True
                )
                st.warning("Property does not meet the model's screening rule.")

            st.markdown("</div>", unsafe_allow_html=True)

        with c2:

            st.markdown(
                '<div class="result-card"><div class="result-label">Estimated Value After 5 Years</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="result-value">₹ {future_price:,.2f} Lakhs</div>',
                unsafe_allow_html=True
            )

            st.caption("Based on the assumed annual appreciation rate of 8%.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.info(
            "These are model-based estimates, not financial advice. "
            "Investment suitability uses a rule-generated dataset label, "
            "and future value uses an assumed 8% growth formula."
        )


# =====================================================
# MARKET INTELLIGENCE
# =====================================================

elif page == "Market Intelligence":

    page_header(
        "Market Intelligence",
        "Explore regional pricing patterns and property market characteristics."
    )

    state_data = (
        df.groupby("State")["Price_in_Lakhs"]
        .mean().sort_values(ascending=False).head(12)
    )

    city_data = (
        df.groupby("City")["Price_in_Lakhs"]
        .mean().sort_values(ascending=False).head(12)
    )

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            '<div class="panel"><div class="panel-title">Top States by Average Price</div>',
            unsafe_allow_html=True
        )

        fig = px.bar(
            x=state_data.values,
            y=state_data.index,
            orientation="h",
            color=state_data.values,
            color_continuous_scale=["#344A66", "#C5A45D"]
        )

        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig = chart_layout(fig, 390)
        fig.update_layout(coloraxis_showscale=False)

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:

        st.markdown(
            '<div class="panel"><div class="panel-title">Top Cities by Average Price</div>',
            unsafe_allow_html=True
        )

        fig = px.bar(
            x=city_data.values,
            y=city_data.index,
            orientation="h",
            color=city_data.values,
            color_continuous_scale=["#344A66", "#C5A45D"]
        )

        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig = chart_layout(fig, 390)
        fig.update_layout(coloraxis_showscale=False)

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            '<div class="panel"><div class="panel-title">Price by Furnishing Status</div>',
            unsafe_allow_html=True
        )

        furnishing = (
            df.groupby("Furnished_Status")["Price_in_Lakhs"]
            .mean()
        )

        fig = px.bar(
            x=furnishing.index,
            y=furnishing.values,
            color=furnishing.values,
            color_continuous_scale=["#344A66", "#C5A45D"]
        )

        fig = chart_layout(fig, 330)
        fig.update_layout(coloraxis_showscale=False)

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:

        st.markdown(
            '<div class="panel"><div class="panel-title">Property Size vs Price</div>',
            unsafe_allow_html=True
        )

        sample = df.sample(
            min(3000, len(df)),
            random_state=42
        )

        fig = px.scatter(
            sample,
            x="Size_in_SqFt",
            y="Price_in_Lakhs",
            color="Property_Type",
            opacity=0.6
        )

        fig = chart_layout(fig, 330)

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# MODEL ANALYTICS
# =====================================================

elif page == "Model Analytics":

    page_header(
        "Model Analytics",
        "Machine learning evaluation, model selection and predictive performance."
    )

    st.markdown("### Classification Model")

    classification = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall", "F1 Score"],
        "Score": [0.67566, 0.36024, 0.96368, 0.52444]
    })

    c1, c2 = st.columns([1, 1.3])

    with c1:
        st.dataframe(
            classification,
            hide_index=True,
            use_container_width=True
        )

    with c2:

        fig = px.bar(
            classification,
            x="Metric",
            y="Score",
            color="Score",
            color_continuous_scale=["#344A66", "#C5A45D"],
            range_y=[0, 1]
        )

        fig = chart_layout(fig, 310)
        fig.update_layout(coloraxis_showscale=False)

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### Regression Model")

    regression = pd.DataFrame({
        "Metric": ["MAE", "RMSE", "R² Score"],
        "Value": [0.0008004, 0.0010213, 0.999999999975]
    })

    st.dataframe(
        regression,
        hide_index=True,
        use_container_width=True
    )

    st.info(
        "Important methodology limitation: The regression target was "
        "generated using an assumed 8% annual appreciation formula. "
        "Therefore, the very high R² reflects the formula-based target, "
        "not verified real-world forecasting accuracy."
    )


# =====================================================
# ABOUT PROJECT
# =====================================================

elif page == "About Project":

    page_header(
        "About EstateIQ",
        "A machine learning-based real estate investment analysis project."
    )

    st.markdown("""
    <div class="panel">
        <div class="panel-title">PROJECT OVERVIEW</div>
        EstateIQ is a real estate analytics platform designed to explore
        housing data, assess investment suitability using a classification
        model and estimate future property value using regression.
        <div class="gold-line"></div>
        <div class="panel-title">PROJECT OBJECTIVES</div>
        • Analyze housing prices and property characteristics.<br>
        • Identify potentially suitable investment properties.<br>
        • Estimate property value after five years.<br>
        • Present market insights through interactive visualizations.<br>
        • Track machine learning experiments using MLflow.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Technology Stack")

    tech = st.columns(5)

    technologies = [
        ("Python", "Data Processing"),
        ("Pandas", "Data Analysis"),
        ("Scikit-learn", "Machine Learning"),
        ("MLflow", "Experiment Tracking"),
        ("Streamlit", "Web Application")
    ]

    for col, (name, purpose) in zip(tech, technologies):
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value" style="font-size:17px">{name}</div><div class="metric-note">{purpose}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown("### Dataset Information")
    st.write(f"Total records: {len(df):,}")
    st.write(f"Total columns: {df.shape[1]}")
    st.write("Dataset: India Housing Prices")


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="text-align:center; padding:15px; color:#8291A8;">
    <span style="color:#D5B66C; font-weight:700;">◆ ESTATEIQ</span>
    &nbsp; | &nbsp; Real Estate Investment Intelligence
    <br>
    <span style="font-size:11px;">
    Machine Learning • Data Analytics • Predictive Modelling
    </span>
</div>
""", unsafe_allow_html=True)
