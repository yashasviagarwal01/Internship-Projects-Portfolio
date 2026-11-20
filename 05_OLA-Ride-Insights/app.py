
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="🚕",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background-color: #F4F7FB;
}

[data-testid="stSidebar"] {
    background-color: #E8EFF5;
}

[data-testid="stSidebar"] h1 {
    color: #087E8B;
}

h1, h2, h3 {
    color: #17324D;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
    border-left: 4px solid #087E8B;
    margin-bottom: 12px;
}

.metric-label {
    color: #64748B;
    font-size: 14px;
}

.metric-value {
    color: #17324D;
    font-size: 25px;
    font-weight: 700;
}

div[data-testid="stDataFrame"] {
    background: white;
    border-radius: 10px;
}

.stButton button {
    background-color: #087E8B;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD DATA ----------------
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


# ---------------- COMMON CALCULATIONS ----------------
total_bookings = len(df)

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
avg_booking_value = success["Booking_Value"].mean()
total_distance = df["Ride_Distance"].sum()
avg_distance = df["Ride_Distance"].mean()


# ---------------- KPI CARD FUNCTION ----------------
def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_kpis(items):
    cols = st.columns(len(items))

    for col, (label, value) in zip(cols, items):
        with col:
            metric_card(label, value)


# ---------------- SIDEBAR ----------------
st.sidebar.title("🚕 OLA INSIGHTS")
st.sidebar.caption("RIDE ANALYTICS PLATFORM")

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
st.sidebar.caption("OLA RIDE INSIGHTS | JULY 2024")


# ==================================================
# 1. EXECUTIVE OVERVIEW
# ==================================================
if page == "Executive Overview":

    st.title("Executive Overview")
    st.write("A complete overview of OLA ride booking performance.")

    show_kpis([
        ("Total Bookings", f"{total_bookings:,}"),
        ("Successful Rides", f"{len(success):,}"),
        ("Cancelled Rides", f"{len(cancelled):,}"),
        ("Total Revenue", f"₹{total_revenue:,.0f}")
    ])

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Booking Status Breakdown")

        status_data = df["Booking_Status"].value_counts().reset_index()
        status_data.columns = ["Booking Status", "Bookings"]

        fig = px.pie(
            status_data,
            names="Booking Status",
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
            .rename(columns={"Booking_ID": "Bookings"})
        )

        fig = px.line(
            daily,
            x="Date",
            y="Bookings",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)


# ==================================================
# 2. VEHICLE ANALYSIS
# ==================================================
elif page == "Vehicle Analysis":

    st.title("Vehicle Analysis")
    st.write("Analyze booking value and ride distance across vehicle types.")

    vehicle_data = df.groupby("Vehicle_Type").agg(
        Total_Booking_Value=("Booking_Value", "sum"),
        Average_Distance=("Ride_Distance", "mean"),
        Total_Distance=("Ride_Distance", "sum"),
        Total_Bookings=("Booking_ID", "count")
    ).reset_index()

    successful_value = (
        success.groupby("Vehicle_Type")["Booking_Value"]
        .sum()
        .reset_index(name="Success_Booking_Value")
    )

    vehicle_data = vehicle_data.merge(
        successful_value,
        on="Vehicle_Type",
        how="left"
    )

    vehicle_data["Success_Booking_Value"] = (
        vehicle_data["Success_Booking_Value"].fillna(0)
    )

    show_kpis([
        ("Total Vehicles", vehicle_data["Vehicle_Type"].nunique()),
        ("Total Bookings", f"{total_bookings:,}"),
        ("Total Distance", f"{total_distance:,.0f} km")
    ])

    st.subheader("Vehicle Performance Table")

    st.dataframe(
        vehicle_data.round(2),
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Total Booking Value by Vehicle")

        fig = px.bar(
            vehicle_data,
            x="Vehicle_Type",
            y="Total_Booking_Value",
            color="Vehicle_Type"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Successful Booking Value by Vehicle")

        fig = px.bar(
            vehicle_data,
            x="Vehicle_Type",
            y="Success_Booking_Value",
            color="Vehicle_Type"
        )
        st.plotly_chart(fig, use_container_width=True)


# ==================================================
# 3. REVENUE ANALYSIS
# ==================================================
elif page == "Revenue Analysis":

    st.title("Revenue Analysis")
    st.write("Explore revenue trends and payment preferences.")

    show_kpis([
        ("Total Revenue", f"₹{total_revenue:,.0f}"),
        ("Average Booking Value", f"₹{avg_booking_value:,.2f}"),
        ("Total Ride Distance", f"{total_distance:,.0f} km"),
        ("Average Ride Distance", f"{avg_distance:,.2f} km")
    ])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Payment Method")

        payment_data = (
            success.groupby("Payment_Method")["Booking_Value"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            payment_data,
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


# ==================================================
# 4. CANCELLATION ANALYSIS
# ==================================================
elif page == "Cancellation Analysis":

    st.title("Cancellation Analysis")
    st.write("Understand customer and driver cancellation patterns.")

    show_kpis([
        ("Customer Cancellations", f"{customer_cancelled:,}"),
        ("Driver Cancellations", f"{driver_cancelled:,}"),
        ("Total Cancelled Rides", f"{len(cancelled):,}")
    ])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Incomplete Rides by Reason")

        if "Incomplete_Rides_Reason" in df.columns:
            reason_data = (
                df["Incomplete_Rides_Reason"]
                .dropna()
                .value_counts()
                .reset_index()
            )
            reason_data.columns = ["Reason", "Count"]

            fig = px.bar(
                reason_data,
                x="Count",
                y="Reason",
                orientation="h"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Incomplete ride reason data is unavailable.")

    with col2:
        st.subheader("Cancelled Rides by Vehicle Type")

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


# ==================================================
# 5. RATINGS ANALYSIS
# ==================================================
elif page == "Ratings Analysis":

    st.title("Ratings Analysis")
    st.write("Understand driver and customer satisfaction.")

    avg_driver_rating = df["Driver_Ratings"].mean()
    avg_customer_rating = df["Customer_Rating"].mean()

    driver_rated = df["Driver_Ratings"].count()
    customer_rated = df["Customer_Rating"].count()

    show_kpis([
        ("Average Driver Rating", f"{avg_driver_rating:.2f} / 5"),
        ("Average Customer Rating", f"{avg_customer_rating:.2f} / 5"),
        ("Driver Rated Rides", f"{driver_rated:,}"),
        ("Customer Rated Rides", f"{customer_rated:,}")
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


# ==================================================
# 6. ABOUT PROJECT
# ==================================================
elif page == "About Project":

    st.title("About OLA Ride Insights")

    st.write(
        "OLA Ride Insights is a data analytics project designed "
        "to understand ride booking performance, revenue, "
        "vehicle usage, cancellations and customer satisfaction."
    )

    st.markdown("---")

    st.subheader("Project Objectives")

    st.markdown("""
    - Analyze overall ride booking performance.
    - Identify the performance of different vehicle types.
    - Understand revenue trends and payment methods.
    - Analyze customer and driver cancellations.
    - Evaluate driver and customer ratings.
    """)

    st.subheader("Tools & Technologies")

    st.markdown("""
    - **Python:** Data cleaning and analysis
    - **SQL Server:** Database management and SQL queries
    - **Power BI:** Interactive business dashboard
    - **Streamlit:** Web application development
    - **Pandas:** Data manipulation
    - **Plotly:** Interactive visualizations
    """)

    st.subheader("Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        metric_card("Total Records", f"{len(df):,}")

    with col2:
        metric_card("Total Columns", f"{len(df.columns)}")

    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)


# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<center style='color:#64748B;'>"
    "OLA Ride Insights | Data Analytics Project"
    "</center>",
    unsafe_allow_html=True
)
