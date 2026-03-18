import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="SMASH Volleyball Tryout Tracker", layout="wide")
st.title("Team Selection Dashboard")

# --- CONNECT TO DATA ---
# Replace the URL below with your actual Google Sheet link
url = "https://docs.google.com/spreadsheets/d/1lKxXGeG_VlDMT8JQ1Dip63To8seOA59w4IvSFNPhaAs/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# Read the 'Roster' and 'Physical_Tests' tabs
df_roster = conn.read(spreadsheet=url, worksheet="Roster")
df_phys = conn.read(spreadsheet=url, worksheet="Physical_Tests")

# --- CALCULATION LOGIC ---
# We calculate a 'Power Score' based on Vertical and Speed
# Vertical = Approach Touch - Standing Reach
if not df_phys.empty:
    df_phys['Vertical'] = df_phys['Approach Touch'] - df_phys['Reach']
    
    # Normalize scores (0 to 100) to create a ranking
    df_phys['Physical_Rank'] = (
        (df_phys['Vertical'] / df_phys['Vertical'].max()) * 60 + 
        (1 - (df_phys['Shuttle Time'] / df_phys['Shuttle Time'].max())) * 40
    )

# --- DASHBOARD UI ---
tab1, tab2 = st.tabs(["🏆 Leaderboard", "📊 Player Profiles"])

with tab1:
    st.subheader("Current Top Prospects (Physicality)")
    if not df_phys.empty:
        # Merge physical data with names from Roster
        leaderboard = pd.merge(df_roster[['Name', 'Bib #', 'Position']], 
                               df_phys[['Name', 'Vertical', 'Physical_Rank']], 
                               on="Name")
        
        # Sort by the highest rank
        st.dataframe(leaderboard.sort_values(by="Physical_Rank", ascending=False), use_container_width=True)
    else:
        st.info("No test data recorded yet.")

with tab2:
    player_list = df_roster['Name'].tolist()
    selected_player = st.selectbox("Select a player to view details", player_list)
    
    # Display individual stats
    p_data = df_roster[df_roster['Name'] == selected_player]
    col1, col2 = st.columns(2)
    col1.metric("Position", p_data['Position'].values[0])
    col1.metric("Bib #", p_data['Bib #'].values[0])
