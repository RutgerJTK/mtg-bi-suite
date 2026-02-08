import streamlit as st
import pandas as pd
from data_loader import load_orders_data

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

# Display total orders
st.write(f"**Total Orders:** {len(df)}")

# Display metrics in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Revenue (Gross)", value=f"€{df['Total Value'].sum():.2f}")

with col2:
    st.metric(label="Total Commission Paid", value=f"€{df['Commission'].sum():.2f}")

with col3:
    st.metric(label="Net Revenue", value=f"€{df['Net Value'].sum():.2f}")

# Display the dataframe
st.dataframe(df, use_container_width=True)

# Add download button
st.download_button(
    label="Download CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='cardmarket_orders_data.csv',
    mime='text/csv',
)

# Add spacing
st.markdown("---")

# Cumulative Net Revenue Chart
st.subheader("Cumulative Net Revenue Over Time")

# Calculate cumulative sum of net value
df['Cumulative Net Value'] = df['Net Value'].cumsum()

# Create the line chart
st.line_chart(
    df.set_index('Date of Purchase')['Cumulative Net Value'],
    use_container_width=True
)