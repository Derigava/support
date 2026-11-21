#!/usr/bin/env python3
"""Download only official Derigava brand files, pinned and checked by Git blob SHA-1."""
import hashlib
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

BRAND_COMMIT = "73c06b7628e85ec3924a6d1cbae5707f5dcae8e3"
FILES = json.loads(r'''{
  "site/assets/fonts/Onest-Variable.ttf": {
    "source": "00 Основа/assets/fonts/Onest-Variable.ttf",
    "git_sha": "477cb31027450d80e486a53119641bf87dde3d4c"
  },
  "site/assets/fonts/Unbounded-Variable.ttf": {
    "source": "00 Основа/assets/fonts/Unbounded-Variable.ttf",
    "git_sha": "e3c064ddfa3acdd3af2e0f06cd2f2288cc4fcae3"
  },
  "site/assets/fonts/JetBrainsMono-Regular.ttf": {
    "source": "00 Основа/assets/fonts/JetBrainsMono-Regular.ttf",
    "git_sha": "dff66cc50702c75abd025dcf49f62a4dcc2d72de"
  },
  "site/assets/fonts/JetBrainsMono-Medium.ttf": {
    "source": "00 Основа/assets/fonts/JetBrainsMono-Medium.ttf",
    "git_sha": "97671156df256e850498054fdebcd41d74a65d6b"
  },
  "site/assets/fonts/Onest-OFL.txt": {
    "source": "00 Основа/assets/fonts/Onest-OFL.txt",
    "git_sha": "b6f4f91487900bb8f00ae991724121f1d59e30d9"
  },
  "site/assets/fonts/Unbounded-OFL.txt": {
    "source": "00 Основа/assets/fonts/Unbounded-OFL.txt",
    "git_sha": "1c7db28325aa3a1e8bd8978ef1d760daf3bb357b"
  },
  "site/assets/fonts/JetBrainsMono-OFL.txt": {
    "source": "00 Основа/assets/fonts/JetBrainsMono-OFL.txt",
    "git_sha": "5ceee0025da23d2cd5fd14b28569708a8db4db2b"
  },
  "site/assets/mark-dark-color.png": {
    "source": "00 Основа/logos/mark-dark-color.png",
    "git_sha": "b420a8708ab13581851d089a4c2b577138191c8e"
  },
  "site/assets/mark-dark-color.svg": {
    "source": "00 Основа/logos/mark-dark-color.svg",
    "git_sha": "b144e24fb20cdd54066ee590d1cb4d7f4cf56143"
  },
  "site/assets/mark-light-color.svg": {
    "source": "00 Основа/logos/mark-light-color.svg",
    "git_sha": "c672e7e876516e00f1692cb5c67ba8906ea43c26"
  },
  "site/assets/wordmark-dark-color.svg": {
    "source": "00 Основа/logos/wordmark-dark-color.svg",
    "git_sha": "24cc193a487390068092a0387d3fd8faf27466cf"
  },
  "site/assets/wordmark-light-color.svg": {
    "source": "00 Основа/logos/wordmark-light-color.svg",
    "git_sha": "db84d6061d73e941ee9176cb87f080173a85be40"
  },
  "site/tokens.css": {
    "source": "04 Управление и продажи/Командный кит/source/tokens.css",
    "git_sha": "d0cb93ccf9849b928218dca88e00fc7bfb5c5434"
  }
}''')
ROOT = Path(__file__).resolve().parents[1]

def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def main() -> None:
    for destination, entry in FILES.items():
        file = ROOT / destination
        expected = entry["git_sha"]
        if file.exists() and blob_sha(file.read_bytes()) == expected:
            print("Verified:", destination)
            continue
        url = ("https://raw.githubusercontent.com/Derigava/derigava-brand/"
               + BRAND_COMMIT + "/" + quote(entry["source"], safe="/"))
        request = Request(url, headers={"User-Agent": "Derigava-Support-Brand-Sync"})
        with urlopen(request, timeout=50) as response:
            data = response.read()
        if blob_sha(data) != expected:
            raise RuntimeError("Brand asset SHA mismatch: " + destination)
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(data)
        print("Synced:", destination)

if __name__ == "__main__":
    main()
