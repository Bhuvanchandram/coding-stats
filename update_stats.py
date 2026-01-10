import requests
import json
from datetime import datetime

# -------------------- CONFIG --------------------

LEETCODE_USERNAME = "bhuvanchandra"
GFG_USERNAME = "bm296g2v2"

STATS_FILE = "stats.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    )
}

# -------------------- HELPERS --------------------

def safe_get(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"[ERROR] GET {url} failed:", e)
        return ""

def safe_post(url, payload):
    try:
        r = requests.post(url, json=payload, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR] POST {url} failed:", e)
        return {}

# -------------------- FETCHERS --------------------

def get_leetcode_count():
    url = "https://leetcode.com/graphql"
    payload = {
        "query": """
        query userProfile($username: String!) {
          matchedUser(username: $username) {
            submitStatsGlobal {
              acSubmissionNum {
                difficulty
                count
              }
            }
          }
        }
        """,
        "variables": {"username": LEETCODE_USERNAME},
    }

    data = safe_post(url, payload)

    try:
        stats = data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]
        for item in stats:
            if item["difficulty"] == "All":
                print("[INFO] LeetCode solved:", item["count"])
                return item["count"]
    except Exception as e:
        print("[ERROR] LeetCode parse failed:", e)

    return 0

def get_gfg_count():
    url = f"https://auth.geeksforgeeks.org/user/{GFG_USERNAME}/practice/"
    html = safe_get(url)

    if not html:
        return 0

    import re
    match = re.search(r"Solved Problems.*?<span>(\d+)</span>", html, re.S)

    if match:
        count = int(match.group(1))
        print("[INFO] GFG solved:", count)
        return count

    print("[WARN] GFG count not found")
    return 0

# -------------------- MAIN --------------------

def main():
    leetcode = get_leetcode_count()
    gfg = get_gfg_count()

    total = leetcode + gfg

    data = {
        "total": total,
        "last_updated": datetime.utcnow().isoformat() + "Z"
    }

    with open(STATS_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("[SUCCESS] Stats updated:", data)

if __name__ == "__main__":
    main()
