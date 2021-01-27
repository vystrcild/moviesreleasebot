import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from movie_details import Movie
import sys

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

url = sys.argv[1]
title = get_movie_from_csfd(url)[0]
year = get_movie_from_csfd(url)[1]
tmdb_id = get_movie_from_tmdb_by_name(title, year)

query_movie = Movie(tmdb_id)
print(query_movie.youtube_url)
