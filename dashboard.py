import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SoccerStats", layout="wide")
st.title("SoccerStats")

df = pd.read_csv("Clean.csv")

competition = st.selectbox("Choisir une compétition :", sorted(df["Comp"].unique()))
positions = st.multiselect("Choisir une ou plusieurs positions :", sorted(df["Pos"].unique()))

df_filtre = df[df["Comp"] == competition]
if positions:
    df_filtre = df_filtre[df_filtre["Pos"].isin(positions)]

st.subheader("Plusieurs graphiques")

col1, col2 = st.columns(2)

with col1:
    pos_counts = df_filtre["Pos"].value_counts().reset_index()
    pos_counts.columns = ["Poste", "Joueurs"]
    fig = px.bar(pos_counts, x="Poste", y="Joueurs", text="Joueurs", color="Poste")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    nat_counts = df_filtre["Nation"].value_counts().head(15).reset_index()
    nat_counts.columns = ["Nation", "Joueurs"]
    fig = px.bar(nat_counts, x="Nation", y="Joueurs", text="Joueurs", color="Nation")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Statistiques individuelles")

col3, col4 = st.columns(2)

with col3:
    top_buteurs = df_filtre.sort_values("Gls", ascending=False).head(20)
    fig = px.bar(top_buteurs, x="Player", y="Gls", color="Squad", text="Gls", title="Top 20 buteurs")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.scatter(df_filtre, x="xG", y="Gls", size="Min", color="Pos", hover_name="Player", title="xG vs Buts")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Analyse de joueurs")

joueurs = st.multiselect("Choisir des joueurs :", df_filtre["Player"].unique())

if joueurs:
    df_joueurs = df_filtre[df_filtre["Player"].isin(joueurs)]

    col5, col6 = st.columns(2)
    with col5:
        fig = px.bar(df_joueurs, x="Player", y="Gls", color="Pos", text="Gls", title="Buts par joueur")
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        fig = px.scatter(df_joueurs, x="Min", y="Ast", size="Gls", color="Squad", hover_name="Player", title="Minutes vs Assists")
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_joueurs)
else:
    st.info("Sélectionnez un ou plusieurs joueurs pour voir leurs statistiques.")

st.subheader("Données filtrées")
st.dataframe(df_filtre)
