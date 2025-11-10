import json
import httpx
from bs4 import BeautifulSoup
import time

def fetch_greek_english_bible(BOOK_NAME="matthew",BOOK_URL_NAME="matthew"):
    #BOOK_NAME = "matthew"
    #BOOK_URL_NAME = "matthew"  # Adjust for GreekBible’s format if needed (e.g. "2-corinthians")
    BASE_URL = "https://www.greekbible.com"
    TRANSLATION = "asv"

    # --- Load verse counts from local JSON ---
    with open(f'json/{BOOK_NAME}.json', 'r', encoding='utf-8') as f:
        verse_counts = json.load(f)

    print(f"--- Loaded verse counts for {BOOK_NAME.capitalize()} ---")

    # Containers for both languages
    greek_data = {}
    english_data = {}

    # --- Iterate through each chapter and verse ---
    for chapter, verse_count in verse_counts.items():
        chapter = int(chapter)
        greek_data[chapter] = {}
        english_data[chapter] = {}

        print(f"\n📖 Fetching {BOOK_NAME.capitalize()} Chapter {chapter} ({verse_count} verses)")

        for verse in range(1, verse_count + 1):
            url = f"{BASE_URL}/{BOOK_URL_NAME}/{chapter}/{verse}"
            url= f"https://corsproxy.io/?url={url}"
            try:
                response = httpx.get(url, timeout=20.0)
                if response.status_code != 200:
                    print(f"⚠️ Skipping {BOOK_NAME} {chapter}:{verse} (HTTP {response.status_code})")
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')
                passage = soup.find('div', class_='passage-output')

                if not passage:
                    print(f"❌ No passage found for {BOOK_NAME} {chapter}:{verse}")
                    continue

                # Extract Greek
                greek_words = passage.find_all('span', class_='word')
                greek_text = ' '.join(w.text for w in greek_words).strip()

                # Extract English
                english_div = passage.find('div', class_='text-stone-500')
                english_text = english_div.text.strip() if english_div else ""

                greek_data[chapter][verse] = greek_text
                english_data[chapter][verse] = english_text

                print(f"✅ {BOOK_NAME.capitalize()} {chapter}:{verse} fetched")

                # Optional: small delay to be polite to the server
                time.sleep(0.5)

            except Exception as e:
                print(f"❌ Error fetching {BOOK_NAME} {chapter}:{verse}: {e}")
                continue

    # --- Save results as JSON ---
    with open(f"json/{BOOK_NAME}_greek.json", 'w', encoding='utf-8') as f:
        json.dump(greek_data, f, ensure_ascii=False, indent=4)

    with open(f"json/{BOOK_NAME}_english.json", 'w', encoding='utf-8') as f:
        json.dump(english_data, f, ensure_ascii=False, indent=4)

    print("\n✅ All verses saved as JSON files:")
    print(f" - {BOOK_NAME}_greek.json")
    print(f" - {BOOK_NAME}_english.json")
