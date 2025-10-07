import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(
    page_title="SoccerStats Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


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
    
    .main-header p {
        color: #e8f4f8;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #1f4e79;
        margin: 1rem 0;
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
        background: linear-gradient(180deg, ##e8f4f8 0%, #e9ecef 100%);
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="main-header">
    <h1> SoccerStats Dashboard</h1>
    <p></p>
</div>
""", unsafe_allow_html=True)


df = pd.read_csv("Clean.csv")


with st.sidebar:
    st.markdown("### Filtres")
    st.markdown("---")
    
    competition = st.selectbox(
        " Compétition :", 
        sorted(df["Comp"].unique()),
        help="Sélectionnez la compétition à analyser"
    )
    
    positions = st.multiselect(
        " Positions :", 
        sorted(df["Pos"].unique()),
        help="Choisissez une ou plusieurs positions"
    )
    
    st.markdown("---")
    st.markdown("###  Informations")
    st.info(f"**Total de joueurs :** {len(df)}")


df_filtre = df[df["Comp"] == competition]
if positions:
    df_filtre = df_filtre[df_filtre["Pos"].isin(positions)]

st.markdown('<div class="section-header"> Vue d\'ensemble</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label=" Joueurs sélectionnés",
        value=len(df_filtre),
        delta=f"{len(df_filtre) - len(df[df['Comp'] == competition])}" if positions else None
    )

with col2:
    total_goals = df_filtre["Gls"].sum()
    st.metric(
        label=" Buts totaux",
        value=f"{total_goals:,}",
        delta=f"{df_filtre['Gls'].mean():.1f} moy/joueur"
    )

with col3:
    total_assists = df_filtre["Ast"].sum()
    st.metric(
        label=" Passes décisives",
        value=f"{total_assists:,}",
        delta=f"{df_filtre['Ast'].mean():.1f} moy/joueur"
    )

st.markdown('<div class="section-header"> Distribution des joueurs</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    pos_counts = df_filtre["Pos"].value_counts().reset_index()
    pos_counts.columns = ["Poste", "Joueurs"]
    
    fig = px.bar(
        pos_counts, 
        x="Poste", 
        y="Joueurs", 
        text="Joueurs",
        title=" Répartition par position",
        color="Joueurs",
        color_continuous_scale="Blues",
        template="plotly_white"
    )
    fig.update_layout(
        showlegend=False,
        font=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_size=16
    )
    fig.update_traces(textposition='outside', textfont_size=12)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    nat_counts = df_filtre["Nation"].value_counts().head(15).reset_index()
    nat_counts.columns = ["Nation", "Joueurs"]
    
    fig = px.bar(
        nat_counts, 
        x="Nation", 
        y="Joueurs", 
        text="Joueurs",
        title=" Top 15 des nationalités",
        color="Joueurs",
        color_continuous_scale="Greens",
        template="plotly_white"
    )
    fig.update_layout(
        showlegend=False,
        font=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_size=16,
        xaxis_tickangle=-45
    )
    fig.update_traces(textposition='outside', textfont_size=12)
    st.plotly_chart(fig, use_container_width=True)


st.markdown('<div class="section-header"> Performances individuelles</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    top_buteurs = df_filtre.sort_values("Gls", ascending=False).head(20)
    
    fig = px.bar(
        top_buteurs, 
        x="Player", 
        y="Gls", 
        color="Squad", 
        text="Gls", 
        title=" Top 20 buteurs",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(
        font=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_size=16,
        xaxis_tickangle=-45,
        height=500
    )
    fig.update_traces(textposition='outside', textfont_size=10)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.scatter(
        df_filtre, 
        x="xG", 
        y="Gls", 
        size="Min", 
        color="Pos", 
        hover_name="Player",
        hover_data=["Squad", "Age", "Min"],
        title=" xG vs Buts réels",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        font=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_size=16,
        height=500
    )
    fig.add_shape(
        type="line", line=dict(dash="dash", color="red"),
        x0=df_filtre["xG"].min(), x1=df_filtre["xG"].max(),
        y0=df_filtre["xG"].min(), y1=df_filtre["xG"].max()
    )
    st.plotly_chart(fig, use_container_width=True)


st.markdown('<div class="section-header"> Analyse personnalisée</div>', unsafe_allow_html=True)


st.markdown("###  Sélection de joueurs")
joueurs = st.multiselect(
    "Choisir des joueurs à analyser :", 
    df_filtre["Player"].unique(),
    help="Sélectionnez un ou plusieurs joueurs pour une analyse détaillée"
)

if joueurs:
    df_joueurs = df_filtre[df_filtre["Player"].isin(joueurs)]
    

    st.markdown("###  Statistiques des joueurs sélectionnés")
    
    col_metrics1, col_metrics2, col_metrics3, col_metrics4 = st.columns(4)
    
    with col_metrics1:
        st.metric(" Buts totaux", f"{df_joueurs['Gls'].sum()}")
    with col_metrics2:
        st.metric(" Passes décisives", f"{df_joueurs['Ast'].sum()}")
    with col_metrics3:
        st.metric(" Minutes moyennes", f"{df_joueurs['Min'].mean():.0f}")
    with col_metrics4:
        st.metric(" Âge moyen", f"{df_joueurs['Age'].mean():.1f}")

    col5, col6 = st.columns(2)
    
    with col5:
        fig = px.bar(
            df_joueurs, 
            x="Player", 
            y="Gls", 
            color="Pos", 
            text="Gls", 
            title=" Buts par joueur",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            font=dict(size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=16,
            xaxis_tickangle=-45
        )
        fig.update_traces(textposition='outside', textfont_size=12)
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        fig = px.scatter(
            df_joueurs, 
            x="Min", 
            y="Ast", 
            size="Gls", 
            color="Squad", 
            hover_name="Player",
            hover_data=["Pos", "Age", "xG"],
            title=" Minutes vs Passes décisives",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Pastel2
        )
        fig.update_layout(
            font=dict(size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)


    st.markdown("###  Détails des joueurs sélectionnés")
    

    colonnes_importantes = ["Player", "Squad", "Pos", "Age", "Gls", "Ast", "Min", "xG", "Nation"]
    df_affichage = df_joueurs[colonnes_importantes].copy()
    

    df_affichage = df_affichage.round(2)
    df_affichage = df_affichage.sort_values("Gls", ascending=False)
    
    st.dataframe(
        df_affichage,
        use_container_width=True,
        hide_index=True
    )
    

    csv = df_affichage.to_csv(index=False)
    st.download_button(
        label=" Télécharger les données des joueurs sélectionnés",
        data=csv,
        file_name=f"joueurs_selectionnes_{competition}.csv",
        mime="text/csv"
    )
    
else:
    st.info(" Sélectionnez un ou plusieurs joueurs pour voir leurs statistiques détaillées.")


st.markdown('<div class="section-header"> Données complètes</div>', unsafe_allow_html=True)


col_opt1, col_opt2 = st.columns(2)
with col_opt1:
    show_all = st.checkbox("Afficher toutes les données", value=False)
with col_opt2:
    if show_all:
        limit = st.slider("Limite d'affichage", 10, len(df_filtre), min(50, len(df_filtre)))

if show_all:
    if 'limit' in locals():
        df_affichage_complet = df_filtre.head(limit)
    else:
        df_affichage_complet = df_filtre
    
    st.dataframe(
        df_affichage_complet,
        use_container_width=True,
        hide_index=True
    )
    

    st.markdown("###  Statistiques rapides")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.metric(" Total joueurs", len(df_affichage_complet))
    with col_stat2:
        st.metric(" Buts totaux", f"{df_affichage_complet['Gls'].sum():,}")
    with col_stat3:
        st.metric(" Passes décisives", f"{df_affichage_complet['Ast'].sum():,}")


st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p> <strong>SoccerStats Dashboard</strong> - Analyse des performances de football</p>
        <p><em>Développé avec Streamlit et Plotly</em></p>
    </div>
    """, 
    unsafe_allow_html=True
)
