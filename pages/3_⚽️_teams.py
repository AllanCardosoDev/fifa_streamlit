import streamlit as st

st.set_page_config(
    page_title="Teams",
    page_icon="🌐",
    layout="wide"
)

df_data = st.session_state["data"]

# Sidebar
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

# Filtrar dados do clube
df_filtered = df_data[(df_data["Club"] == club)].set_index("Name")

# Cabeçalho do clube - CORRIGIDO
col1, col2 = st.columns([1, 4])

with col1:
    # Logo do clube com largura controlada
    try:
        st.image(df_filtered.iloc[0]["Club Logo"], width=150)
    except:
        st.warning("Logo não disponível")

with col2:
    st.markdown(f"# {club}")
    st.markdown(f"**Total de Jogadores:** {len(df_filtered)}")
    st.markdown(f"**Overall Médio:** {df_filtered['Overall'].mean():.1f}")

st.divider()

# Tabela de jogadores
st.subheader("📋 Elenco Completo")

columns = ["Age", "Photo", "Flag", "Overall", 'Value(£)', 'Wage(£)', 'Joined', 
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
        "Photo": st.column_config.ImageColumn(
            "Foto",
            width="small"  # ADICIONADO: controla tamanho
        ),
        "Flag": st.column_config.ImageColumn(
            "País",
            width="small"  # ADICIONADO: controla tamanho
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
