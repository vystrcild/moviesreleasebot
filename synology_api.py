import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = os.environ["SYNO_URL"]
user = os.environ["SYNO_USER"]
password = os.environ["SYNO_PASS"]

torrent = "magnet:?xt=urn:btih:07da57688cc8bcf4a2645a20a3794fee610f3143&dn=Terminator.2.Judgment.Day.1991.DC.1080p.BluRay.x264.DTS-FGT&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2710&tr=udp%3A%2F%2F9.rarbg.to%3A2710&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce"

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

download_torrent(torrent)

# TODO - notification about starting/ending download