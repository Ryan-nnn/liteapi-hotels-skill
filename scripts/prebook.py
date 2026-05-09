#!/usr/bin/env python3
import argparse, json, os, sys, urllib.request, urllib.error

BASE = os.environ.get("HOTEL_API_URL", "https://web-production-8a533.up.railway.app").rstrip("/")
if not BASE:
    print(json.dumps({"error": "HOTEL_API_URL not configured"})); sys.exit(1)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--offer-id", required=True)
    p.add_argument("--first-name", required=True)
    p.add_argument("--last-name", required=True)
    p.add_argument("--email", required=True)
    p.add_argument("--hotel-name", default="")
    p.add_argument("--room-name", default="")
    p.add_argument("--checkin", default="")
    p.add_argument("--checkout", default="")
    args = p.parse_args()

    body = json.dumps({
        "offerId": args.offer_id,
        "firstName": args.first_name,
        "lastName": args.last_name,
        "email": args.email,
        "hotelName": args.hotel_name,
        "roomName": args.room_name,
        "checkin": args.checkin,
        "checkout": args.checkout,
    }).encode()
    req = urllib.request.Request(
        f"{BASE}/prebook", data=body,
        headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req) as r:
            print(r.read().decode())
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": e.read().decode()})); sys.exit(1)

if __name__ == "__main__":
    main()
