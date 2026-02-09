import streamlit as st
import pandas as pd
from data_loader import load_articles_data, load_orders_data
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Orders Overview",
    layout="wide"
)

st.title("📊 Orders Overview")

# Load data from S3
df = load_orders_data()

if df is None:
    st.error("Could not load orders data. Please check your S3 bucket configuration.")
    st.stop()

# Display variety of stats about the sold articles
st.markdown("### Key Metrics of Shipped Orders")

# Display total orders
st.write(f"**Total Orders:** {len(df)}")

# Display metrics in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Revenue (Articles Value + Shipping)", value=f"€{df['Total Value'].sum():.2f}")

with col2:
    st.metric(label="Total Commission Paid", value=f"€{df['Commission'].sum():.2f}")

with col3:
    st.metric(label="Net Revenue", value=f"€{df['Net Value'].sum():.2f}")

# Add spacing
st.markdown("---")

# Load data from S3
articles_df = load_articles_data()

if articles_df is None:
    st.error("Could not load articles data. Please check your S3 bucket configuration.")
    st.stop()

# Display variety of stats about the sold articles
st.markdown("### Key Metrics of Sold Articles")

col1, col2, col3 = st.columns(3)

with col1:
    total_articles_sold = len(articles_df)
    st.metric("Total Number of Singles Sold", total_articles_sold)

with col2:
    total_revenue = articles_df['card_prices'].sum()
    st.metric("Total Revenue on Sold Singles", f"€{total_revenue:.2f}")

with col3: # average card price
    average_price = articles_df['card_prices'].mean()
    st.metric("Average Card Price", f"€{average_price:.2f}")

# Cumulative Net Revenue Chart
st.subheader("Cumulative Net Revenue Over Time")

# Calculate cumulative sum of net value
df['Cumulative Net Value'] = df['Net Value'].cumsum()

# Create the line chart
st.line_chart(
    df.set_index('Date of Purchase')['Cumulative Net Value'],
    use_container_width=True
)

col1, col2 = st.columns(2)

with col1:
    # Create a barchart depicting orders by month, separate X axis by month and year, e.g. Jan 2023, Feb 2023, etc.
    st.subheader("Orders by Month")
    df['Date of Purchase'] = pd.to_datetime(df['Date of Purchase'])
    df['Month'] = df['Date of Purchase'].dt.to_period('M')
    orders_by_month = df.groupby('Month').size().reset_index(name='Orders')
    orders_by_month['Month'] = orders_by_month['Month'].dt.strftime('%b %Y')  # Format as "Jan 2023"

    fig = px.bar(orders_by_month, x='Month', y='Orders')
    fig.update_layout(xaxis_tickangle=-45)  # Rotate labels 45 degrees
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # do the same as above, but instead of depicting orders by month, depict total net revenue by month
    st.subheader("Net Revenue by Month")
    df['Month'] = df['Date of Purchase'].dt.to_period('M')
    net_revenue_by_month = df.groupby('Month')['Net Value'].sum().reset_index(name='Net Revenue')
    net_revenue_by_month['Month'] = net_revenue_by_month['Month'].dt.strftime('%b %Y')  # Format as "Jan 2023"

    fig = px.bar(net_revenue_by_month, x='Month', y='Net Revenue')
    fig.update_layout(xaxis_tickangle=-45)  # Rotate labels 45 degrees
    st.plotly_chart(fig, use_container_width=True)