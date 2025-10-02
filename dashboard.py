import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("Clean.csv")

st.set_page_config(page_title="Tableau de bord des joueurs", layout="wide")
st.title("Tableau de bord - SocerStats")

competition = st.selectbox("Choisir une compétition :", df["Comp"].unique())
positions = st.multiselect("Choisir une ou plusieurs positions :", df["Pos"].unique())

df_filtre = df[df["Comp"] == competition]
if positions:
    df_filtre = df_filtre[df_filtre["Pos"].isin(positions)]

st.subheader("Nombre de buts par joueur")
fig1 = px.bar(
    df_filtre.sort_values("Gls", ascending=False).head(20),
    x="Player", y="Gls", color="Squad", text="Gls")
st.plotly_chart(fig1, use_container_width=True)


st.subheader("xG (buts attendus) vs Buts marqués")
fig2 = px.scatter(
    df_filtre, x="xG", y="Gls", size="Min", color="Pos",
    hover_name="Player", title="Efficacité offensive")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Nombre de joueurs par poste")
compte_postes = df_filtre["Pos"].value_counts().reset_index()
compte_postes.columns = ["Poste", "Nombre de joueurs"]
fig3 = px.bar(compte_postes,x="Poste", y="Nombre de joueurs", text="Nombre de joueurs")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Nombre de joueurs par nation (Top 15)")
compte_nations = df_filtre["Nation"].value_counts().head(15).reset_index()
compte_nations.columns = ["Nation", "Nombre de joueurs"]
fig4 = px.bar(compte_nations,x="Nation", y="Nombre de joueurs", text="Nombre de joueurs")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Données filtrées")
st.dataframe(df_filtre)
