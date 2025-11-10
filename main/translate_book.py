import asyncio
import json
import googletrans
import random
def translate_book(BOOK_NAME = "matthew"):
    translated={}
    from fp.fp import FreeProxy

    with open(f'json/{BOOK_NAME}_greek.json', 'r', encoding='utf-8') as f:
        chapters = json.load(f)

    async def translate_book(chapters):
        proxy = FreeProxy(rand=True).get()
        for chapter in chapters:
            print(f"--- Translating Chapter {chapter} ---")

                #print(f"Translating Chapter {chapter}, Verse {verse}...")
            #greek_text = chapters[chapter][verse]

            ch=chapters[chapter]
            #print(ch)
            #lst = [ch[str(i)] for i in range(1, len(ch)+1)]
            #print(lst)        
            #translated_text = await text.translate(lst)

            for i in range(1, len(ch)+1):
                it = True
                while it:
                    try:
                        t=googletrans.Translator(proxy=proxy)
                        translate=await t.translate(dest='en', text=ch[str(i)])
                        #translated_text=await text.translate(ch[str(i)])
                        translated.setdefault(chapter, {})[str(i)] = translate.text
                        #print(f"Chapter {chapter}, Verse {ni}: {translated_text}")
                        print(translate.text)
                        it = False
                    except Exception as e:
                        print(f"Error translating Chapter {chapter}, Verse {i} with proxy {proxy}: {e}")
                        proxy = FreeProxy(rand=True).get()


        with open(f"json/{BOOK_NAME}_translated.json", "w", encoding="utf-8") as f:
            json.dump(translated, f, ensure_ascii=False, indent=4)

            #for response in translated_text:
            #    print(response.text)
            #print(f"Chapter {chapter}, Verse {verse}: {translated_text}")


    asyncio.run(translate_book(chapters))


"""import threading
import asyncio
import simdjson as json
from googletrans import Translator
import random, os, certifi

# Ensure SSL works for httpx before any requests
os.environ["SSL_CERT_FILE"] = certifi.where()

# Load proxies
with open('proxies.proxy', 'r') as f:
    PROXIES = [line.strip() for line in f.readlines()]

# Load JSON
with open('matthew_greek.json', 'r', encoding='utf-8') as f:
    parser = json.Parser()
    jsondata = parser.parse(f.read()).as_dict()

results = []
lock = threading.Lock()

async def translate_text(text):
    try:
        translator = Translator(proxy=random.choice(PROXIES))
        result = await translator.translate(text, proxies=random.choice(PROXIES))
        return result.text
    except Exception as e:
        print("Translate error:", e)
        return None

def worker(verses):
    async def run_all():
        local_results = []
        for j in range(1, len(verses)+1):
            text = verses[str(j)]
            translated = await translate_text(text)
            local_results.append(translated)
        with lock:
            results.extend(local_results)
    asyncio.run(run_all())

# Example: thread for chapter 1
t = threading.Thread(target=worker, args=(jsondata["1"],))
t.start()
t.join()

print(results)"""

'''
# Create threads for each chapter
for i in range(1, 28):
    verses = jsondata[str(i)]
    thread = threading.Thread(target=worker, args=(verses,))
    threads.append(thread)

# Start all threads
for t in threads:
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

with open('matthew_translated.txt', 'w', encoding='utf-8') as f:
    for line in translated:
        f.write(line + '\n')
print("Done! Translated:", len(translated))
'''
    



"""for i in range(1,28):
    #print(jsondata)
    verses=jsondata[str(i)]
    #print(verses)
    texts=[]
    for j in range(1,len(verses)+1):
        texts.append(verses[str(j)])
    
    thread = threading.Thread(target=worker, args=(texts,))
    thread.start()
    thread.join()"""


'''import json

with open('matthew.json', 'r', encoding='utf-8') as f:
    verse_counts = json.load(f)

print(verse_counts)

for i, j in verse_counts.items():
    print(j)
    for y in range(int(j)):
        print(i ,y)
        
    #print(x)
    print(i, j)'''

    #print(f"Chapter {i:02d}: {verse_counts[i]} verses")

"""

var = httpx.get('https://www.greekbible.com/2-corinthians/4/6')
result = BeautifulSoup(var.text, 'html.parser')

# Find the passage-output div
passage = result.find('div', class_='passage-output')

if passage:
    # Extract Greek text (all word spans)
    greek_words = passage.find_all('span', class_='word')
    greek_text = ' '.join(word.text for word in greek_words).strip()
    
    # Extract English text (from the italic div)
    english_text = passage.find('div', class_='text-stone-500').text.strip()
    
    print("Greek text:")
    print(greek_text)
    print("\nEnglish text:")
    print(english_text)
else:
    print("Passage not found")

# Save both versions to separate files
with open('greek.txt', 'w', encoding='utf-8') as f:
    f.write(greek_text)
    
with open('english.txt', 'w', encoding='utf-8') as f:
    f.write(english_text)"""