#!/usr/bin/env python3
import argparse, json, os, sys, urllib.request, urllib.error

KEY = os.environ.get("LITEAPI_KEY", "")
if not KEY:
    print(json.dumps({"error": "LITEAPI_KEY not set"})); sys.exit(1)

BOOK = "https://book.liteapi.travel/v3.0"
HDR = {"X-API-Key": KEY, "Content-Type": "application/json", "Accept": "application/json"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prebook-id", required=True)
    p.add_argument("--first-name", required=True)
    p.add_argument("--last-name", required=True)
    p.add_argument("--email", required=True)
    p.add_argument("--card-number", required=True)
    p.add_argument("--card-exp-month", required=True)
    p.add_argument("--card-exp-year", required=True)
    p.add_argument("--card-cvc", required=True)
    args = p.parse_args()

    payload = {
        "prebookId": args.prebook_id,
        "holder": {"firstName": args.first_name, "lastName": args.last_name, "email": args.email},
        "payment": {
            "method": "CREDIT_CARD",
            "card": {
                "number": args.card_number,
                "expMonth": args.card_exp_month,
                "expYear": args.card_exp_year,
                "cvc": args.card_cvc,
                "holderName": f"{args.first_name} {args.last_name}",
            }
        },
        "guests": [{"occupancyNumber": 1, "firstName": args.first_name, "lastName": args.last_name, "email": args.email}],
    }
    body = json.dumps(payload).encode()
    req = urllib.request.Request(f"{BOOK}/rates/book", data=body, headers=HDR, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": e.read().decode()})); sys.exit(1)

    d = resp.get("data", {})
    print(json.dumps({
        "bookingId": d.get("bookingId"),
        "status": d.get("status"),
        "hotel": d.get("hotel", {}).get("name"),
        "checkin": d.get("checkin"),
        "checkout": d.get("checkout"),
        "totalPrice": d.get("offerRetailRate", {}).get("amount"),
        "currency": d.get("offerRetailRate", {}).get("currency"),
    }, indent=2))

if __name__ == "__main__":
    main()
