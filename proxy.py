# Generate a list of working proxies for later use with google translate.
# Great forfinding working proxies, can work with requests, 




import asyncio
from fp.fp import FreeProxy
from googletrans import Translator

# --- CONFIG ---
NUM_PROXIES_TO_COLLECT = 50
REQUEST_TIMEOUT = 8  # seconds for each translate attempt
CONCURRENCY = 10     # how many checks to run concurrently

async def test_proxy(proxy_url):
    global r
    """Test a single proxy by attempting a small translation."""
    try:
        translator = Translator(proxy={"http://": proxy_url, "https://": proxy_url})
        result = await translator.translate("hello", dest="fr")
        return True, proxy_url, result.text
    except Exception as e:
        return False, proxy_url, str(e)

for i in range(NUM_PROXIES_TO_COLLECT):
    proxy=FreeProxy(rand=True).get()
    ok, p, info = asyncio.run(test_proxy(proxy))
    print('response:',info)
    print('proxy:',proxy)
    print('ok:',ok)
    
    if ok:
        print('writing proxy to file')
        with open('proxies.proxy', 'a', encoding='utf-8') as f:
            f.write(proxy+'\n')

'''
async def fetch_proxy_list(n):
    """Blocking FreeProxy.get calls run in executor to avoid blocking the event loop."""
    loop = asyncio.get_running_loop()
    proxies = []
    with ThreadPoolExecutor() as ex:
        tasks = [loop.run_in_executor(ex, FreeProxy(rand=True).get) for _ in range(n)]
        for coro in asyncio.as_completed(tasks):
            try:
                p = await coro
                proxies.append(p)
            except Exception:
                # ignore failures from FreeProxy.get
                pass
    return proxies

def check_proxy_blocking(proxy_url):
    """Blocking check using googletrans (runs inside thread pool)."""
    # googletrans expects a dict named 'proxies' with keys "http" and "https"
    proxies = {"http://": proxy_url, "https://": proxy_url}
    translator = Translator(proxy=proxies)
    # translate returns a result object with .text
    return translator.translate("hello", dest="fr")

async def check_proxy(proxy_url, sem, executor, timeout):
    """Async wrapper that runs the blocking check in executor and applies a timeout."""
    loop = asyncio.get_running_loop()
    async with sem:
        try:
            # run the blocking translate in the thread pool, but time-limit it
            task = loop.run_in_executor(executor, check_proxy_blocking, proxy_url)
            result = await asyncio.wait_for(task, timeout=timeout)
            # result.text should contain the translated text if successful
            return True, proxy_url, getattr(result, "text", None)
        except asyncio.TimeoutError:
            return False, proxy_url, "timeout"
        except Exception as e:
            return False, proxy_url, repr(e)

async def main():
    print(f"Collecting up to {NUM_PROXIES_TO_COLLECT} candidate proxies...")
    candidates = await fetch_proxy_list(NUM_PROXIES_TO_COLLECT)
    print(f"Got {len(candidates)} candidates (may contain duplicates).")

    sem = asyncio.Semaphore(CONCURRENCY)
    good_proxies = []
    # use a single ThreadPoolExecutor for checks
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        tasks = [check_proxy(p, sem, executor, REQUEST_TIMEOUT) for p in candidates]
        for coro in asyncio.as_completed(tasks):
            ok, proxy_url, info = await coro
            if ok:
                good_proxies.append(proxy_url)
                print("Proxy works:", proxy_url, "-> response:", info)
            else:
                print("Proxy failed:", proxy_url, "->", info)

    print("\nGood proxies:", good_proxies)
    return good_proxies

if __name__ == "__main__":
    asyncio.run(main())'''


# ----------------
"""
def normalize_proxy_string(p):
    '''FreeProxy().get() often returns 'IP:PORT' — ensure scheme present'''
    if p.startswith("http://") or p.startswith("https://"):
        return p
    return "http://" + p  # using http scheme for both http/https proxies

def test_proxy_with_google(proxy_url):
    '''
    Return tuple (ok_http, ok_googletrans, details)
    ok_http: boolean if simple GET to translate.google.com succeeded
    ok_googletrans: boolean if googletrans translate test succeeded (None if googletrans not installed)
    details: short explanation or exception text
    '''
    proxies = {
        "http://": proxy_url,
        "https://": proxy_url,  # requests will use this for https as well
    }
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"}
    # 1) Test simple GET to translate.google.com
    try:
        r = requests.get(TEST_URL, headers=headers, proxies=proxies, timeout=REQUEST_TIMEOUT)
        # Consider OK if we get 200 and some expected text in body
        if r.status_code == 200 and ("Google" in r.text or "translate.google" in r.text.lower() or "translate" in r.text.lower()):
            ok_http = True
            http_details = f"HTTP {r.status_code}"
        else:
            ok_http = False
            http_details = f"HTTP {r.status_code} (unexpected body)"
    except RequestException as e:
        ok_http = False
        http_details = f"RequestException: {e}"

    # 2) Try googletrans small translation (optional)
    ok_googletrans = None
    gt_details = "googletrans not installed"
    try:
        from googletrans import Translator  # googletrans 4.x (rc1) or similar
        # googletrans accepts a 'proxies' argument in its Translator constructor in many versions
        try:
            translator = Translator(proxy=proxies)
            # run a quick translate call
            res = translator.translate("hello", dest="fr")
            #print(res.text)
            if hasattr(res, "text") and res.text:
                ok_googletrans = True
                gt_details = f"translated -> {res.text}"
            else:
                ok_googletrans = False
                gt_details = "translate returned no text"
        except Exception as e:
            ok_googletrans = False
            gt_details = f"googletrans error: {e}"
    except Exception:
        # googletrans not installed: leave ok_googletrans as None
        pass

    details = f"{http_details}; {gt_details}"
    return ok_http, ok_googletrans, details

def main():
    print(f"Collecting {NUM_PROXIES_TO_COLLECT} random free proxies...")
    raw_proxies = []
    for _ in range(NUM_PROXIES_TO_COLLECT):
        try:
            p = FreeProxy(rand=True).get()
            raw_proxies.append(p)
        except Exception as e:
            # if the provider fails, keep trying (don't abort)
            print(f"FreeProxy error (ignored): {e}")
        time.sleep(0.05)  # small delay to be polite

    # dedupe and shuffle
    raw_proxies = list(dict.fromkeys(raw_proxies))
    random.shuffle(raw_proxies)

    # save raw list (optional)
    with open('proxies.proxy', 'w', encoding='utf-8') as f:
        for proxy in raw_proxies:
            f.write(proxy + '\n')

    working = []
    report_lines = []
    print(f"Testing {len(raw_proxies)} proxies against {TEST_URL} ...")

    for i, raw in enumerate(raw_proxies, 1):
        proxy_url = normalize_proxy_string(raw)
        print(f"[{i}/{len(raw_proxies)}] testing {raw} ...", end=' ')
        ok_http, ok_gt, details = test_proxy_with_google(proxy_url)
        if ok_http:
            print("OK (HTTP)", end='')
            tag = "OK_HTTP"
            # prefer proxies that also work with googletrans
            if ok_gt is True:
                print(" + googletrans", end='')
                tag += "|OK_GT"
            elif ok_gt is False:
                print(" + googletrans FAIL", end='')
                tag += "|GT_FAIL"
            else:
                print(" + googletrans UNKNOWN", end='')
                tag += "|GT_UNKNOWN"
            print()
            working.append(raw)
        else:
            print("FAIL (HTTP)")
            tag = "FAIL_HTTP"

        report_lines.append(f"{raw}\t{tag}\t{details}")

    # write working proxies to file
    with open('working_proxies.proxy', 'w', encoding='utf-8') as f:
        for p in working:
            f.write(p + '\n')

    # write a human-readable report
    with open('proxies_report.txt', 'w', encoding='utf-8') as f:
        f.write("proxy\tstatus\tdetails\n")
        f.write("\n".join(report_lines))

    print(f"\nDone. {len(working)} proxies passed the translate.google.com HTTP test.")
    print("Saved:")
    print(" - raw proxies -> proxies.proxy")
    print(" - working proxies -> working_proxies.proxy")
    print(" - full report -> proxies_report.txt")
    if len(working) == 0:
        print("No working proxies found — try increasing NUM_PROXIES_TO_COLLECT or run again later.")

if __name__ == "__main__":
    main()
"""