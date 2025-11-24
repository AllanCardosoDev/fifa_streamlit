import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Players",
    page_icon="🏃🏼",
    layout="wide"
)

# CARREGAR DADOS SE NÃO EXISTIREM
if "data" not in st.session_state:
    df_data = pd.read_csv("datasets/CLEAN_FIFA23_official_data.csv", index_col=0)
    df_data = df_data[df_data["Contract Valid Until"] >= datetime.today().year]
    df_data = df_data[df_data["Value(£)"] > 0]
    df_data = df_data.sort_values(by="Overall", ascending=False)
    st.session_state["data"] = df_data

df_data = st.session_state["data"]

# Sidebar com filtros
st.sidebar.markdown("## 🔍 Filtros")

clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_players = df_data[(df_data["Club"] == club)]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

# Dados do jogador selecionado
player_stats = df_data[df_data["Name"] == player].iloc[0]

# Layout do jogador
st.title(f"⚽ {player_stats['Name']}")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"**Clube:** {player_stats['Club']}")
    st.markdown(f"**Posição:** {player_stats['Position']}")

with col2:
    st.markdown(f"**Idade:** {player_stats['Age']} anos")
    st.markdown(f"**Nacionalidade:** {player_stats['Nationality']}")

with col3:
    st.markdown(f"**Altura:** {player_stats['Height(cm.)'] / 100:.2f} m")
    st.markdown(f"**Peso:** {player_stats['Weight(lbs.)'] * 0.453:.2f} kg")

st.divider()

# Overall
st.subheader(f"⭐ Overall: {player_stats['Overall']}")
st.progress(int(player_stats["Overall"]) / 100)

st.divider()

# Informações financeiras
st.subheader("💰 Informações Financeiras")
col1, col2, col3 = st.columns(3)

col1.metric(
    label="Valor de Mercado", 
    value=f"£ {player_stats['Value(£)']:,.0f}"
)
col2.metric(
    label="Salário Semanal", 
    value=f"£ {player_stats['Wage(£)']:,.0f}"
)
col3.metric(
    label="Cláusula de Rescisão", 
    value=f"£ {player_stats['Release Clause(£)']:,.0f}"
)
