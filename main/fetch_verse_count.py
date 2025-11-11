import httpx
import json
import asyncio
from fp.fp import FreeProxy
import random, os

VERSION = "en-asv"
MAX_RETRIES = 5000


async def fetch_chapter(book, chapter, proxy_ip):
    OUTPUT_FILE = f"json/{book}.json"
    url_book = book.replace(" ", "").replace("-", "")
    url = f"https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/{VERSION}/books/{url_book}/chapters/{chapter}.json"
    
    for attempt in range(MAX_RETRIES):
        proxies = proxy_ip
        try:
            async with httpx.AsyncClient(proxy=proxies, timeout=10) as client:
                print(f"📖 Fetching {book.capitalize()} {chapter} (Attempt {attempt+1}) using proxy {proxy_ip}...")
                r = await client.get(url)
                # Handle 403 "package too large" manually before raise_for_status
                if r.status_code == 403 and "Package size exceeded" in r.text:
                    print(f"🚫 {book.capitalize()} {chapter} appears too large or missing (end of book).")
                    return None

                r.raise_for_status()
                data = r.json()

                if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
                    return len(data["data"])
                else:
                    print(f"⚠️ Unexpected data structure at {book} {chapter}: {data}")
                    return None

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                print(f"🚫 {book.capitalize()} {chapter} not found (end of book).")
                return None
            elif e.response.status_code in [403, 429]:
                print(f"⚠️ HTTP {e.response.status_code} error at {book} {chapter}. Retrying with new proxy...")
                proxy_ip = FreeProxy(rand=True, anonym=True).get()
            else:
                print(f"⚠️ HTTP error at {book} {chapter}: {e}. Retrying...")
                proxy_ip = FreeProxy(rand=True, anonym=True).get()
        except Exception as e:
            print(f"⚠️ Network or JSON error at {book} {chapter}: {e}. Retrying...")
            proxy_ip = FreeProxy(rand=True, anonym=True).get()

        await asyncio.sleep(random.uniform(1, 3))

    print(f"❌ Failed to fetch {book} {chapter} after {MAX_RETRIES} attempts.")
    return None


async def fetch_book(book, location=""):
    try:
        os.mkdir(location)
    except:
        print('folder already exists')
    OUTPUT_FILE = f"{location}{book}.json"
    chapter = 1
    chapters = {}
    proxy_ip = FreeProxy(rand=True, anonym=True).get()
    
    while True:
        verse_count = await fetch_chapter(book, chapter, proxy_ip=proxy_ip)
        if verse_count is None:
            break
        chapters[str(chapter)] = verse_count
        print(f"✅ {book.capitalize()} {chapter}: {verse_count} verses")
        chapter += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chapters, f, ensure_ascii=False, indent=2)

    print(f"\n📘 Done! Saved {len(chapters)} chapters to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    book_name = "john"
    asyncio.run(fetch_book(book_name))

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