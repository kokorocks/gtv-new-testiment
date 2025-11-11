import app
import translate_book
from fetch_verse_count import fetch_book
import asyncio
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


if input("Reset all data? (y/n): ").lower() == 'y':
    print("resetting...")
    import reset

try:
    os.mkdir('json/nts')
except:
    pass
try:
    os.mkdir('json/ots')
except:
    pass

# --- Bible book lists ---
ubb = {
    "Old Testament": [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "1-Samuel", "2-Samuel",
        "1-Kings", "2-Kings", "1 Chronicles", "2-Chronicles", "Ezra",
        "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
        "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
        "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
        "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
        "Zephaniah", "Haggai", "Zechariah", "Malachi"
    ],
    "New Testament": [
        "Matthew", "Mark", "Luke", "John", "Acts",
        "Romans", "1-Corinthians", "2-Corinthians", "Galatians", "Ephesians",
        "Philippians", "Colossians", "1-Thessalonians", "2-Thessalonians",
        "1-Timothy", "2-Timothy", "Titus", "Philemon", "Hebrews",
        "James", "1-Peter", "2-Peter", "1-John", "2-John",
        "3-John", "Jude", "Revelation"
    ]
}


def process_book(book_name: str, testament:str):
    """Handles fetching and translation for one book."""
    file_path = os.path.join("json", f"{book_name.lower()}_translated.json.json")

    if os.path.exists(file_path):
        print(f"Skipping {book_name} (already done)")
        return

    try:
        print(f"Processing {book_name}...")

        # Fetch book data asynchronously
        asyncio.run(fetch_book(book_name.lower(),f'json/{testament}/{book_name.lower()}/'))

        # Combine Greek + English Bibles
        app.fetch_greek_english_bible(book_name.lower(), book_name.lower(),f'json/{testament}/{book_name.lower()}/')

        # Translate to English (or whatever your logic does)
        translate_book.translate_book(book_name.lower(),f'json/{testament}/{book_name.lower()}/')

        print(f"✅ Finished {book_name}")

    except Exception as e:
        print(f"❌ Error processing {book_name}: {e}")


def run_threaded_processing():
    max_threads = 10  # Adjust this (5–10 is safe)
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []

        # Schedule New Testament books
        if(input('nts? y|n')=='y'):
            for book in ubb["New Testament"]:
                futures.append(executor.submit(process_book, book, 'nts'))

        # Schedule Old Testament books
        if(input('nts? y|n')=='y'):
            for book in ubb["Old Testament"]:
                futures.append(executor.submit(process_book, book, 'ots'))

        # Wait for all to finish
        for future in as_completed(futures):
            future.result()


if __name__ == "__main__":
    run_threaded_processing()
