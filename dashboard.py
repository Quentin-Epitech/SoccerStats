import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SoccerStats", layout="wide")

st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1f4e79 0%, #2d5a87 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;}
.main-header h1 {
    color: white;
    font-size: 3rem;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);}
.section-header {
    color: #1f4e79;
    font-size: 1.8rem;
    font-weight: bold;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 3px solid #1f4e79;}
.stSelectbox > div > div {
    background-color: #1f4e79;
    color: white;
    border-radius: 8px;
    border: 1px solid #2d5a87;}
.stSelectbox > div > div > div {
    color: white;}
.stMultiSelect > div > div {
    background-color: #1f4e79;
    color: white;
    border-radius: 8px;
    border: 1px solid #2d5a87;}
.stMultiSelect > div > div > div {
    color: white;}
.stSelectbox label, .stMultiSelect label {
    color: white;}
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);}
</style>
""", unsafe_allow_html=True)



df = pd.read_csv("Clean.csv")

competitions = sorted(df["Comp"].unique())
competitions.insert(0, "Toutes les compétitions")
competition = st.selectbox("Choisir une compétition :", competitions)

positions = st.multiselect("Choisir une ou plusieurs positions :", sorted(df["Pos"].unique()))

if competition == "Toutes les compétitions":
    df_filtre = df.copy()
else:
    df_filtre = df[df["Comp"] == competition]

if positions:
    df_filtre = df_filtre[df_filtre["Pos"].isin(positions)]

st.subheader("Plusieurs graphiques")
col1, col2 = st.columns(2)
with col1:
    pos_counts = df_filtre["Pos"].value_counts().reset_index()
    pos_counts.columns = ["Poste", "Joueurs"]
    fig = px.bar(pos_counts, x="Poste", y="Joueurs", text="Joueurs", color="Poste", title="Répartition des postes")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    nat_counts = df_filtre["Nation"].value_counts().head(15).reset_index()
    nat_counts.columns = ["Nation", "Joueurs"]
    fig = px.bar(nat_counts, x="Nation", y="Joueurs", text="Joueurs", color="Nation", title="Top 15 nationalités")
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
    col5, col6, col7 = st.columns(3)
    with col5:
        fig = px.bar(df_joueurs, x="Player", y="Gls", color="Pos", text="Gls", title="Buts par joueur")
        st.plotly_chart(fig, use_container_width=True)
    with col6:
        fig = px.scatter(df_joueurs, x="Min", y="Ast", size="Gls", color="Squad", hover_name="Player", title="Minutes vs Assists")
        st.plotly_chart(fig, use_container_width=True)
    with col7:
        fig = px.scatter(df_joueurs, x="Min", y="Gls", size="Ast", color="Squad", hover_name="Player", title="Minutes vs Buts")
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_joueurs)
else:
    st.info("Sélectionnez un ou plusieurs joueurs pour voir leurs statistiques.")

st.subheader("Données filtrées")
st.dataframe(df_filtre)
