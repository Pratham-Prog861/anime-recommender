import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from recommender import AnimeRecommender

# Page config
st.set_page_config(
    page_title="Anime Recommender",
    page_icon="🎌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize recommender
@st.cache_resource
def load_recommender():
    return AnimeRecommender('anime.csv')

recommender = load_recommender()

# Modern CSS styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Title styling */
    h1 {
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* Stat cards */
    .stat-card {
        background: linear-gradient(135deg, #667eea15, #764ba215);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
    }
    
    /* Anime cards */
    .anime-card {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .anime-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 24px rgba(102,126,234,0.2);
        transform: translateY(-2px);
    }
    
    /* Match badge */
    .match-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Score badge */
    .score-badge {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.2s;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-color: transparent;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
        background: rgba(255,255,255,0.05);
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 1px #667eea;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 4rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        color: rgba(255,255,255,0.6);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .anime-card, .stat-card {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>🎌 Anime Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1em; color: rgba(255,255,255,0.7); margin-bottom: 2rem;'>Discover your next favorite anime with AI</p>", unsafe_allow_html=True)

# Stats
col1, col2, col3, col4 = st.columns(4)
all_genres = set()
for genres in recommender.df['genres'].dropna():
    all_genres.update([g.strip() for g in genres.split(',')])

with col1:
    st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size: 2.5em; margin-bottom: 0.5rem;'>📚</div>
            <div style='font-size: 2em; font-weight: 700; margin-bottom: 0.25rem;'>{len(recommender.df):,}</div>
            <div style='font-size: 0.9em; opacity: 0.8;'>Anime</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size: 2.5em; margin-bottom: 0.5rem;'>⭐</div>
            <div style='font-size: 2em; font-weight: 700; margin-bottom: 0.25rem;'>{recommender.df['score'].mean():.1f}</div>
            <div style='font-size: 0.9em; opacity: 0.8;'>Avg Score</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size: 2.5em; margin-bottom: 0.5rem;'>🎭</div>
            <div style='font-size: 2em; font-weight: 700; margin-bottom: 0.25rem;'>{len(all_genres)}</div>
            <div style='font-size: 0.9em; opacity: 0.8;'>Genres</div>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size: 2.5em; margin-bottom: 0.5rem;'>📺</div>
            <div style='font-size: 2em; font-weight: 700; margin-bottom: 0.25rem;'>{int(recommender.df['episodes'].sum()):,}</div>
            <div style='font-size: 0.9em; opacity: 0.8;'>Episodes</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Recommendations", "🤖 AI Assistant", "📊 Browse", "📈 Stats"])

with tab1:
    st.markdown("### Find similar anime based on what you love")
    st.markdown("")
    
    # Initialize session state
    if 'rec_results' not in st.session_state:
        st.session_state.rec_results = None
    if 'rec_anime_name' not in st.session_state:
        st.session_state.rec_anime_name = ""
    if 'rec_search_value' not in st.session_state:
        st.session_state.rec_search_value = ""
    
    col1, col2 = st.columns([4, 1])
    with col1:
        anime_search = st.text_input(
            "Type anime name", 
            placeholder="e.g., Naruto, One Piece, Death Note...",
            key="rec_search_input",
            label_visibility="collapsed",
            value=st.session_state.rec_search_value
        )
    with col2:
        num_recs = st.selectbox("Results", [5, 10, 15, 20], index=1, label_visibility="collapsed")
    
    # Button to trigger search
    if st.button("Get Recommendations", type="primary", width='stretch', key="rec_btn"):
        if anime_search:
            search_results = recommender.search_anime(anime_search)
            
            if len(search_results) > 0:
                selected_anime = search_results.iloc[0]['name']
                st.session_state.rec_anime_name = selected_anime
                st.session_state.rec_search_value = anime_search
                
                with st.spinner("Analyzing similarities..."):
                    recommendations = recommender.get_recommendations(selected_anime, num_recs)
                    st.session_state.rec_results = recommendations
                st.rerun()
            else:
                st.warning(f"❌ No anime found matching '{anime_search}'")
                st.session_state.rec_results = None
    
    # Display results
    if st.session_state.rec_results is not None and len(st.session_state.rec_results) > 0:
        st.markdown("---")
        st.markdown(f"#### Because you liked **{st.session_state.rec_anime_name}**")
        st.markdown("")
        
        for idx, row in st.session_state.rec_results.iterrows():
            match_percent = round(row['similarity_score'] * 100, 1)
            episodes = int(row['episodes']) if pd.notna(row['episodes']) else 'Unknown'
            
            st.markdown(f"""
            <div class='anime-card'>
                <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                    <div style='flex: 1;'>
                        <h3 style='margin: 0 0 0.75rem 0;'>{row['name']}</h3>
                        <p style='margin: 0.5rem 0; opacity: 0.8;'><strong>Genres:</strong> {row['genres']}</p>
                        <p style='margin: 0.5rem 0; opacity: 0.8;'>{row['type']} • {episodes} episodes • <span class='score-badge'>⭐ {row['score']}</span></p>
                    </div>
                    <div class='match-badge'>{match_percent}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")
        if st.button("🔄 Search Another Anime", key="rec_clear", width='stretch'):
            st.session_state.rec_results = None
            st.session_state.rec_anime_name = ""
            st.session_state.rec_search_value = ""
            st.rerun()
    
    # Show suggestions
    elif anime_search and len(anime_search) >= 2:
        search_results = recommender.search_anime(anime_search)
        if len(search_results) > 0:
            st.markdown("**Quick suggestions:**")
            suggestions = search_results['name'].head(6).tolist()
            st.caption(", ".join(suggestions))

with tab2:
    st.markdown("### Get AI-powered recommendations with explanations")
    st.markdown("")
    
    # Initialize session state
    if 'ai_results' not in st.session_state:
        st.session_state.ai_results = None
    if 'ai_anime_name' not in st.session_state:
        st.session_state.ai_anime_name = ""
    if 'ai_search_value' not in st.session_state:
        st.session_state.ai_search_value = ""
    
    ai_search = st.text_input(
        "Type anime name", 
        placeholder="e.g., Death Note, Attack on Titan, Naruto...",
        key="ai_search_input",
        label_visibility="collapsed",
        value=st.session_state.ai_search_value
    )
    
    # Button to trigger AI search
    if st.button("Get AI Recommendations", type="primary", width='stretch', key="ai_btn"):
        if ai_search:
            search_results = recommender.search_anime(ai_search)
            
            if len(search_results) > 0:
                selected_anime = search_results.iloc[0]['name']
                st.session_state.ai_anime_name = selected_anime
                st.session_state.ai_search_value = ai_search
                
                with st.spinner("🤖 AI is analyzing and generating recommendations..."):
                    try:
                        recommendations = recommender.get_gemini_recommendations(selected_anime)
                        st.session_state.ai_results = recommendations
                    except Exception as e:
                        st.session_state.ai_results = f"error:{str(e)}"
                st.rerun()
            else:
                st.warning(f"❌ No anime found matching '{ai_search}'")
                st.session_state.ai_results = None
    
    # Display results
    if st.session_state.ai_results:
        if st.session_state.ai_results.startswith("error:"):
            error_msg = st.session_state.ai_results.replace("error:", "")
            st.error(f"❌ AI recommendation failed: {error_msg}")
            
            if "429" in error_msg or "rate limit" in error_msg.lower():
                st.warning("⏰ **Rate Limit Reached**")
                st.info("""
                The Gemini API has a rate limit. Please:
                - Wait 1-2 minutes before trying again
                - Or use the regular Recommendations tab (doesn't use AI)
                """)
        else:
            st.markdown("---")
            st.markdown("### 🎬 AI Recommendations")
            st.markdown(st.session_state.ai_results)
            st.markdown("---")
            st.success("✨ Recommendations generated successfully!")
            
            st.markdown("")
            if st.button("🔄 Search Another Anime", key="ai_clear", width='stretch'):
                st.session_state.ai_results = None
                st.session_state.ai_anime_name = ""
                st.session_state.ai_search_value = ""
                st.rerun()
    
    # Show suggestions
    elif ai_search and len(ai_search) >= 2:
        search_results = recommender.search_anime(ai_search)
        if len(search_results) > 0:
            st.markdown("**Quick suggestions:**")
            suggestions = search_results['name'].head(6).tolist()
            st.caption(", ".join(suggestions))

with tab3:
    st.markdown("### Browse and filter anime database")
    st.markdown("")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    # Get unique genres
    genre_set = set()
    for genres in recommender.df['genres'].dropna():
        genre_set.update([g.strip() for g in genres.split(',')])
    genre_list = sorted(list(genre_set))
    
    with col1:
        search_term = st.text_input("Search", placeholder="Name or genre...", label_visibility="collapsed")
    with col2:
        selected_genre = st.selectbox("Genre", ["All"] + genre_list, label_visibility="collapsed")
    with col3:
        anime_type = st.selectbox("Type", ["All", "TV", "Movie", "OVA", "Special", "ONA"], label_visibility="collapsed")
    with col4:
        sort_by = st.selectbox("Sort by", ["score", "members", "name"], label_visibility="collapsed")
    
    # Apply filters
    filtered_df = recommender.df.copy()
    
    if search_term:
        filtered_df = recommender.search_anime(search_term)
    if selected_genre != "All":
        filtered_df = filtered_df[filtered_df['genres'].str.contains(selected_genre, case=False, na=False)]
    if anime_type != "All":
        filtered_df = filtered_df[filtered_df['type'] == anime_type]
    
    # Sort
    if sort_by == "name":
        filtered_df = filtered_df.sort_values(sort_by, ascending=True)
    else:
        filtered_df = filtered_df.sort_values(sort_by, ascending=False)
    
    st.markdown(f"**{len(filtered_df)}** anime found")
    
    # Display
    st.dataframe(
        filtered_df[['name', 'score', 'genres', 'type', 'episodes', 'members']].head(100),
        width='stretch',
        height=500
    )
    
    if len(filtered_df) > 100:
        st.info(f"Showing first 100 of {len(filtered_df)} results")
    
    # Download
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        "Download CSV",
        data=csv,
        file_name="anime_results.csv",
        mime="text/csv",
        width='stretch'
    )

with tab4:
    st.markdown("### Database statistics and visualizations")
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Genre distribution
        genre_counts = {}
        for genres in recommender.df['genres'].dropna():
            for genre in genres.split(','):
                genre = genre.strip()
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        genre_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Count'])
        genre_df = genre_df.sort_values('Count', ascending=False).head(12)
        
        fig1 = px.bar(
            genre_df, 
            x='Count', 
            y='Genre', 
            orientation='h',
            color='Count',
            color_continuous_scale='purples'
        )
        fig1.update_layout(
            title="Top Genres",
            showlegend=False,
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig1, width='stretch')
    
    with col2:
        # Type distribution
        type_counts = recommender.df['type'].value_counts()
        
        fig2 = px.pie(
            values=type_counts.values, 
            names=type_counts.index,
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Purples_r
        )
        fig2.update_layout(
            title="Anime Types",
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig2, width='stretch')
    
    # Score distribution
    fig3 = px.histogram(
        recommender.df, 
        x='score', 
        nbins=25,
        color_discrete_sequence=['#667eea']
    )
    fig3.update_layout(
        title="Score Distribution",
        xaxis_title="Score",
        yaxis_title="Count",
        showlegend=False,
        height=350,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig3, width='stretch')
    
    # Top rated
    st.markdown("#### Top Rated Anime")
    top_n = st.slider("Number of anime", 5, 30, 10, label_visibility="collapsed")
    top_anime = recommender.get_top_anime(top_n)
    st.dataframe(top_anime, width='stretch', height=350)

# Footer
st.markdown("""
<div class='footer'>
    <p style='font-size: 0.9em; margin-bottom: 0.5rem;'>Built with Streamlit • Powered by Gemini AI & Jikan API</p>
    <p style='font-size: 0.8em;'>Content-based filtering using TF-IDF & Cosine Similarity</p>
</div>
""", unsafe_allow_html=True)
