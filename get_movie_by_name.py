import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from movie_details import Movie
import sys
import json

load_dotenv()

TMDB_API_KEY = os.environ["TMDB_API_KEY"]

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/79.0.3945.117 Safari/537.36'}

def get_movie_from_tmdb_by_name(title, year):
    url_api = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&language=en-US&query={title}&page=1&include_adult=false&year={year}"
    r = requests.get(url_api).json()
    movie_id = r["results"][0]["id"]
    return movie_id

def get_movie_from_csfd(url):
    r_movie = requests.get(url, headers=headers)
    soup = BeautifulSoup(r_movie.content, "html.parser")
    title = soup.find("ul", class_="names").find("li").find("h3").get_text().strip()
    year = soup.find("p", class_="origin").find("span").get_text()
    return title, year

# Script input
url = sys.argv[1]

# Get movie details from CSFD
title = get_movie_from_csfd(url)[0]
year = get_movie_from_csfd(url)[1]
tmdb_id = get_movie_from_tmdb_by_name(title, year)

# Create movie
query_movie = Movie(tmdb_id)

# Output for Alfred - List Script feature
json_ouput = {"items": [
    {
        "uid": "youtube",
        "title": "Watch YouTube Trailer",
        "subtitle": f"{query_movie.title} {query_movie.release_year} Trailer",
        "arg": query_movie.youtube_url,
        "icon": {
            "path": "youtube.png"
        }
    },
        {
            "uid": "watchlist",
            "title": "Add To Watchlist",
            "subtitle": f"{query_movie.title} {query_movie.release_year}",
            "arg": "MOVIE ID",
            "icon": {
                "path": "watchlist.png"
            }
        },
    {
            "uid": "torrent",
            "title": "Get Torrent",
            "subtitle": f"{query_movie.title} {query_movie.release_year}",
            "arg": "MOVIE ID",
            "icon": {
                "path": "torrent.png"
            }
        }
    ]}

# Print output for Alfred Workflow
print(json.dumps(json_ouput))
