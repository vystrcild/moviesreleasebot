import requests
import rarbgapi
import json
import sys
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


def get_all_torrents(query):
    # Make a list of all torrent results
    rarbg = get_torrent_rarbg(query)
    yts = get_torrent_yts(query)
    torrents = rarbg + yts
    return torrents

def create_json(torrents):
    items = []
    for i in torrents:
        torrent = {
            "title": i["name"],
            "subtitle": i["url"],
            "arg": i["url"]
        }
        items.append(torrent)
    return {"items": items}

# Get data
query = sys.argv[1]
torrents = get_all_torrents(query)
json_ouput = create_json(torrents)

# Print output for Alfred Workflow
print(json.dumps(json_ouput))
