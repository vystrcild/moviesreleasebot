import requests
import rarbgapi
# TODO: https://darksearch.io/apidoc

def get_torrent_yts(query):
    # List all query results from YTS.mx
    url = f"https://yts.mx/api/v2/list_movies.json?query_term={query}"
    r = requests.get(url).json()
    results = []
    for movie in r["data"]["movies"]:
        title = movie["title"]
        year = movie["year"]
        for torrent in movie["torrents"]:
            if torrent["quality"] == "1080p":
                torrent_url = torrent["url"]
                size = torrent["size"]
        torrent_name = f"{title} - {year} - {size}"
        results.append({"name":torrent_name, "url":torrent_url})
    return results


def get_torrent_rarbg(query):
    # List all query results from RARBG.to
    client = rarbgapi.RarbgAPI()
    search = client.search(search_string=query, categories=[rarbgapi.RarbgAPI.CATEGORY_MOVIE_H264_1080P])
    results = []
    for torrent in search:
        results.append({"name": torrent.filename, "url": torrent.download})
    return results

print(get_torrent_rarbg("Soul 2020"))
