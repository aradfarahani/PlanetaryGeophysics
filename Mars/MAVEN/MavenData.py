import requests
from bs4 import BeautifulSoup
import os
import time

base_url = "https://spdf.gsfc.nasa.gov/pub/data/maven/mag/l2/sunstate-1sec/cdfs/"

def get_links(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    # Return hrefs that don't start with ../ (skip parent links)
    links = [a['href'] for a in soup.find_all('a') if not a['href'].startswith('../')]
    return links

def download_file(file_url, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    local_filename = os.path.join(dest_folder, file_url.split('/')[-1])
    if os.path.exists(local_filename):
        print(f"Already downloaded {local_filename}")
        return
    print(f"Downloading {file_url} to {local_filename}")
    r = requests.get(file_url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    time.sleep(0.1)  # polite delay

def crawl_and_download(base, folder=""):
    url = base + folder
    links = get_links(url)
    for link in links:
        if link.endswith('/'):
            # It's a drectory, recurse
            crawl_and_download(base, folder + link)
        elif link.endswith('.cdf'):
            # It's a CDF file, download
            download_file(url + link, os.path.join("maven_cdfs", folder))

crawl_and_download(base_url)

