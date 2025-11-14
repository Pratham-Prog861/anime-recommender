import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime


def fetch_anime_data(num_pages=10, append_to_existing=True):
    """
    Fetch anime data from Jikan API
    
    Args:
        num_pages: Number of pages to fetch (25 anime per page)
        append_to_existing: If True, adds to existing anime.csv; if False, overwrites
    
    Returns:
        DataFrame with fetched anime data
    """
    anime_list = []
    base_url = "https://api.jikan.moe/v4/anime"
    
    print(f"🎌 Starting to fetch anime data...")
    print(f"📊 Pages to fetch: {num_pages} (approximately {num_pages * 25} anime)")
    print(f"{'='*50}")
    
    # Load existing data if appending
    existing_ids = set()
    if append_to_existing:
        try:
            existing_df = pd.read_csv('anime.csv')
            existing_ids = set(existing_df['anime_id'].values)
            print(f"📂 Found {len(existing_ids)} existing anime entries")
        except FileNotFoundError:
            print("📂 No existing file found, creating new database")
    
    success_count = 0
    duplicate_count = 0
    
    for page in range(1, num_pages + 1):
        try:
            print(f"\n🔄 Fetching page {page}/{num_pages}...")
            response = requests.get(f"{base_url}?page={page}&limit=25&order_by=popularity")
            
            if response.status_code == 200:
                data = response.json()
                
                for anime in data['data']:
                    anime_id = anime['mal_id']
                    
                    # Skip if already exists
                    if anime_id in existing_ids:
                        duplicate_count += 1
                        continue
                    
                    anime_entry = {
                        'anime_id': anime_id,
                        'name': anime['title'],
                        'score': anime.get('score', 0) if anime.get('score') else 0,
                        'genres': ', '.join([g['name'] for g in anime.get('genres', [])]) if anime.get('genres') else '',
                        'type': anime.get('type', 'Unknown'),
                        'episodes': anime.get('episodes', 0) if anime.get('episodes') else 0,
                        'members': anime.get('members', 0),
                        'synopsis': anime.get('synopsis', ''),
                        'image_url': anime['images']['jpg']['image_url']
                    }
                    
                    anime_list.append(anime_entry)
                    existing_ids.add(anime_id)
                    success_count += 1
                
                print(f"✅ Page {page} complete! Added {success_count} new anime (Skipped {duplicate_count} duplicates)")
                time.sleep(1)  # Rate limiting - respect the API
                
            elif response.status_code == 429:
                print(f"⏸️  Rate limited. Waiting 60 seconds...")
                time.sleep(60)
                continue
            else:
                print(f"⚠️  Error on page {page}: Status code {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error on page {page}: {e}")
            continue
    
    print(f"\n{'='*50}")
    print(f"📊 Fetch Summary:")
    print(f"  ✅ New anime added: {success_count}")
    print(f"  ⏭️  Duplicates skipped: {duplicate_count}")
    
    # Save data
    if anime_list:
        new_df = pd.DataFrame(anime_list)
        
        if append_to_existing:
            try:
                existing_df = pd.read_csv('anime.csv')
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                combined_df.drop_duplicates(subset=['anime_id'], keep='first', inplace=True)
                combined_df.to_csv('anime.csv', index=False)
                print(f"💾 Updated anime.csv - Total anime: {len(combined_df)}")
                return combined_df
            except FileNotFoundError:
                new_df.to_csv('anime.csv', index=False)
                print(f"💾 Created new anime.csv with {len(new_df)} anime")
                return new_df
        else:
            new_df.to_csv('anime.csv', index=False)
            print(f"💾 Saved {len(new_df)} anime to anime.csv (overwrite mode)")
            return new_df
    else:
        print("⚠️  No new anime to save")
        return None


def fetch_top_anime(limit=100):
    """
    Fetch top-rated anime
    
    Args:
        limit: Number of top anime to fetch
    """
    print(f"🏆 Fetching top {limit} anime...")
    num_pages = (limit // 25) + 1
    return fetch_anime_data(num_pages=num_pages, append_to_existing=True)


def fetch_by_genre(genre, num_pages=5):
    """
    Fetch anime by specific genre
    
    Args:
        genre: Genre name (e.g., 'Action', 'Comedy')
        num_pages: Number of pages to fetch
    """
    anime_list = []
    base_url = "https://api.jikan.moe/v4/anime"
    
    # Genre IDs (you can find more at https://api.jikan.moe/v4/genres/anime)
    genre_map = {
        'Action': 1, 'Adventure': 2, 'Comedy': 4, 'Drama': 8,
        'Fantasy': 10, 'Horror': 14, 'Romance': 22, 'Sci-Fi': 24,
        'Sports': 30, 'Supernatural': 37, 'Thriller': 41
    }
    
    genre_id = genre_map.get(genre)
    if not genre_id:
        print(f"❌ Genre '{genre}' not found. Available: {list(genre_map.keys())}")
        return None
    
    print(f"🎭 Fetching {genre} anime...")
    
    for page in range(1, num_pages + 1):
        try:
            response = requests.get(f"{base_url}?genres={genre_id}&page={page}&limit=25")
            if response.status_code == 200:
                data = response.json()
                for anime in data['data']:
                    anime_list.append({
                        'anime_id': anime['mal_id'],
                        'name': anime['title'],
                        'score': anime.get('score', 0) if anime.get('score') else 0,
                        'genres': ', '.join([g['name'] for g in anime.get('genres', [])]) if anime.get('genres') else '',
                        'type': anime.get('type', 'Unknown'),
                        'episodes': anime.get('episodes', 0) if anime.get('episodes') else 0,
                        'members': anime.get('members', 0),
                        'synopsis': anime.get('synopsis', ''),
                        'image_url': anime['images']['jpg']['image_url']
                    })
                print(f"✅ Fetched page {page}")
                time.sleep(1)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    if anime_list:
        # Append to existing
        new_df = pd.DataFrame(anime_list)
        try:
            existing_df = pd.read_csv('anime.csv')
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.drop_duplicates(subset=['anime_id'], keep='first', inplace=True)
            combined_df.to_csv('anime.csv', index=False)
            print(f"💾 Added {len(new_df)} {genre} anime. Total: {len(combined_df)}")
        except FileNotFoundError:
            new_df.to_csv('anime.csv', index=False)
            print(f"💾 Created new file with {len(new_df)} anime")
    
    return pd.DataFrame(anime_list)


def show_stats():
    """Display statistics about current anime database"""
    try:
        df = pd.read_csv('anime.csv')
        
        # Handle NaN values in genres column
        df['genres'] = df['genres'].fillna('')  # Replace NaN with empty string
        
        print(f"\n{'='*50}")
        print(f"📊 ANIME DATABASE STATISTICS")
        print(f"{'='*50}")
        print(f"📚 Total Anime: {len(df)}")
        print(f"⭐ Average Score: {df['score'].mean():.2f}")
        print(f"📺 Total Episodes: {int(df['episodes'].sum()):,}")
        
        # Safely extract unique genres by filtering out empty strings and NaN
        unique_genres = set()
        for genres in df['genres']:
            if genres and isinstance(genres, str):  # Check if not empty and is string
                for g in genres.split(','):
                    genre = g.strip()
                    if genre:  # Only add non-empty genres
                        unique_genres.add(genre)
        
        print(f"🎭 Unique Genres: {len(unique_genres)}")
        
        print(f"\n📊 Anime by Type:")
        print(df['type'].value_counts().to_string())
        
        # Show top 5 most common genres
        genre_counts = {}
        for genres in df['genres']:
            if genres and isinstance(genres, str):
                for genre in genres.split(','):
                    genre = genre.strip()
                    if genre:
                        genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        if genre_counts:
            print(f"\n🎭 Top 5 Genres:")
            sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            for genre, count in sorted_genres:
                print(f"  {genre}: {count}")
        
        print(f"{'='*50}\n")
    except FileNotFoundError:
        print("❌ No anime.csv file found!")
    except Exception as e:
        print(f"❌ Error reading stats: {e}")


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════╗
    ║   🎌 ANIME DATA FETCHER                      ║
    ║   Powered by Jikan API (MyAnimeList)         ║
    ╚═══════════════════════════════════════════════╝
    
    Choose an option:
    1. Fetch more anime (append to existing)
    2. Fetch top-rated anime
    3. Fetch by genre
    4. Show current database stats
    5. Replace entire database (careful!)
    """)
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "1":
        pages = int(input("How many pages to fetch? (25 anime per page): "))
        fetch_anime_data(num_pages=pages, append_to_existing=True)
    elif choice == "2":
        limit = int(input("How many top anime? (e.g., 100): "))
        fetch_top_anime(limit=limit)
    elif choice == "3":
        print("Available genres: Action, Adventure, Comedy, Drama, Fantasy, Horror, Romance, Sci-Fi, Sports, Supernatural, Thriller")
        genre = input("Enter genre name: ").strip()
        pages = int(input("How many pages? "))
        fetch_by_genre(genre, num_pages=pages)
    elif choice == "4":
        show_stats()
    elif choice == "5":
        confirm = input("⚠️  This will DELETE all existing data! Type 'YES' to confirm: ")
        if confirm == "YES":
            pages = int(input("How many pages to fetch? "))
            fetch_anime_data(num_pages=pages, append_to_existing=False)
        else:
            print("Cancelled.")
    else:
        print("Invalid choice!")
    
    # Always show stats at the end if not just showing stats
    if choice != "4":
        show_stats()
