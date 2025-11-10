import asyncio
from googletrans import Translator
import random
import httpx

with open('proxies.proxy', 'r') as f:
    PROXIES = [line.strip() for line in f.readlines()]

async def translate(text, retries=5):
    for attempt in range(1, retries + 1):
        proxy = random.choice(PROXIES)
        try:
            translator = Translator(proxy=proxy)
            translated = await translator.translate(text, proxies=proxy)
            return translated.text
        except (httpx.ConnectTimeout, httpx.ReadTimeout) as e:
            print(f"[Attempt {attempt}/{retries}] Proxy failed ({proxy}) -> {e.__class__.__name__}")
            await asyncio.sleep(1)  # brief delay before retry
        except Exception as e:
            print(f"[Attempt {attempt}/{retries}] Unexpected error: {e}")
            await asyncio.sleep(1)
    return "(translation failed after retries)"


# ✅ Only run this test when executing directly
if __name__ == "__main__":
    result = asyncio.run(translate('Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυὶδ υἱοῦ Ἀβραάμ.'))
    print(result)


'''import asyncio
from googletrans import Translator
import random

with open('proxies.proxy', 'r') as f:
    PROXIES = [line.strip() for line in f.readlines()]

#PROXIES = []

print("Using proxies:", PROXIES)

response = ""

async def translate(text):
    global response
    translator = Translator(proxy=random.choice(PROXIES))
    translated = await translator.translate(text,proxies=random.choice(PROXIES))
    #print(translated.src)  # ko
    #print(translated.dest) # en
    #print(translated.text) # Good evening.
    response=translated.text

asyncio.run(translate('Βίβλος  γενέσεως  Ἰησοῦ  Χριστοῦ  υἱοῦ  Δαυὶδ  υἱοῦ  Ἀβραάμ.'))
#print(response)'''