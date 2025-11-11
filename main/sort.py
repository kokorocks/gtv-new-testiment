import os
import shutil
types=['translated','length','greek','english']
'''for type in types:
    try:
        os.mkdir('json/'+type)
    except:
        print(' likely exists already')
'''

try:
    os.mkdir('json/nts')
except:
    print('nts likely exists already')
try:
    os.mkdir('json/ots')
except:
    print('ots likely exists already')

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

for book in ubb["New Testament"]:
    try:os.mkdir(f'json/nts/{book.lower()}')
    except:print('dir')
    try:
       shutil.move(f'json/{book.lower()}.json', f'json/nts/{book.lower()}/{book.lower()}.json')
    except:
       pass
    try:shutil.move(f'json/{book.lower()}_greek.json', f'json/nts/{book.lower()}/{book.lower()}_greek.json')
    except:pass

    try:shutil.move(f'json/{book.lower()}_english.json', f'json/nts/{book.lower()}/{book.lower()}_english.json')
    except:pass


    try:shutil.move(f'json/{book.lower()}_translated.json', f'json/nts/{book.lower()}/{book.lower()}_translated.json')
    except: pass