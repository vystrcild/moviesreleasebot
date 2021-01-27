import requests
import rarbgapi
# TODO: https://darksearch.io/apidoc

def get_torrent_yts(query):
    # List all query results from YTS.mx
    url = f"https://yts.mx/api/v2/list_movies.json?query_term={query}"
    r = requests.get(url).json()
    for movie in r["data"]["movies"]:
        title = movie["title"]
        year = movie["year"]
        print(title, year)

def get_torrent_rarbg(query):
    # List all query results from RARBG.to
    client = rarbgapi.RarbgAPI()
    search = client.search(search_string=query, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_H264_1080P])
    for movie in search:
        print(movie.download, movie.filename)

get_torrent_rarbg("Terminator 2 1991")
