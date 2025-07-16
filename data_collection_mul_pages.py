from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import time

BASE = "https://vedabase.io"
def get_letter_links_for_year(year):
    links = set()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page_num = 1
        while True:
            url = f"https://vedabase.io/en/library/letters/?year={year}&page={page_num}"
            print(f"🔍 Scraping year {year}, page {page_num}...")
            page.goto(url)
            page.wait_for_timeout(2000)

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            new_links = set()

            for a in soup.select("a[href^='/en/library/letters/']"):
                href = a.get("href")
                if href and href.count("/") > 4:
                    full_url = BASE + href
                    if full_url not in links:
                        new_links.add(full_url)

            if not new_links:
                print(f"⛔ No new links found on page {page_num}, stopping year {year}")
                break

            links.update(new_links)
            page_num += 1

        browser.close()

    return list(links)

def get_all_letter_links():
    all_links = []
    for year in range(1947, 1978):  # Inclusive of 1977
        year_links = get_letter_links_for_year(year)
        all_links.extend(year_links)
    return list(set(all_links))  # remove duplicates

if __name__ == "__main__":
    all_links = get_all_letter_links()

    with open("letter_urls.json", "w", encoding="utf-8") as f:
        json.dump(all_links, f, indent=2)

    print(f"✅ Saved {len(all_links)} unique letters to letter_urls.json")
