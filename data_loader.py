"""
Data loader for CardMarket Dashboard
Reads CSV files from public S3 bucket
"""
import pandas as pd
import streamlit as st

# S3 Configuration - Public bucket, geen credentials nodig!
BUCKET_NAME = "mtg-streamlit-dashboard-s3-bucket"
PUBLIC_BASE_URL = f"https://{BUCKET_NAME}.s3.eu-central-1.amazonaws.com"

# File paths
ORDERS_CSV_URL = f"{PUBLIC_BASE_URL}/public/exports/cardmarket_orders_data.csv"
ARTICLES_CSV_URL = f"{PUBLIC_BASE_URL}/public/exports/cardmarket_articles_sold.csv"
EXPENSES_ODS_URL = f"{PUBLIC_BASE_URL}/raw/monthly_expenses/Expenses.ods"

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_orders_data():
    """
    Load orders data from S3
    Returns: pandas DataFrame
    """
    try:
        df = pd.read_csv(ORDERS_CSV_URL)
        
        # Convert Date of Purchase to datetime
        df['Date of Purchase'] = pd.to_datetime(df['Date of Purchase'])
        
        # Convert numeric columns (handle European format)
        numeric_columns = ['Merchandise Value', 'Shipment Costs', 'Total Value', 'Commission']
        for col in numeric_columns:
            if col in df.columns and df[col].dtype == 'object':
                df[col] = df[col].str.replace(',', '.').astype(float)
        
        # Calculate net value
        df['Net Value'] = df['Total Value'] - df['Commission']
        
        # Sort by date
        df = df.sort_values('Date of Purchase')
        
        return df
    except Exception as e:
        st.error(f"Error loading orders data: {str(e)}")
        st.error(f"Tried to load from: {ORDERS_CSV_URL}")
        return None


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_articles_data():
    """
    Load articles data from S3
    Returns: pandas DataFrame
    """
    try:
        df = pd.read_csv(ARTICLES_CSV_URL)
        
        # Convert card_prices (handle European format)
        if 'card_prices' in df.columns and df['card_prices'].dtype == 'object':
            df['card_prices'] = df['card_prices'].str.replace(',', '.').astype(float)
        
        return df
    except Exception as e:
        st.error(f"Error loading articles data: {str(e)}")
        st.error(f"Tried to load from: {ARTICLES_CSV_URL}")
        return None


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_expenses_data():
    """
    Load monthly expenses data from S3 (ODS format)
    Returns: pandas DataFrame
    """
    try:
        df = pd.read_excel(EXPENSES_ODS_URL, engine='odf')
        
        # Convert Order_Date to datetime
        df['Order_Date'] = pd.to_datetime(df['Order_Date'])
        
        # Sort by date
        df = df.sort_values('Order_Date')
        
        return df
    except Exception as e:
        st.error(f"Error loading expenses data: {str(e)}")
        st.error(f"Tried to load from: {EXPENSES_ODS_URL}")
        return None


def refresh_data():
    """
    Clear cache to force data refresh
    """
    st.cache_data.clear()
    st.success("Data cache cleared! Reload the page to fetch fresh data.")