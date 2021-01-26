import requests
import os
from youtube_search import YoutubeSearch
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.environ["TMDB_API_KEY"]

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/79.0.3945.117 Safari/537.36'}


class Movie:
    def __init__(self, tmdb_id):
        self.tmdb_id = tmdb_id
        self.url_tmdb_api = f"https://api.themoviedb.org/3/movie/{self.tmdb_id}?api_key={TMDB_API_KEY}"
        r = requests.get(self.url_tmdb_api).json()

        self.title = r["title"]
        self.original_title = r["original_title"]
        self.poster = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{r['poster_path']}"
        self.overview = r["overview"]
        self.original_language = r["original_language"]
        self.imdb_id = r["imdb_id"]
        self.runtime = r["runtime"]
        self.popularity = r["popularity"]
        self.vote_count = r["vote_count"]
        self.vote_average = r["vote_average"]
        self.release_date = r["release_date"]
        self.release_year = r["release_date"][:4]
        self.url_tmdb = f"https://www.themoviedb.org/movie/{tmdb_id}"
        self.genres = ", ".join([i["name"] for i in r["genres"]])
        self.country = ", ".join([i["iso_3166_1"] for i in r["production_countries"]])

        # Get cast & crew details
        cast_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits?api_key={TMDB_API_KEY}"
        r_credits = requests.get(cast_url).json()
        self.actors = ", ".join([actor["name"] for actor in r_credits["cast"][:5]])
        self.writers = ", ".join([writer["name"] for writer in r_credits["crew"] if writer["job"] == "Writer"])
        self.directors = ", ".join([direct["name"] for direct in r_credits["crew"] if direct["job"] == "Director"])

        # Get youtube_link
        search = YoutubeSearch(f"{self.title} {self.release_year} trailer", max_results=1).to_dict()[0]["id"]
        self.youtube_url = f"https://www.youtube.com/watch?v={search}"

        # Get CSFD details
        def get_csfd_url(title):
            # Check if url is on search page or movie detail
            url = f'https://www.csfd.cz/hledat/?q={title.replace(" ", "%20")}'
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.content, "html.parser")

            # If in movie detail
            if soup.find("body", id="ap-web-film"):
                pass
            # If in search
            else:
                url = f'https://www.csfd.cz{soup.find("a", class_="film")["href"]}'
            return url

        def get_csfd_details(url):
            # Get rating value, rating count and url from CSFD.cz profile
            r_movie = requests.get(url, headers=headers)
            soup = BeautifulSoup(r_movie.content, "html.parser")

            if soup.find("div", class_="count") is None:
                csfd_rating = "0.0"
                csfd_rating_count = "0"
            else:
                csfd_rating = soup.find("h2", class_="average").get_text()
                csfd_rating_count = soup.find("div", class_="count").get_text().strip()
                csfd_rating_count = re.findall("(\d)", csfd_rating_count)
                csfd_rating_count = "".join(csfd_rating_count)
            return csfd_rating, csfd_rating_count

        self.csfd_url = get_csfd_url(f"{self.title} {self.release_year}")
        self.csfd_rating, self.csfd_rating_count = get_csfd_details(self.csfd_url)

        def get_imdb_details(id):
            # Get rating value, rating count and url from IMDB profile
            imdb_url = f"https://www.imdb.com/title/{id}"
            r = requests.get(imdb_url)
            soup = BeautifulSoup(r.content, "html.parser")

            if soup.find("span", itemprop="ratingCount") is None:
                imdb_rating = "0.0"
                imdb_rating_count = "0"
            else:
                imdb_rating = soup.find("span", itemprop="ratingValue").get_text()
                imdb_rating_count = soup.find("span", itemprop="ratingCount").get_text()

            return imdb_url, imdb_rating, imdb_rating_count

        self.imdb_url, self.imdb_rating, self.imdb_rating_count = get_imdb_details(self.imdb_id)
