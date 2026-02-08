import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from data_loader import load_articles_data

# Set page configuration
st.set_page_config(
    page_title="Sold Articles Overview",
    layout="wide"
)

st.title("🎴 Sold Articles Overview")

# Load data from S3
df = load_articles_data()

if df is None:
    st.error("Could not load articles data. Please check your S3 bucket configuration.")
    st.stop()

# Display the dataframe
st.dataframe(df, use_container_width=True)

# Display variety of stats about the sold articles
st.markdown("### Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    total_articles_sold = len(df)
    st.metric("Total Articles Sold", total_articles_sold)

with col2:
    total_revenue = df['card_prices'].sum()
    st.metric("Total Revenue", f"€{total_revenue:.2f}")

with col3:
    unique_sets = df['set_names'].nunique()
    st.metric("Unique Sets", unique_sets)

# Display the number of cards sold per card_rarity
st.markdown("---")
st.markdown("### Articles Sold by Rarity")
rarity_counts = df['card_rarities'].value_counts()
st.bar_chart(rarity_counts)

# Cards Sold by Set (Treemap)
st.markdown("---")
st.title("🌳 Cards Sold by Set")

# Group by set only, count total cards
treemap_data = df.groupby('set_names').size().reset_index(name='count')

# Create treemap with just sets
fig = px.treemap(
    treemap_data,
    path=['set_names'],  # Only set level, no card names
    values='count',
    title='Cards Sold per Set'
)

fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
fig.update_traces(
    textposition="middle center",
    textfont_size=14
)

st.plotly_chart(fig, use_container_width=True)