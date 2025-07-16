import json
import requests
import time
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def extract_letter_content(url, page):
    print(f"🔍 Extracting from: {url}")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        page.goto(url, timeout=15000)
        page.wait_for_timeout(2000)

        # Get title
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "No Title"

        # Get date/location
        date_loc_tag = soup.find("p", class_="text-sm text-muted")
        date_location = date_loc_tag.get_text(strip=True) if date_loc_tag else ""

        # Get letter body
        body_div = soup.find("div", class_="text-lg leading-loose mt-6")
        if body_div:
            paragraphs = body_div.find_all("p")
            body = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            body = ""

        return {
            "title": title,
            "date_location": date_location,
            "body": body,
            "url": url
        }
    except Exception as e:
        print(f"❌ Error on {url}: {e}")
        return None

def main():
    with open("letter_urls.json", "r", encoding="utf-8") as f:
        urls = json.load(f)
    urls = urls[:10]  # Limit to first 10 for testing

    Path("data").mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        with open("data/letters.jsonl", "w", encoding="utf-8") as out_file:
            for url in urls:
                data = extract_letter_content(url, page)
                if data:
                    json.dump(data, out_file, ensure_ascii=False)
                    out_file.write("\n")

        browser.close()

    print("✅ All letters saved to data/letters.jsonl")

if __name__ == "__main__":
    main()
