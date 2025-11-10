import app as app
import translate_book as translate_book
from fetch_verse_count import fetch_book
import asyncio
import os

if input("Reset all data? (y/n): ").lower() == 'y':
    print("resetting...")
    import reset

#--- list of books of the Bible ---
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

bb = { 
    "Old Testament": [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
        "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
        "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
        "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
        "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
        "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
        "Zephaniah", "Haggai", "Zechariah", "Malachi"
    ],
    "New Testament": [
        "Matthew", "Mark", "Luke", "John", "Acts",
        "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
        "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
        "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews",
        "James", "1 Peter", "2 Peter", "1 John", "2 John",
        "3 John", "Jude", "Revelation"
    ]
}

'''
#BOOK="genesis"
BOOK="1 john"
BOOK_URL="1-john"
'''

i=-1

for book in ubb["New Testament"]:
    i=+1
    p=os.path.join("json", f"{book.lower()}_translated.json.json")
    #if os.path.exists(full_path):
    #if os.path.isfile(full_path):
    if(not os.path.exists(p)):
        asyncio.run(fetch_book(book.lower()))
        app.fetch_greek_english_bible(book.lower(),ubb["New Testament"][i].lower())
        translate_book.translate_book(book.lower())
    else:
        print(f"Skipping {book}")
    
book=None    
    
i=-1
for book in ubb["Old Testament"]:
    i=+1
    p=os.path.join("json", f"{book.lower()}_translated.json.json")
    if(not os.path.exists(p)):
        asyncio.run(fetch_book(book.lower()))
        app.fetch_greek_english_bible(book.lower(),ubb["Old Testament"][i].lower())
        translate_book.translate_book(book.lower())
    else:
        print(f"Skipping {book}")
