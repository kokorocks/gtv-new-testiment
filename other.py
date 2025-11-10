'''import httpx

VERSION = "en-asv"
BOOK = "genesis"
CHAPTER_NUMBER = 1 # Change this to test, e.g., 51 for a known error

url = f"https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/{VERSION}/books/{BOOK}/chapters/{CHAPTER_NUMBER}.json"

try:
    response = httpx.get(url)
    response.raise_for_status()
    chapter_data = response.json()
    print(f"Fetched data type: {chapter_data}")
    
    # --- FIX START ---
    if isinstance(chapter_data, list):
        # The data is a list of verses, safe to proceed
        verse_count = len(chapter_data)
        
        # We can still try to get the last verse number, but only if the list isn't empty
        last_verse_number = chapter_data[-1]['verse'] if chapter_data else 0

        print(f"✅ Successful! {BOOK.capitalize()} Chapter {CHAPTER_NUMBER}")
        print(f"Total Verses:   {verse_count}")
        print(f"Last Verse No.: {last_verse_number}")
    else:
        # The data is a dictionary, likely an error message
        error_message = chapter_data.get('error', 'Unknown Error')
        print(f"❌ Error in API Response for {BOOK.capitalize()} Chapter {CHAPTER_NUMBER}.")
        print(f"   API returned a dictionary/object, not a list of verses. Message: {error_message}")
    # --- FIX END ---
    
except httpx.exceptions.RequestException as e:
    print(f"❌ Network Error fetching data: {e}")'''
    
"""response_data = {'data': [{'book': 'Genesis', 'chapter': '1', 'verse': '1', 'text': 'In the beginning God created the heavens and the earth.'}, 
                           # ... all 31 verses ... 
                          {'book': 'Genesis', 'chapter': '1', 'verse': '31', 'text': 'And God saw everything that he had made, and, behold, it was very good. And there was evening and there was morning, the sixth day.'}]}

# 1. Access the list of verses using the 'data' key
list_of_verses = response_data['data'] 

# 2. Get the count
verse_count = len(list_of_verses)

# 3. Get the book and chapter reference
book_name = list_of_verses[0]['book']
chapter_number = list_of_verses[0]['chapter']

print(f"📖 The book is: **{book_name}**")
print(f"📘 Chapter {chapter_number} contains **{verse_count}** verses.")"""

