import streamlit as st

st.set_page_config(
    page_title="Players",
    page_icon="🏃🏼",
    layout="wide"
)

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

# Layout do jogador - CORRIGIDO
col1, col2 = st.columns([1, 3])

with col1:
    # Foto do jogador com largura controlada
    try:
        st.image(player_stats["Photo"], width=200)
    except:
        st.warning("Foto não disponível")

    # Bandeira do país
    try:
        st.image(player_stats["Flag"], width=80)
    except:
        st.warning("Bandeira não disponível")

with col2:
    st.title(f"{player_stats['Name']}")
    st.markdown(f"### {player_stats['Club']}")
    st.markdown(f"**Posição:** {player_stats['Position']}")

    st.markdown("---")

    col_a, col_b, col_c = st.columns(3)
    col_a.markdown(f"**Idade:** {player_stats['Age']} anos")
    col_b.markdown(f"**Altura:** {player_stats['Height(cm.)'] / 100:.2f} m")
    col_c.markdown(f"**Peso:** {player_stats['Weight(lbs.)'] * 0.453:.2f} kg")

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

st.divider()

# Estatísticas técnicas
st.subheader("🎯 Principais Atributos")

# Pega alguns atributos relevantes
attributes = {
    'Pace': player_stats.get('Pace', 0),
    'Shooting': player_stats.get('Shooting', 0),
    'Passing': player_stats.get('Passing', 0),
    'Dribbling': player_stats.get('Dribbling', 0),
    'Defending': player_stats.get('Defending', 0),
    'Physical': player_stats.get('Physic', 0)
}

col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

for idx, (attr, value) in enumerate(attributes.items()):
    with cols[idx % 3]:
        st.metric(label=attr, value=f"{value}")
        st.progress(int(value) / 100)
