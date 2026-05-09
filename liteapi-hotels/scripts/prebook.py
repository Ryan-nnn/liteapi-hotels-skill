#!/usr/bin/env python3
import argparse, json, os, sys, urllib.request, urllib.error

KEY = os.environ.get("LITEAPI_KEY", "")
if not KEY:
    print(json.dumps({"error": "LITEAPI_KEY not set"})); sys.exit(1)

BOOK = "https://book.liteapi.travel/v3.0"
HDR = {"X-API-Key": KEY, "Content-Type": "application/json", "Accept": "application/json"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--offer-id", required=True)
    args = p.parse_args()

    body = json.dumps({"offerId": [args.offer_id], "usePaymentSdk": False}).encode()
    req = urllib.request.Request(f"{BOOK}/rates/prebook", data=body, headers=HDR, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": e.read().decode()})); sys.exit(1)

    d = resp.get("data", {})
    print(json.dumps({
        "prebookId": d.get("prebookId"),
        "price": d.get("offerRetailRate", {}).get("amount"),
        "currency": d.get("offerRetailRate", {}).get("currency"),
        "priceChanged": d.get("priceChanged", False),
    }, indent=2))

if __name__ == "__main__":
    main()
