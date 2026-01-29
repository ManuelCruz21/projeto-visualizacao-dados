import streamlit as st
import pandas as pd
import plotly.express as px


# Carregar CSV Jogadores
df_players = pd.read_csv("dados/PrimeiraLiga_players.csv", encoding="utf-8")

# Média de golos por jogo
df_players['goals_per_match'] = df_players['goals'] / df_players['matches_played']

# Golos + Assistências por jogo
df_players['contribution_per_match'] = (df_players['goals'] + df_players['assists']) / df_players['matches_played']

st.set_page_config(page_title="Dashboard Primeira Liga 23/24", layout="wide")

st.title("Dashboard - Primeira Liga 2023/2024")
st.markdown("Análise interativa de desempenho dos jogadores (golos, assistências e contribuições).")

# Filtros laterais
st.sidebar.header("Filtros")

teams = df_players['team_name'].dropna().unique()
positions = df_players['position'].dropna().unique()

selected_team = st.sidebar.multiselect("Equipa:", options=teams, default=teams)
selected_position = st.sidebar.multiselect("Posição:", options=positions, default=positions)

df_filtered = df_players[(df_players['team_name'].isin(selected_team)) & (df_players['position'].isin(selected_position))]

# Métricas
st.subheader("Estatísticas gerais (filtros aplicados)")
col1, col2, col3 = st.columns(3)

col1.metric("Média de Golos", round(df_filtered['goals'].mean(), 2))
col2.metric("Média de Assistências", round(df_filtered['assists'].mean(), 2))
col3.metric("Média de Contribuição/Jogo", round(df_filtered['contribution_per_match'].mean(), 3))

# Gráficos interativos

# Scatter Plot — desempenho individual
fig1 = px.scatter(
    df_filtered, x='goals_per_match', y='contribution_per_match',
    hover_data=['first_name', 'last_name', 'team_name', 'position'],
    color='position', size='matches_played',
    title="Desempenho: Golos por Jogo vs Contribuição por Jogo"
)
st.plotly_chart(fig1, use_container_width=True)

# Bar Chart — Top 10 marcadores
top_scorers = df_filtered.sort_values(by='goals', ascending=False).head(10)
fig2 = px.bar(
    top_scorers, x='last_name', y='goals', color='team_name',
    title="Top 10 Marcadores", text='goals'
)
st.plotly_chart(fig2, use_container_width=True)

# Boxplot — distribuição de golos por posição
fig3 = px.box(
    df_filtered, x='position', y='goals_per_match', color='position',
    title="Distribuição de Golos por Jogo por Posição"
)
st.plotly_chart(fig3, use_container_width=True)

# Tabela
st.subheader("Tabela de Jogadores")
st.dataframe(df_filtered[['first_name', 'last_name', 'team_name', 'position', 'goals', 'assists', 'goals_per_match', 'contribution_per_match']])
