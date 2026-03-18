import streamlit as st
import pandas as pd

# 1. PASTE YOUR ID BETWEEN THE QUOTES BELOW
SHEET_ID = "Club_Tryouts_Data_2026"

# This builds the direct download link for the first tab
url = f"https://docs.google.com/spreadsheets/d/1lKxXGeG_VlDMT8JQ1Dip63To8seOA59w4IvSFNPhaAs/export?format=csv"

st.set_page_config(page_title="Club Tryouts", layout="wide")
st.title("SMASH Volleyball Tryout Leaderboard")

try:
    # Read the data directly using pandas
    df = pd.read_csv(url)
    
    if st.success("Connected to Google Sheets!"):
        st.subheader("Current Roster")
        st.dataframe(df, use_container_width=True)
        
        # Simple stats check
        if 'Height' in df.columns:
            st.metric("Avg Height", f"{df['Height'].mean():.1f}\"")

except Exception as e:
    st.error("Connection Failed")
    st.write("Troubleshooting Steps:")
    st.write("1. Make sure your Google Sheet is set to 'Anyone with the link can view'.")
    st.write(f"2. Check if this link works in your browser: [Click to test link]({url})")
    st.write(f"Technical Error: {e}")
