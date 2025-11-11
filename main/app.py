import json
import httpx
from bs4 import BeautifulSoup
import time
import random
from fp.fp import FreeProxy

def get_proxy():
    """Get a new working proxy using FreeProxy."""
    try:
        proxy = FreeProxy(rand=True, timeout=1).get()
        print(f"🌐 New proxy acquired: {proxy}")
        return proxy
    except Exception as e:
        print(f"⚠️ Could not get proxy: {e}")
        time.sleep(1)
        return None

def fetch_with_proxy(url, proxy):
    """Try to fetch a URL using a given proxy."""
    try:
        '''proxies = {
            "http://": proxy,
            "https://": proxy
        }'''
        with httpx.Client(proxy=proxy, timeout=20.0, follow_redirects=True) as client:
            return client.get(url)
    except Exception as e:
        print(f"🚫 Proxy failed ({proxy}): {e}")
        return None

def fetch_greek_english_bible(BOOK_NAME="matthew", BOOK_URL_NAME="matthew", path="./"):
    BASE_URL = "https://www.greekbible.com"

    # --- Load verse counts from local JSON ---
    with open(f'{path}{BOOK_NAME}.json', 'r', encoding='utf-8') as f:
        verse_counts = json.load(f)

    print(f"--- Loaded verse counts for {BOOK_NAME.capitalize()} ---")

    greek_data = {}
    english_data = {}

    proxy = get_proxy()

    for chapter, verse_count in verse_counts.items():
        chapter = int(chapter)
        greek_data[chapter] = {}
        english_data[chapter] = {}

        print(f"\n📖 Fetching {BOOK_NAME.capitalize()} Chapter {chapter} ({verse_count} verses)")

        for verse in range(1, verse_count + 1):
            url = f"{BASE_URL}/{BOOK_URL_NAME}/{chapter}/{verse}"
            cors_url = f"https://corsproxy.io/?url={url}"
            print(f"🔗 {cors_url}")

            for attempt in range(50):  # up to 5 retries per verse
                if not proxy:
                    proxy = get_proxy()

                response = fetch_with_proxy(cors_url, proxy)

                if not response or response.status_code != 200:
                    print(f"⚠️ Retry {attempt+1}/50 for {BOOK_NAME} {chapter}:{verse}")
                    proxy = get_proxy()
                    time.sleep(1)
                    continue

                try:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    passage = soup.find('div', class_='passage-output')

                    if not passage:
                        print(f"❌ No passage found for {BOOK_NAME} {chapter}:{verse}")
                        break

                    greek_words = passage.find_all('span', class_='word')
                    greek_text = ' '.join(w.text for w in greek_words).strip()

                    english_div = passage.find('div', class_='text-stone-500')
                    english_text = english_div.text.strip() if english_div else ""

                    greek_data[chapter][verse] = greek_text
                    english_data[chapter][verse] = english_text

                    print(f"✅ {BOOK_NAME.capitalize()} {chapter}:{verse} fetched with contents: ")#{english_text}")
                    time.sleep(0.5)
                    break

                except Exception as e:
                    print(f"❌ Parsing error {BOOK_NAME} {chapter}:{verse}: {e}")
                    proxy = get_proxy()
                    time.sleep(1)
                    continue

    with open(f"{path}{BOOK_NAME}_greek.json", 'w', encoding='utf-8') as f:
        json.dump(greek_data, f, ensure_ascii=False, indent=4)

    with open(f"{path}{BOOK_NAME}_english.json", 'w', encoding='utf-8') as f:
        json.dump(english_data, f, ensure_ascii=False, indent=4)

    print("\n✅ All verses saved as JSON files:")
    print(f" - {BOOK_NAME}_greek.json")
    print(f" - {BOOK_NAME}_english.json")

if __name__ == '__main__':
    fetch_greek_english_bible('john', 'john', 'json/nts/john/')