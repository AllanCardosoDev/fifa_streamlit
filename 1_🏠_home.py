import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="FIFA23 Dataset",
    page_icon="⚽",
    layout="wide"
)

# Carregar dados
if "data" not in st.session_state:
    df_data = pd.read_csv("datasets/CLEAN_FIFA23_official_data.csv", index_col=0)
    df_data = df_data[df_data["Contract Valid Until"] >= datetime.today().year]
    df_data = df_data[df_data["Value(£)"] > 0]
    df_data = df_data.sort_values(by="Overall", ascending=False)
    st.session_state["data"] = df_data

# Sidebar
st.sidebar.markdown("### Desenvolvido por **Allan Cardoso** 👨‍💻")
st.sidebar.markdown("---")

# Título principal
st.markdown("# FIFA23 OFFICIAL DATASET! ⚽️")

# Botão para Kaggle
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    btn = st.link_button(
        "🔗 Acesse os dados no Kaggle",
        "https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data",
        use_container_width=True
    )

st.markdown("---")

# Descrição do dataset
st.markdown(
    """
    ### 📊 Sobre o Dataset

    O conjunto de dados de jogadores de futebol de 2017 a 2023 fornece informações 
    abrangentes sobre jogadores de futebol profissionais.
    O conjunto de dados contém uma ampla gama de atributos, incluindo dados demográficos 
    do jogador, características físicas, estatísticas de jogo, detalhes do contrato e 
    afiliações de clubes. 

    Com **mais de 17.000 registros**, este conjunto de dados oferece um recurso valioso para 
    analistas de futebol, pesquisadores e entusiastas interessados em explorar vários 
    aspectos do mundo do futebol, pois permite estudar atributos de jogadores, métricas de 
    desempenho, avaliação de mercado, análise de clubes, posicionamento de jogadores e 
    desenvolvimento do jogador ao longo do tempo.
    """
)

# Estatísticas rápidas
st.markdown("### 📈 Estatísticas Gerais")
col1, col2, col3, col4 = st.columns(4)

df_data = st.session_state["data"]

with col1:
    st.metric("Total de Jogadores", f"{len(df_data):,}")

with col2:
    st.metric("Total de Clubes", f"{df_data['Club'].nunique():,}")

with col3:
    st.metric("Média Overall", f"{df_data['Overall'].mean():.1f}")

with col4:
    st.metric("Jogador Mais Valioso", f"£{df_data['Value(£)'].max():,.0f}")
