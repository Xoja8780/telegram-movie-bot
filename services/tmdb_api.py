# Работа с API TMDB
import requests
from config import API_KEY

def get_movies_by_genre(genre_id):
    """Получает список фильмов по жанру из TMDB API."""
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=ru-RU&with_genres={genre_id}&page=1"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("results", [])

def get_movie_videos(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}&language=ru-RU"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("results", [])

def get_youtube_trailer_url(movie_id):
    videos = get_movie_videos(movie_id)
    for prefer in ("Trailer", "Teaser"):
        for v in videos:
            if v.get("site") == "YouTube" and v.get("type") == prefer:
                return f"https://www.youtube.com/watch?v={v.get('key')}"
    for v in videos:
        if v.get("site") == "YouTube":
            return f"https://www.youtube.com/watch?v={v.get('key')}"
    return None


