# 🎌 Anime Recommender System

An AI-powered anime recommendation system built with Streamlit, featuring content-based filtering and Google Gemini AI integration for personalized anime suggestions.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **🎯 Smart Recommendations**: Content-based filtering using TF-IDF and Cosine Similarity
- **🤖 AI Assistant**: Powered by Google Gemini AI for detailed, personalized recommendations
- **📊 Browse & Filter**: Search and filter anime by genre, type, score, and more
- **📈 Statistics**: Interactive visualizations of anime data
- **🎨 Modern UI**: Clean, responsive design with smooth animations
- **⚡ Fast Search**: Real-time search with autocomplete suggestions

## 🚀 Demo

### Recommendations Tab

Get similar anime based on content similarity with match percentages.

### AI Assistant Tab

Get AI-powered recommendations with detailed explanations, genres, ratings, and episode counts.

### Browse Tab

Filter and explore the entire anime database with advanced search options.

### Stats Tab

Visualize anime statistics with interactive charts and graphs.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key (for AI recommendations)

## 🛠️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/pratham-prog861/anime-recommender.git
cd anime-recommender
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up Gemini API key**

Create a `.streamlit/secrets.toml` file:

```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

5. **Fetch anime data** (optional - if you want to update the database)

```bash
python fetch_anime_data.py
```

## 🎮 Usage

1. **Start the application**

```bash
streamlit run app.py
```

2. **Open your browser**

   Navigate to `http://localhost:8501`

3. **Explore the features**
   - **Recommendations**: Type an anime name and get similar recommendations
   - **AI Assistant**: Get AI-powered recommendations with detailed explanations
   - **Browse**: Filter and search through the anime database
   - **Stats**: View interactive statistics and visualizations

## 📁 Project Structure

```bash
anime-recommender/
├── app.py                      # Main Streamlit application
├── recommender.py              # Recommendation engine
├── fetch_anime_data.py         # Data fetching script
├── anime.csv                   # Anime database
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── secrets.toml           # API keys (not in git)
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## 🔧 Configuration

### Gemini API Configuration

The AI Assistant uses Google's Gemini API. Configure it in `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-api-key"
```

### Fetching More Anime Data

To update or expand the anime database:

```bash
python fetch_anime_data.py
```

Options:

1. Fetch more anime (append to existing)
2. Fetch top-rated anime
3. Fetch by genre
4. Show current database stats
5. Replace entire database

## 🧠 How It Works

### Content-Based Filtering

1. **TF-IDF Vectorization**: Converts anime features (genres, type) into numerical vectors
2. **Cosine Similarity**: Measures similarity between anime based on their feature vectors
3. **Recommendation Engine**: Returns top N most similar anime with similarity scores

### AI Recommendations

1. Uses Google Gemini AI to analyze anime preferences
2. Provides detailed recommendations with:
   - Anime name
   - Genres
   - Rating (MAL score)
   - Episode count
   - Story description and similarity explanation

## 📊 Data Source

Anime data is fetched from [MyAnimeList](https://myanimelist.net) via the [Jikan API](https://jikan.moe) - an unofficial MyAnimeList API.

## 🛡️ Rate Limiting

The Gemini API has rate limits. If you encounter a 429 error:

- Wait 1-2 minutes before trying again
- Use the regular Recommendations tab (doesn't use AI)
- The app includes automatic retry logic with delays

## 🎨 Technologies Used

- **[Streamlit](https://streamlit.io/)**: Web application framework
- **[Scikit-learn](https://scikit-learn.org/)**: Machine learning (TF-IDF, Cosine Similarity)
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation
- **[Plotly](https://plotly.com/)**: Interactive visualizations
- **[Google Gemini AI](https://ai.google.dev/)**: AI-powered recommendations
- **[Jikan API](https://jikan.moe/)**: Anime data source

## 📝 Requirements

```bash
streamlit
pandas
numpy
scikit-learn
requests
plotly
matplotlib
seaborn
google-generativeai
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [MyAnimeList](https://myanimelist.net) for anime data
- [Jikan API](https://jikan.moe) for providing the API
- [Google Gemini](https://aistudio.google.com/) for AI capabilities
- [Streamlit](https://streamlit.io/) for the amazing framework

## 📧 Contact

Project Link: [https://github.com/pratham-prog861/anime-recommender](https://github.com/pratham-prog861/anime-recommender)

## 🐛 Known Issues

- Gemini API rate limiting may occur with frequent requests
- Large anime databases may slow down initial load time

---

Made with ❤️ by Pratham
