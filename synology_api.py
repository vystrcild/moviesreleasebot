import requests
import os
from dotenv import load_dotenv
import sys

load_dotenv()

url = os.environ["SYNO_URL"]
user = os.environ["SYNO_USER"]
password = os.environ["SYNO_PASS"]


def autheniticate_synology():
    # Authenticate and get session ID
    api = f"{url}/webapi/auth.cgi?api=SYNO.API.Auth&version=2&method=login&account={user}&passwd={password}" \
          f"&session=DownloadStation&format=sid"
    r = requests.get(api).json()
    sid = r["data"]["sid"]
    return sid

def download_torrent(torrent_uri):
    # Starts download on Synology server
    sid = autheniticate_synology()
    api = f"{url}/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=3&method=create" \
          f"&uri={torrent_uri}&_sid={sid}"
    r = requests.get(api).json()
    return r

torrent = sys.argv[1]
download_torrent(torrent)

# TODO - notification about starting/ending download
