import json
import requests
import ssl
import datetime
from get_top_releases import get_top_releases
from movie_details import Movie
from dotenv import load_dotenv
import os

load_dotenv()

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]
ssl._create_default_https_context = ssl._create_unverified_context

today = datetime.date.today()
movies = get_top_releases(today)

for i in movies[:5]:
    movie = Movie(i)

    payload = {
        "type": "home",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "New releases for today:"
                }
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": movie.title + " (" + movie.release_year + ")"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": movie.genres + "\n" + movie.country + " (" + str(movie.runtime) +
                            " m) \n *Director:* " + movie.directors + "\n *Writers:* " + movie.writers + " \n *Cast:* " +
                            movie.actors + " \n\n" + movie.overview + " \n "
                },
                "accessory": {
                    "type": "image",
                    "image_url": movie.poster,
                    "alt_text": "alt text for image"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://img.csfd.cz/assets/b1645/images/favicon.ico",
                        "alt_text": "csfd"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "<" + movie.csfd_url + "|*" + movie.csfd_rating + "*> (" +
                                str(movie.csfd_rating_count) + ")"
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://m.media-amazon.com/images/G/01/imdb/images-ANDW73HA/favicon_desktop_32x32"
                                     "._CB1582158068_.png",
                        "alt_text": "imdb"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "<" + movie.imdb_url + "|*" + movie.imdb_rating + "*> (" +
                                str(movie.imdb_rating_count) + ")"
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://www.themoviedb.org/assets/2/favicon-32x32-543a21832c8931d3494a68881f6afcafc58e96c5d324345377f3197a37b367b5.png",
                        "alt_text": "tmdb"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "<" + movie.url_tmdb + "|*" + str(movie.vote_average) + "*> (" +
                                str(movie.vote_count) + ")"
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://www.youtube.com/s/desktop/ba104690/img/favicon.ico",
                        "alt_text": "youtube"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "<" + movie.youtube_url + "|*Trailer*>"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]
    }

    response = requests.post(
        SLACK_WEBHOOK, data=json.dumps(payload),
        headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
