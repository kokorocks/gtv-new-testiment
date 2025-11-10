import httpx
import urllib.parse

inner_url = "https://bible-api.com/genesis 16?translation=asv"
encoded = urllib.parse.quote(inner_url, safe="")

final_url = f"https://corsproxy.io/?url={encoded}"

print(final_url)

response = httpx.get(final_url, headers={"User-Agent": "Mozilla/5.0"})
print(response.status_code)
print(response.text[:300])
