import httpx
import json
import asyncio
from httpx import HTTPStatusError

VERSION = "en-asv"  # Translation version
'''BOOK = "genesis"    # Book name (lowercase, e.g. 'matthew', 'psalms', '1-corinthians')
OUTPUT_FILE = f"{BOOK}.json"
'''

async def fetch_chapter(client, book, chapter):
    OUTPUT_FILE = f"json/{book}.json"
    url_book=book.replace(' ',"").replace('-','')
    """Fetch one chapter and return the number of verses."""
    url = f"https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/{VERSION}/books/{url_book}/chapters/{chapter}.json"
    try:
        print(f"📖 Fetching {book.capitalize()} {chapter}...")
        r = await client.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        # Check that it has "data" and count how many verses there are
        if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
            verse_count = len(data["data"])
            return verse_count
        else:
            print(f"⚠️ Unexpected data structure at {book} {chapter}: {data}")
            return None

    except HTTPStatusError as e:
        if e.response.status_code == 404:
            print(f"🚫 {book.capitalize()} {chapter} not found (end of book).")
            return None  # Stop when chapter doesn't exist
        print(f"⚠️ HTTP error fetching {book} {chapter}: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Network or JSON error at {book} {chapter}: {e}")
        return None

async def fetch_book(book):
    OUTPUT_FILE = f"json/{book}.json"
    """Fetch all chapters for a given book."""
    async with httpx.AsyncClient() as client:
        chapter = 1
        chapters = {}

        while True:
            verse_count = await fetch_chapter(client, book, chapter)
            if verse_count is None:
                break  # Stop when a chapter doesn't exist
            chapters[str(chapter)] = verse_count
            print(f"✅ {book.capitalize()} {chapter}: {verse_count} verses")
            chapter += 1

        # Save to JSON file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)

        print(f"\n📘 Done! Saved {len(chapters)} chapters to '{OUTPUT_FILE}'.")

#asyncio.run(fetch_book(BOOK))


'''import httpx
import json
import asyncio
from httpx import HTTPStatusError

VERSION = "en-asv"  # Translation version
BOOK = "genesis"    # Book name (lowercase, e.g. 'matthew', 'psalms', '1-corinthians')
OUTPUT_FILE = f"{BOOK}.json"

async def fetch_chapter(client, book, chapter):
    """Fetch one chapter and return the number of verses."""
    url = f"https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/{VERSION}/books/{book}/chapters/{chapter}.json"
    try:
        print(url)
        r = await client.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        if isinstance(data, list) and len(data) > 0:
            return len(data)  # Verse count
        else:
            return None  # Invalid or empty response
    except HTTPStatusError as e:
        if e.response.status_code == 404:
            return None  # Stop when chapter doesn't exist
        print(f"⚠️ Error fetching {book} {chapter}: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Network or JSON error at {book} {chapter}: {e}")
        return None

async def fetch_book(book):
    """Fetch all chapters for a given book."""
    async with httpx.AsyncClient() as client:
        chapter = 1
        chapters = {}

        while True:
            verse_count = await fetch_chapter(client, book, chapter)
            if verse_count is None:
                break  # Stop when a chapter doesn't exist
            chapters[str(chapter)] = verse_count
            print(f"✅ {book.capitalize()} {chapter}: {verse_count} verses")
            chapter += 1

        # Save to JSON
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)

        print(f"\n📘 Done! Saved {len(chapters)} chapters to '{OUTPUT_FILE}'.")

asyncio.run(fetch_book(BOOK))
'''