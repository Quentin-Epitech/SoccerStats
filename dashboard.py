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
    text-align: center;
}
.main-header h1 {
    color: white;
    font-size: 3rem;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
.section-header {
    color: #1f4e79;
    font-size: 1.8rem;
    font-weight: bold;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 3px solid #1f4e79;
}
.stSelectbox > div > div {
    background-color: #1f4e79;
    color: white;
    border-radius: 8px;
    border: 1px solid #2d5a87;
}
.stSelectbox > div > div > div {
    color: white;
}
.stMultiSelect > div > div {
    background-color: #1f4e79;
    color: white;
    border-radius: 8px;
    border: 1px solid #2d5a87;
}
.stMultiSelect > div > div > div {
    color: white;
}
.stSelectbox label, .stMultiSelect label {
    color: white;
}
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
<h1>SoccerStats Dashboard</h1>
</div>
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

st.subheader("Aperçu général")

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

st.subheader("Analyses approfondies")

col1, col2 = st.columns(2)
with col1:
    top_ga = df_filtre.sort_values("G+A", ascending=False).head(20)
    fig = px.bar(top_ga, x="Player", y="G+A", color="Squad", text="G+A", title="Top 20 joueurs (Buts + Passes décisives)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    goals_by_league = df_filtre.groupby("Comp")["Gls"].mean().reset_index()
    fig = px.bar(goals_by_league, x="Comp", y="Gls", color="Comp", text="Gls", title="Moyenne de buts par ligue")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Ratio de buts par 90 minutes")
goals_90 = df_filtre.sort_values("Gls_90", ascending=False).head(20)
fig = px.bar(goals_90, x="Player", y="Gls_90", color="Squad", text="Gls_90", title="Top 20 joueurs – Buts par 90 minutes")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Répartition des buts selon le poste")
goals_by_pos = df_filtre.groupby("Pos")["Gls"].sum().reset_index()
fig = px.pie(goals_by_pos, values="Gls", names="Pos", title="Répartition des buts par poste", hole=0.4)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Moyenne de buts par club")
goals_by_club = df_filtre.groupby("Squad")["Gls"].mean().reset_index().sort_values("Gls", ascending=False).head(20)
fig = px.bar(goals_by_club, x="Squad", y="Gls", color="Squad", text="Gls", title="Top 20 clubs – Moyenne de buts")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Comparaison du niveau moyen de performance entre les ligues")
perf_by_league = df_filtre.groupby("Comp")[["G+A", "xG", "xAG"]].mean().reset_index()
fig = px.bar(perf_by_league, x="Comp", y="G+A", text="G+A", color="Comp", title="Performance moyenne (G+A, xG, xAG)")
st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    cards_by_league = df_filtre.groupby("Comp")[["CrdY", "CrdR"]].sum().reset_index()
    fig = px.bar(cards_by_league, x="Comp", y=["CrdY", "CrdR"], barmode="group", title="Répartition des cartons par ligue")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    top_cards = df_filtre.assign(Cartons=df_filtre["CrdY"] + df_filtre["CrdR"]).sort_values("Cartons", ascending=False).head(20)
    fig = px.bar(top_cards, x="Player", y="Cartons", color="Squad", text="Cartons", title="Joueurs les plus avertis (jaunes + rouges)")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Taux d’utilisation des joueurs")
df_filtre["Taux_utilisation"] = (df_filtre["Min"] / (df_filtre["90s"] * 90)).clip(upper=1)
top_util = df_filtre.sort_values("Min", ascending=False).head(20)
fig = px.bar(top_util, x="Player", y="Min", color="Squad", text="Min", title="Top 20 joueurs les plus utilisés")
st.plotly_chart(fig, use_container_width=True)
