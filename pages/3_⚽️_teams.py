import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Teams",
    page_icon="🌐",
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

# Sidebar
st.sidebar.markdown("## 🔍 Filtros")
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

# Filtrar dados do clube
df_filtered = df_data[(df_data["Club"] == club)].set_index("Name")

# Cabeçalho do clube
st.title(f"🏆 {club}")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Jogadores", len(df_filtered))
with col2:
    st.metric("Overall Médio", f"{df_filtered['Overall'].mean():.1f}")
with col3:
    st.metric("Valor Total do Elenco", f"£ {df_filtered['Value(£)'].sum():,.0f}")

st.divider()

# Tabela de jogadores (SEM IMAGENS por enquanto)
st.subheader("📋 Elenco Completo")

columns = ["Age", "Overall", "Position", 'Value(£)', 'Wage(£)', 'Joined', 
           'Height(cm.)', 'Weight(lbs.)',
           'Contract Valid Until', 'Release Clause(£)']

st.dataframe(
    df_filtered[columns],
    column_config={
        "Overall": st.column_config.ProgressColumn(
            "Overall", 
            format="%d", 
            min_value=0, 
            max_value=100
        ),
        "Wage(£)": st.column_config.ProgressColumn(
            "Weekly Wage", 
            format="£%f",
            min_value=0, 
            max_value=df_filtered["Wage(£)"].max()
        ),
        "Value(£)": st.column_config.NumberColumn(
            "Valor",
            format="£%.0f"
        ),
        "Release Clause(£)": st.column_config.NumberColumn(
            "Cláusula",
            format="£%.0f"
        ),
    },
    height=600,
    use_container_width=True
)

# Estatísticas do time
st.divider()
st.subheader("📊 Estatísticas do Time")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Jogador Mais Velho", f"{df_filtered['Age'].max()} anos")

with col2:
    st.metric("Jogador Mais Novo", f"{df_filtered['Age'].min()} anos")

with col3:
    st.metric("Idade Média", f"{df_filtered['Age'].mean():.1f} anos")

with col4:
    st.metric("Overall Máximo", f"{df_filtered['Overall'].max()}")
