
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="🚕",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color: #F5F7FA;
    color: #263445;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0;
}

section[data-testid="stSidebar"] > div {
    background-color: #FFFFFF !important;
}

section[data-testid="stSidebar"] * {
    color: #263445 !important;
    text-shadow: none !important;
    opacity: 1 !important;
}

/* SIDEBAR TITLE */
section[data-testid="stSidebar"] h1 {
    color: #087E8B !important;
    font-size: 25px !important;
}

/* SIDEBAR RADIO OPTIONS */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 7px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: #F3F6F9 !important;
    border: 1px solid #E5EAF0 !important;
    border-radius: 8px !important;
    padding: 9px 12px !important;
    margin-bottom: 5px !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color: #263445 !important;
    font-weight: 500 !important;
}

/* SELECTED OPTION */
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background-color: #DDF2F1 !important;
    border: 1px solid #087E8B !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color: #087E8B !important;
    font-weight: 700 !important;
}

/* HEADINGS */
h1, h2, h3 {
    color: #19344D !important;
}

/* KPI CARDS */
.metric-card {
    background-color: #FFFFFF;
    border: 1px solid #E5EAF0;
    border-left: 4px solid #087E8B;
    border-radius: 12px;
    padding: 18px;
    min-height: 105px;
    box-shadow: 0 2px 8px rgba(25,52,77,0.04);
}

.metric-label {
    color: #64748B;
    font-size: 14px;
    margin-bottom: 10px;
}

.metric-value {
    color: #087E8B;
    font-size: 25px;
    font-weight: 700;
}

/* BUTTONS */
.stButton button {
    background-color: #087E8B;
    color: white;
    border-radius: 8px;
    border: none;
}

</style>
""", unsafe_allow_html=True)


# LOAD DATA
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "OLA_Cleaned_Data.csv"
    data = pd.read_csv(file_path)

    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    numeric_columns = [
        "Booking_Value",
        "Ride_Distance",
        "Driver_Ratings",
        "Customer_Rating",
        "V_TAT",
        "C_TAT"
    ]

    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    return data


df = load_data()


# COMMON CALCULATIONS
success = df[df["Booking_Status"] == "Success"]

cancelled = df[
    df["Booking_Status"].isin(
        ["Canceled by Customer", "Canceled by Driver"]
    )
]

customer_cancelled = (
    df["Booking_Status"] == "Canceled by Customer"
).sum()

driver_cancelled = (
    df["Booking_Status"] == "Canceled by Driver"
).sum()

total_revenue = success["Booking_Value"].sum()
total_distance = df["Ride_Distance"].sum()


# KPI FUNCTION
def metric_card(label, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def show_kpis(items):
    cols = st.columns(len(items))

    for col, (label, value) in zip(cols, items):
        with col:
            metric_card(label, value)


# SIDEBAR
st.sidebar.title("🚕 OLA INSIGHTS")
st.sidebar.caption("RIDE ANALYTICS PLATFORM")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "WORKSPACE",
    [
        "Executive Overview",
        "Vehicle Analysis",
        "Revenue Analysis",
        "Cancellation Analysis",
        "Ratings Analysis",
        "About Project"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("JULY 2024 | RIDE ANALYTICS")


# 1. EXECUTIVE OVERVIEW
if page == "Executive Overview":

    st.title("Executive Overview")
    st.write("Overall ride booking performance and business insights.")

    show_kpis([
        ("Total Bookings", f"{len(df):,}"),
        ("Successful Rides", f"{len(success):,}"),
        ("Cancelled Rides", f"{len(cancelled):,}"),
        ("Total Revenue", f"₹{total_revenue:,.0f}")
    ])

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Booking Status Breakdown")

        status = df["Booking_Status"].value_counts().reset_index()
        status.columns = ["Status", "Bookings"]

        fig = px.pie(
            status,
            names="Status",
            values="Bookings",
            hole=0.45
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Ride Volume Over Time")

        daily = (
            df.groupby("Date")["Booking_ID"]
            .count()
            .reset_index()
        )

        fig = px.line(
            daily,
            x="Date",
            y="Booking_ID",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)


# 2. VEHICLE ANALYSIS
elif page == "Vehicle Analysis":

    st.title("Vehicle Analysis")
    st.write("Vehicle-wise booking and distance performance.")

    vehicle = df.groupby("Vehicle_Type").agg(
        Total_Booking_Value=("Booking_Value", "sum"),
        Average_Distance=("Ride_Distance", "mean"),
        Total_Distance=("Ride_Distance", "sum"),
        Total_Bookings=("Booking_ID", "count")
    ).reset_index()

    success_vehicle = (
        success.groupby("Vehicle_Type")["Booking_Value"]
        .sum()
        .reset_index(name="Success_Booking_Value")
    )

    vehicle = vehicle.merge(
        success_vehicle,
        on="Vehicle_Type",
        how="left"
    )

    vehicle["Success_Booking_Value"] = (
        vehicle["Success_Booking_Value"].fillna(0)
    )

    show_kpis([
        ("Vehicle Types", vehicle["Vehicle_Type"].nunique()),
        ("Total Bookings", f"{len(df):,}"),
        ("Total Distance", f"{total_distance:,.0f} km")
    ])

    st.subheader("Vehicle Performance Table")

    st.dataframe(
        vehicle.round(2),
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Booking Value by Vehicle")

        fig = px.bar(
            vehicle,
            x="Vehicle_Type",
            y="Total_Booking_Value",
            color="Vehicle_Type"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Successful Booking Value")

        fig = px.bar(
            vehicle,
            x="Vehicle_Type",
            y="Success_Booking_Value",
            color="Vehicle_Type"
        )

        st.plotly_chart(fig, use_container_width=True)


# 3. REVENUE ANALYSIS
elif page == "Revenue Analysis":

    st.title("Revenue Analysis")
    st.write("Revenue trends and payment method analysis.")

    show_kpis([
        ("Total Revenue", f"₹{total_revenue:,.0f}"),
        ("Average Booking Value", f"₹{success['Booking_Value'].mean():,.2f}"),
        ("Total Ride Distance", f"{total_distance:,.0f} km"),
        ("Average Ride Distance", f"{df['Ride_Distance'].mean():,.2f} km")
    ])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Payment Method")

        payment = (
            success.groupby("Payment_Method")["Booking_Value"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            payment,
            x="Payment_Method",
            y="Booking_Value",
            color="Payment_Method"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Revenue by Date")

        revenue_date = (
            success.groupby("Date")["Booking_Value"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            revenue_date,
            x="Date",
            y="Booking_Value",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)


# 4. CANCELLATION ANALYSIS
elif page == "Cancellation Analysis":

    st.title("Cancellation Analysis")
    st.write("Customer and driver cancellation patterns.")

    show_kpis([
        ("Customer Cancellations", f"{customer_cancelled:,}"),
        ("Driver Cancellations", f"{driver_cancelled:,}"),
        ("Total Cancelled Rides", f"{len(cancelled):,}")
    ])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Incomplete Rides by Reason")

        reason = (
            df["Incomplete_Rides_Reason"]
            .dropna()
            .value_counts()
            .reset_index()
        )

        reason.columns = ["Reason", "Count"]

        fig = px.bar(
            reason,
            x="Count",
            y="Reason",
            orientation="h"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Cancelled Rides by Vehicle")

        cancel_vehicle = (
            cancelled.groupby("Vehicle_Type")["Booking_ID"]
            .count()
            .reset_index(name="Cancelled Rides")
        )

        fig = px.bar(
            cancel_vehicle,
            x="Vehicle_Type",
            y="Cancelled Rides",
            color="Vehicle_Type"
        )

        st.plotly_chart(fig, use_container_width=True)


# 5. RATINGS ANALYSIS
elif page == "Ratings Analysis":

    st.title("Ratings Analysis")
    st.write("Driver and customer satisfaction insights.")

    show_kpis([
        ("Average Driver Rating", f"{df['Driver_Ratings'].mean():.2f} / 5"),
        ("Average Customer Rating", f"{df['Customer_Rating'].mean():.2f} / 5"),
        ("Driver Rated Rides", f"{df['Driver_Ratings'].count():,}"),
        ("Customer Rated Rides", f"{df['Customer_Rating'].count():,}")
    ])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Average Driver Rating by Vehicle")

        driver_rating = (
            df.groupby("Vehicle_Type")["Driver_Ratings"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            driver_rating,
            x="Vehicle_Type",
            y="Driver_Ratings",
            color="Vehicle_Type"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Average Customer Rating by Vehicle")

        customer_rating = (
            df.groupby("Vehicle_Type")["Customer_Rating"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            customer_rating,
            x="Vehicle_Type",
            y="Customer_Rating",
            color="Vehicle_Type"
        )

        st.plotly_chart(fig, use_container_width=True)


# 6. ABOUT PROJECT
elif page == "About Project":

    st.title("About OLA Ride Insights")

    st.write(
        "OLA Ride Insights is a data analytics project that "
        "analyzes ride bookings, revenue, vehicle performance, "
        "cancellations and customer satisfaction."
    )

    st.markdown("---")

    st.subheader("Project Objectives")

    st.markdown("""
    - Analyze overall ride booking performance.
    - Compare different vehicle categories.
    - Understand revenue and payment trends.
    - Identify customer and driver cancellation patterns.
    - Evaluate customer and driver ratings.
    """)

    st.subheader("Tools & Technologies")

    st.markdown("""
    - Python
    - SQL Server
    - Power BI
    - Streamlit
    - Pandas
    - Plotly
    """)

    col1, col2 = st.columns(2)

    with col1:
        metric_card("Total Records", f"{len(df):,}")

    with col2:
        metric_card("Total Columns", f"{len(df.columns)}")

    st.subheader("Dataset Preview")
    st.dataframe(
        df.head(10),
        use_container_width=True
    )


# FOOTER
st.markdown("---")
st.caption("OLA Ride Insights | Data Analytics Project")
