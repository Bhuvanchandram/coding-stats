import requests
import json
from datetime import datetime

LEETCODE_USERNAME = "bhuvanchandra"
GFG_USERNAME = "bm296g2v2"


def safe_get(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")
        return ""

def get_leetcode_count():
    url = f"https://leetcode.com/{LEETCODE_USERNAME}"
    html = safe_get(url)

    import re
    match = re.search(r'"difficulty":"All","count":(\\d+)', html)
    return int(match.group(1)) if match else 0

def get_gfg_count():
    url = f"https://auth.geeksforgeeks.org/user/{GFG_USERNAME}/practice/"
    html = requests.get(url, timeout=10).text

    import re
    match = re.search(r'"difficulty":"All","count":(\\d+)', html)
    return int(match.group(1)) if match else 0

def main():
    leetcode = get_leetcode_count()
    gfg = get_gfg_count()

    total = leetcode + gfg

    data = {
        "total": total,
        "last_updated": datetime.utcnow().isoformat()
    }

    with open("stats.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Updated:", data)

if __name__ == "__main__":
    main()
