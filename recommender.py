import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import google.generativeai as genai
import streamlit as st

class AnimeRecommender:
    def __init__(self, data_path='anime.csv'):
        """Initialize recommender with anime data"""
        self.df = pd.read_csv(data_path)
        self.df = self.df.dropna(subset=['name', 'genres'])
        self.df['score'] = pd.to_numeric(self.df['score'], errors='coerce').fillna(0)
        self.similarity_matrix = None
        self._build_model()
        self._configure_gemini()

    def _configure_gemini(self):
        """Configure the Gemini API."""
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        except Exception as e:
            print(f"Error configuring Gemini: {e}")

    def _build_model(self):
        """Build content-based recommendation model"""
        # Create feature combining genres and type
        self.df['features'] = self.df['genres'] + ' ' + self.df['type'].fillna('')
        
        # TF-IDF Vectorization
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.df['features'])
        
        # Calculate cosine similarity
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        print("Recommendation model built successfully!")
    
    def get_recommendations(self, anime_name, top_n=10):
        """Get top N similar anime recommendations"""
        # Find anime index
        try:
            idx = self.df[self.df['name'].str.lower() == anime_name.lower()].index[0]
        except:
            return None
        
        # Get similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]  # Exclude itself
        
        # Get anime indices
        anime_indices = [i[0] for i in sim_scores]
        
        # Return recommendations with similarity scores
        recommendations = self.df.iloc[anime_indices].copy()
        recommendations['similarity_score'] = [i[1] for i in sim_scores]
        
        return recommendations[['name', 'genres', 'score', 'episodes', 'type', 'similarity_score']]
    
    def get_gemini_recommendations(self, anime_name):
        """
        Generates anime recommendations using the Gemini API with detailed information.
        """
        import time
        
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Get anime info from database if available
            anime_info = self.df[self.df['name'].str.lower() == anime_name.lower()]
            if len(anime_info) > 0:
                genres = anime_info.iloc[0]['genres']
                anime_type = anime_info.iloc[0]['type']
                context = f"The user likes '{anime_name}' which is a {anime_type} anime with genres: {genres}."
            else:
                context = f"The user is interested in the anime '{anime_name}'."
            
            prompt = f"""
            {context}
            
            Recommend 5 similar anime that the user would enjoy. For each recommendation, provide:
            
            1. **Anime Name** (in bold)
            2. **Genres**: List the main genres
            3. **Rating**: Approximate MAL score (e.g., 8.5/10)
            4. **Episodes**: Number of episodes or "Ongoing"
            5. **Story**: A compelling 2-3 sentence description explaining why it's similar and what makes it great
            
            Format each recommendation like this:
            
            ### 1. **[Anime Name]**
            **Genres**: [Genre1, Genre2, Genre3]  
            **Rating**: [X.X/10] | **Episodes**: [Number]
            
            [Story description explaining why it's similar to {anime_name} and what makes it compelling]
            
            ---
            
            Make the recommendations diverse but thematically similar. Focus on quality anime with good ratings.
            """
            
            # Add retry logic for rate limiting
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    response = model.generate_content(prompt)
                    return response.text
                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str or "rate limit" in error_str.lower():
                        if attempt < max_retries - 1:
                            time.sleep(2)  # Wait 2 seconds before retry
                            continue
                    raise e
                    
        except Exception as e:
            return f"An error occurred: {e}"

    def search_anime(self, query):
        """Search anime by name or genre"""
        if not query:
            return self.df
        
        query = query.lower()
        mask = (
            self.df['name'].str.lower().str.contains(query, na=False) |
            self.df['genres'].str.lower().str.contains(query, na=False)
        )
        return self.df[mask]
    
    def filter_anime(self, genre=None, min_score=0, max_episodes=None, anime_type=None):
        """Filter anime by criteria"""
        filtered = self.df.copy()
        
        if genre:
            filtered = filtered[filtered['genres'].str.contains(genre, case=False, na=False)]
        if min_score > 0:
            filtered = filtered[filtered['score'] >= min_score]
        if max_episodes:
            filtered = filtered[filtered['episodes'] <= max_episodes]
        if anime_type:
            filtered = filtered[filtered['type'] == anime_type]
        
        return filtered.sort_values('score', ascending=False)
    
    def get_top_anime(self, n=10):
        """Get top rated anime"""
        return self.df.nlargest(n, 'score')[['name', 'score', 'genres', 'episodes', 'type']]
    
    def get_all_anime_names(self):
        """Get list of all anime names for autocomplete"""
        return self.df['name'].tolist()

