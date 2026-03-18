import streamlit as st
import pandas as pd

st.set_page_config(page_title="Club Tryouts", layout="wide")
st.title("🏐 Volleyball Tryout Leaderboard")

# --- DATA CONNECTION ---
# 1. Use your Sheet URL but change the end to /export?format=csv
# 2. To get specific tabs, you need the 'gid' number from the end of the URL for that tab
roster_url = "https://docs.google.com/spreadsheets/d/1lKxXGeG_VlDMT8JQ1Dip63To8seOA59w4IvSFNPhaAs//export?format=csv&gid="
try:
    # Read the data
    df = pd.read_csv(roster_url)
    
    st.success("Connected to Google Sheets!")
    
    # Show the table
    st.subheader("Player Roster")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Still can't connect. Error: {e}")
    st.info("Check: Is the Google Sheet set to 'Anyone with the link can view'?")
