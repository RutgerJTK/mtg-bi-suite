import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_orders_data, load_articles_data

st.set_page_config(
    page_title="Analytics",
    layout="wide"
)

st.title("📈 Analytics")

# Load data
orders_df = load_orders_data()
articles_df = load_articles_data()

if orders_df is None or articles_df is None:
    st.error("Could not load data. Please check your S3 bucket configuration.")
    st.stop()

# =========================
# Cards Sold by Set (Treemap)
# =========================
st.header("📦 Cards Sold by Set")

# Group by set, count total cards
treemap_data = articles_df.groupby('set_names').size().reset_index(name='count')

fig = px.treemap(
    treemap_data,
    path=['set_names'],
    values='count',
    title='Cards Sold per Set'
)

fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
fig.update_traces(
    textposition="middle center",
    textfont_size=14
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# Orders by Country (Map)
# =========================
st.markdown("---")
st.header("🌍 Orders by Country")

# Count orders per country
country_data = orders_df.groupby('Country').size().reset_index(name='order_count')

# Create choropleth map
fig_map = px.choropleth(
    country_data,
    locations='Country',
    locationmode='country names',
    color='order_count',
    hover_name='Country',
    color_continuous_scale=['yellow', 'green'],
    title='Orders by Country'
)

# Zoom to Europe
fig_map.update_geos(
    scope='europe',
    projection_scale=1.3,
    showland=True,
    landcolor='lightgray',
    showcountries=True,
    countrycolor='white',
    countrywidth=1
)

fig_map.update_layout(
    margin=dict(l=0, r=0, t=50, b=0),
    height=600
)

st.plotly_chart(fig_map, use_container_width=True)

# =========================
# Cumulative Sales by Country
# =========================
st.markdown("---")
st.header("📈 Cumulative Sales by Country Over Time")

# Get top 5 countries
top_countries = orders_df['Country'].value_counts().head(5).index.tolist()

# Sort all data by date
df_sorted = orders_df.sort_values('Date of Purchase').copy()

# For each country, calculate running cumulative count
cumulative_data = []
for country in top_countries:
    # Get all dates
    all_dates = df_sorted['Date of Purchase'].unique()
    
    # Count cumulative orders for this country
    country_orders = df_sorted[df_sorted['Country'] == country]['Date of Purchase']
    
    cumulative_count = 0
    for date in all_dates:
        # Add orders from this date
        cumulative_count += (country_orders == date).sum()
        cumulative_data.append({
            'Date of Purchase': date,
            'Country': country,
            'Cumulative Orders': cumulative_count
        })

cumulative_df = pd.DataFrame(cumulative_data)

# Create stacked area chart
fig_cumulative = px.area(
    cumulative_df,
    x='Date of Purchase',
    y='Cumulative Orders',
    color='Country',
    title='Cumulative Orders by Country',
    groupnorm=None
)

# Customize hover template
fig_cumulative.update_traces(
    hovertemplate='<b>%{fullData.name}</b><br>%{y}<extra></extra>'
)

fig_cumulative.update_layout(
    xaxis_title='Date',
    yaxis_title='Total Orders',
    hovermode='x unified',
    height=500
)

st.plotly_chart(fig_cumulative, use_container_width=True)

# =========================
# Quick Stats
# =========================
st.markdown("---")
st.header("📊 Quick Stats")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Unique Cards Sold", len(articles_df))

with col2:
    st.metric("Total Unique Sets", articles_df['set_names'].nunique())

with col3:
    st.metric("Countries Served", orders_df['Country'].nunique())