import streamlit as st
import pandas as pd

# 1. YOUR ID (Already working!)
SHEET_ID = "1p-u0r9hOasCAtD8X6o56S_W0q29qRst07VpLzWq6A7Q"
url = f"https://docs.google.com/spreadsheets/d/1lKxXGeG_VlDMT8JQ1Dip63To8seOA59w4IvSFNPhaAs/export?format=csv&gid=0"

st.set_page_config(page_title="Smash Volleyball Tryouts", layout="wide")

# Custom CSS to make it look "Elite"
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_content_as_html=True)

st.title("🏐 Smash Volleyball: Scout Board")

try:
    # Read the data
    df = pd.read_csv(url)
    
    # --- DATA CLEANING ---
    # Ensure columns are numbers (in case someone typed "10ft")
    num_cols = ['Height', 'Reach', 'Approach Touch', 'Block Touch', 'Shuttle Time']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # --- THE MATH ENGINE ---
    if 'Approach Touch' in df.columns and 'Reach' in df.columns:
        # Calculate Vertical
        df['Vertical'] = df['Approach Touch'] - df['Reach']
        
        # Calculate a 0-100 Physicality Score (Weighted)
        # 70% based on Vertical, 30% based on Speed (Shuttle)
        if 'Shuttle Time' in df.columns and df['Shuttle Time'].max() > 0:
            df['Physical_Score'] = (
                (df['Vertical'] / df['Vertical'].max()) * 70 + 
                (1 - (df['Shuttle Time'] / df['Shuttle Time'].max())) * 30
            ).round(1)

    # --- DASHBOARD UI ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Athletes", len(df))
    if 'Vertical' in df.columns:
        col2.metric("Avg Vertical", f"{df['Vertical'].mean():.1f}\"")
        col3.metric("Top Touch", f"{df['Approach Touch'].max():.0f}\"")

    st.divider()

    # LEADERBOARD
    st.subheader("🏆 Physicality Leaderboard")
    if 'Physical_Score' in df.columns:
        # Sort by best score
        display_df = df.sort_values(by="Physical_Score", ascending=False)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Scouting engine error: {e}")
