import requests
from bs4 import BeautifulSoup
import scraperwiki
import time

BASE_URL = "https://www.locanto.com.au/perth/Women-Looking-for-Men/20702/?sort=date&dist=50&page={page}"

def scrape_page(page):
    url = BASE_URL.format(page=page)
    resp = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; MorphIOScraper/1.0)"
    })
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    listings = soup.select("div.listing")

    for item in listings:
        ad_id = item.get("data-listing-id")
        title_el = item.select_one("h2.title")
        price_el = item.select_one("div.price")
        link_el = item.select_one("a[href*='/ad/']")
        location_el = item.select_one("div.location")
        date_el = item.select_one("div.date")

        record = {
            "id": ad_id,
            "title": title_el.text.strip() if title_el else None,
            "price": price_el.text.strip() if price_el else None,
            "url": link_el["href"] if link_el else None,
            "location": location_el.text.strip() if location_el else None,
            "date_posted": date_el.text.strip() if date_el else None,
        }

        scraperwiki.sqlite.save(unique_keys=["id"], data=record)

def main():
    for page in range(1, 6):  # adjust max pages as needed
        scrape_page(page)
        time.sleep(2)  # polite delay

if __name__ == "__main__":
    main()
