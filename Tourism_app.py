import streamlit as st

st.title("Tourism Data Analysis")
import pandas as pd
import plotly.express as px

# Required for the 'ols' trendline in Plotly Express
import statsmodels

st.title("Tourism Data Analysis")

# CSV file URL
DATA_URL = "https://linked.aub.edu.lb/pkgcube/data/551015b5649368dd2612f795c2a9c2d8_20240902_115953.csv"

@st.cache_data
def load_data():
    """Load the data from the URL and cache it."""
    try:
        df = pd.read_csv(DATA_URL)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
data_load_state = st.text("Loading data...")
df = load_data()
if df is not None:
    data_load_state.text("Data loaded successfully!")

    # --- Show raw data ---
    if st.checkbox("Show raw data"):
        st.subheader("Raw data")
        st.write(df)

    # --- Sidebar filters ---
    st.sidebar.subheader("Filter Data")
    
    # Tourism Index filter (for both graphs)
    min_index = float(df["Tourism Index"].min())
    max_index = float(df["Tourism Index"].max())
    tourism_index_range = st.sidebar.slider(
        "Select Tourism Index Range",
        min_value=min_index,
        max_value=max_index,
        value=(min_index, max_index),
        step=0.1
    )

    # NEW: Restaurant Count filter (for Graph 1)
    st.sidebar.subheader("Filter Plot 1")
    min_restaurants = float(df["Total number of restaurants"].min())
    max_restaurants = float(df["Total number of restaurants"].max())
    restaurant_range = st.sidebar.slider(
        "Select Restaurant Count Range",
        min_value=min_restaurants,
        max_value=max_restaurants,
        value=(min_restaurants, max_restaurants),
        step=1.0
    )

    # --- Filter data for Graph 1 ---
    filtered_df1 = df[
        (df["Tourism Index"] >= tourism_index_range[0]) &
        (df["Tourism Index"] <= tourism_index_range[1]) &
        (df["Total number of restaurants"] >= restaurant_range[0]) &
        (df["Total number of restaurants"] <= restaurant_range[1])
    ]
    
    # --- First plot: Hotels vs Tourism Index ---
    st.subheader("Hotels vs Tourism Index")
    fig1 = px.scatter(
        filtered_df1,
        x="Total number of hotels",
        y="Tourism Index",
        opacity=0.65,
        trendline='ols',
        trendline_color_override='darkblue',
        title="Relationship Between Number of Hotels and Tourism Index"
    )
    st.plotly_chart(fig1)

    # --- Second plot: Hotels vs Restaurants, size = Tourism Index ---
    # This graph will only be filtered by the Tourism Index range
    filtered_df2 = df[
        (df["Tourism Index"] >= tourism_index_range[0]) &
        (df["Tourism Index"] <= tourism_index_range[1])
    ]

    st.subheader("Hotels vs Restaurants (Size = Tourism Index)")
    fig2 = px.scatter(
        filtered_df2,
        x="Total number of hotels",
        y="Total number of restaurants",
        size="Tourism Index",
        color="Existence of touristic attractions prone to be exploited and developed - exists",
        title="Hotels vs Restaurants Colored by Tourism Attractions Existence"
    )
    st.plotly_chart(fig2)
    