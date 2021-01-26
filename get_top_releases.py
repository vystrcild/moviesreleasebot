import requests
from dotenv import load_dotenv
import os

load_dotenv()

TMDB_API_KEY = os.environ["TMDB_API_KEY"]

def get_top_releases(date):
    # Find top movies with specific release day
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}"\
          f"&primary_release_date.gte={date}&primary_release_date.lte={date}"
    r = requests.get(url).json()["results"]
    movie_ids = [movie["id"] for movie in r]
    return movie_ids
