#!/usr/bin/env python3
import argparse, json, os, sys, urllib.request, urllib.parse, urllib.error

BASE = os.environ.get("HOTEL_API_URL", "https://web-production-8a533.up.railway.app").rstrip("/")
if not BASE:
    print(json.dumps({"error": "HOTEL_API_URL not configured"})); sys.exit(1)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--city", required=True)
    p.add_argument("--country", required=True)
    p.add_argument("--checkin", required=True)
    p.add_argument("--checkout", required=True)
    p.add_argument("--adults", type=int, default=2)
    p.add_argument("--currency", default="USD")
    args = p.parse_args()

    body = json.dumps({
        "city": args.city, "country": args.country,
        "checkin": args.checkin, "checkout": args.checkout,
        "adults": args.adults, "currency": args.currency,
    }).encode()
    req = urllib.request.Request(
        f"{BASE}/search", data=body,
        headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req) as r:
            print(r.read().decode())
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": e.read().decode()})); sys.exit(1)

if __name__ == "__main__":
    main()
