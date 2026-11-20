
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
    color: #263445;
}

[data-testid="stSidebar"] {
    background-color: #E8EFF5;
    border-right: 1px solid #D5E0E9;
}

[data-testid="stSidebar"] * {
    color: #263445 !important;
}

h1 {
    color: #153B50 !important;
    font-weight: 750 !important;
}

h2, h3 {
    color: #167D8D !important;
}

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #DCE6EE;
    box-shadow: 0 3px 10px rgba(30,60,80,0.06);
}

[data-testid="stMetricLabel"] {
    color: #607487 !important;
}

[data-testid="stMetricValue"] {
    color: #087E8B !important;
    font-weight: 700;
}

.stButton button {
    background-color: #087E8B;
    color: white;
    border-radius: 8px;
    border: none;
}

[data-testid="stDataFrame"] {
    border-radius: 10px;
}

hr {
    border-color: #DCE6EE;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    data = pd.read_csv("OLA_Cleaned_Data.csv")

    numeric_columns = [
        "Booking_Value",
        "Ride_Distance",
        "Driver_Ratings",
        "Customer_Rating"
    ]

    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    return data


df = load_data()

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


# ---------------- WORKSPACE SIDEBAR ----------------
st.sidebar.title("🚕 OLA INSIGHTS")
st.sidebar.caption("RIDE ANALYTICS PLATFORM")
st.sidebar.divider()

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

st.sidebar.divider()
st.sidebar.caption("July 2024 | Data Analytics Project")


# ---------------- 1. EXECUTIVE OVERVIEW ----------------
if page == "Executive Overview":

    st.title("Executive Overview")
    st.caption("Complete overview of OLA ride booking performance")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Bookings", f"{len(df):,}")
    c2.metric("Successful Rides", f"{len(success):,}")
    c3.metric("Cancelled Rides", f"{len(cancelled):,}")
    c4.metric(
        "Total Revenue",
        f"₹{success['Booking_Value'].sum():,.0f}"
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Booking Status Breakdown")

        status_data = (
            df["Booking_Status"].value_counts().reset_index()
        )
        status_data.columns = ["Status", "Bookings"]

        fig = px.pie(
            status_data,
            names="Status",
            values="Bookings",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Ride Volume Over Time")

        daily = (
            df.groupby("Date")["Booking_ID"]
            .count().reset_index()
        )

        fig = px.line(
            daily,
            x="Date",
            y="Booking_ID",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)


# ---------------- 2. VEHICLE ANALYSIS ----------------
elif page == "Vehicle Analysis":

    st.title("Vehicle Analysis")
    st.caption("Vehicle-wise booking and distance performance")

    vehicle = df.groupby("Vehicle_Type").agg(
        Total_Booking_Value=("Booking_Value", "sum"),
        Success_Booking_Value=("Booking_Value",
                               lambda x: x[df.loc[x.index, "Booking_Status"] == "Success"].sum()),
        Avg_Distance=("Ride_Distance", "mean"),
        Total_Distance=("Ride_Distance", "sum")
    ).reset_index()

    st.subheader("Vehicle Performance Table")
    st.dataframe(vehicle, use_container_width=True)

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Booking Value by Vehicle")

        fig = px.bar(
            vehicle,
            x="Vehicle_Type",
            y="Total_Booking_Value",
            color="Vehicle_Type"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Successful Booking Value by Vehicle")

        fig = px.bar(
            vehicle,
            x="Vehicle_Type",
            y="Success_Booking_Value",
            color="Vehicle_Type"
        )
        st.plotly_chart(fig, use_container_width=True)


# ---------------- 3. REVENUE ANALYSIS ----------------
elif page == "Revenue Analysis":

    st.title("Revenue Analysis")
    st.caption("Revenue and ride distance performance")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Revenue",
        f"₹{success['Booking_Value'].sum():,.0f}"
    )

    c2.metric(
        "Average Booking Value",
        f"₹{df['Booking_Value'].mean():,.0f}"
    )

    c3.metric(
        "Total Ride Distance",
        f"{df['Ride_Distance'].sum():,.0f}"
    )

    c4.metric(
        "Average Ride Distance",
        f"{df['Ride_Distance'].mean():,.1f}"
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Revenue by Payment Method")

        payment = (
            success.groupby("Payment_Method")["Booking_Value"]
            .sum().reset_index()
        )

        fig = px.bar(
            payment,
            x="Payment_Method",
            y="Booking_Value",
            color="Payment_Method"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Revenue by Date")

        daily = (
            success.groupby("Date")["Booking_Value"]
            .sum().reset_index()
        )

        fig = px.line(
            daily,
            x="Date",
            y="Booking_Value",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)


# ---------------- 4. CANCELLATION ANALYSIS ----------------
elif page == "Cancellation Analysis":

    st.title("Cancellation Analysis")
    st.caption("Understand ride cancellations and their reasons")

    c1, c2 = st.columns(2)

    c1.metric(
        "Customer Cancellations",
        f"{customer_cancelled:,}"
    )

    c2.metric(
        "Driver Cancellations",
        f"{driver_cancelled:,}"
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Incomplete Rides by Reason")

        reasons = (
            df["Incomplete_Rides_Reason"]
            .dropna()
            .value_counts()
            .reset_index()
        )
        reasons.columns = ["Reason", "Count"]

        fig = px.bar(
            reasons,
            x="Count",
            y="Reason",
            orientation="h"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Cancelled Rides by Vehicle")

        vehicle_cancel = (
            cancelled["Vehicle_Type"]
            .value_counts().reset_index()
        )
        vehicle_cancel.columns = ["Vehicle Type", "Bookings"]

        fig = px.bar(
            vehicle_cancel,
            x="Vehicle Type",
            y="Bookings",
            color="Vehicle Type"
        )
        st.plotly_chart(fig, use_container_width=True)


# ---------------- 5. RATINGS ANALYSIS ----------------
elif page == "Ratings Analysis":

    st.title("Ratings Analysis")
    st.caption("Driver and customer rating performance")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Average Driver Rating",
        f"{df['Driver_Ratings'].mean():.2f}"
    )

    c2.metric(
        "Average Customer Rating",
        f"{df['Customer_Rating'].mean():.2f}"
    )

    c3.metric(
        "Total Rated Rides",
        f"{df['Driver_Ratings'].count():,}"
    )

    c4.metric(
        "Customer Rated Rides",
        f"{df['Customer_Rating'].count():,}"
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Driver Rating by Vehicle")

        driver = (
            df.groupby("Vehicle_Type")["Driver_Ratings"]
            .mean().reset_index()
        )

        fig = px.bar(
            driver,
            x="Vehicle_Type",
            y="Driver_Ratings",
            color="Vehicle_Type"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Customer Rating by Vehicle")

        customer = (
            df.groupby("Vehicle_Type")["Customer_Rating"]
            .mean().reset_index()
        )

        fig = px.bar(
            customer,
            x="Vehicle_Type",
            y="Customer_Rating",
            color="Vehicle_Type"
        )
        st.plotly_chart(fig, use_container_width=True)


# ---------------- 6. ABOUT PROJECT ----------------
elif page == "About Project":

    st.title("About OLA Ride Insights")

    st.write(
        "OLA Ride Insights is a data analytics project "
        "based on July 2024 ride booking data."
    )

    st.subheader("Project Objectives")

    st.markdown("""
    - Analyze ride booking trends
    - Understand revenue performance
    - Study vehicle-wise performance
    - Identify ride cancellation patterns
    - Analyze driver and customer ratings
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

    st.subheader("Dataset Information")

    c1, c2 = st.columns(2)
    c1.metric("Total Records", f"{len(df):,}")
    c2.metric("Total Columns", f"{len(df.columns)}")

    st.subheader("Project Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)


# ---------------- FOOTER ----------------
st.divider()
st.caption("OLA Ride Insights | July 2024 | Data Analytics Project")
