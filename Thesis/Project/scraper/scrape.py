from urllib.parse import urlparse
from collections import defaultdict
from bs4 import BeautifulSoup
import json


import os
import requests
import json

def get_response_and_save(url: str):
    print('url',url)

    response = requests.get(url)
	# create the scrape dir (if not found)
    if not os.path.exists("./scrape"):
        os.mkdir("./scrape")

	# save scraped content to a cleaned filename
    parsedUrl = cleanUrl(url)
    with open("./scrape/" + parsedUrl + ".html", "wb") as f:
        f.write(response.content)
    
    return response

def cleanUrl(url: str):
    return url.replace("https://", "").replace("/", "-").replace(".", "_")

def scrape_links(
    scheme: str,
    origin: str,
    path: str,
    depth=3,
    sitemap: dict = defaultdict(lambda: ""),
):
    siteUrl = scheme + "://" + origin + "/" + path
    cleanedUrl = cleanUrl(siteUrl)
    print('cleaned_url', cleanedUrl)
    if depth < 0:
        return
    if sitemap[cleanedUrl] != "":
        print(sitemap[cleanedUrl])
        return

    sitemap[cleanedUrl] = siteUrl
    print('site_map', sitemap[cleanedUrl])

    response = get_response_and_save(siteUrl)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup)
    links = soup.find_all("a")
    print(links)

    for link in links:
        href = urlparse(link.get("href"))
        if (href.netloc != origin and href.netloc != "") or (
            href.scheme != "" and href.scheme != "https"
        ):
		    # don't scrape external links
            continue
            
        scrape_links(
            href.scheme or "https",
            href.netloc or origin,
            href.path,
            depth=depth - 1,
            sitemap=sitemap,
        )
    
    return sitemap

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--site", type=str, required=True)
parser.add_argument("--depth", type=int, default=3)

if __name__ == "__main__":
    args = parser.parse_args()
    url = urlparse(args.site)
    print(url.scheme, url.netloc, url.path)
    sitemap = scrape_links(url.scheme, url.netloc, url.path, depth=args.depth)
    with open("./scrape/sitemap.json", "w") as f:
        f.write(json.dumps(sitemap))