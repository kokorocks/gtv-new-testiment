import asyncio
from googletrans import Translator
from fp.fp import FreeProxy

async def main():
    proxy1 = FreeProxy(rand=True).get()
    proxy2 = FreeProxy(rand=True).get()
    
    PROXIES = {
        'http': proxy1,
        'https': proxy2
    }
    
    print("Using proxies:", PROXIES)

    translator = Translator(service_urls=['translate.google.com'])
    
    text = "Hello world"
    translated = await translator.translate(text, src='en', dest="ko", proxies=PROXIES)
    
    print("source:", translated.src)
    print("translated:", translated.text)
    print(translated.origin, ' -> ', translated.text)

asyncio.run(main())
