#!/usr/bin/env python3
import argparse, json, os, sys
import urllib.request, urllib.parse, urllib.error

KEY = os.environ.get("LITEAPI_KEY", "")
if not KEY:
    print(json.dumps({"error": "LITEAPI_KEY not set. Please configure your API key in the Skills panel."})); sys.exit(1)

SEARCH = "https://api.liteapi.travel/v3.0"
HDR = {"X-API-Key": KEY, "Content-Type": "application/json", "Accept": "application/json"}

def api(method, url, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HDR, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--city", required=True)
    p.add_argument("--country", required=True)
    p.add_argument("--checkin", required=True)
    p.add_argument("--checkout", required=True)
    p.add_argument("--adults", type=int, default=2)
    p.add_argument("--currency", default="USD")
    p.add_argument("--limit", type=int, default=20)
    args = p.parse_args()

    params = urllib.parse.urlencode({"countryCode": args.country, "cityName": args.city, "limit": args.limit})
    hotels_resp = api("GET", f"{SEARCH}/data/hotels?{params}")
    if "error" in hotels_resp:
        print(json.dumps(hotels_resp)); sys.exit(1)

    hotel_list = hotels_resp.get("data", [])
    if not hotel_list:
        print(json.dumps({"error": f"No hotels found in {args.city}"})); sys.exit(1)

    hotel_ids = [h["id"] for h in hotel_list[:args.limit]]
    rates_resp = api("POST", f"{SEARCH}/hotels/rates", {
        "hotelIds": hotel_ids,
        "checkin": args.checkin, "checkout": args.checkout,
        "currency": args.currency, "guestNationality": args.country,
        "occupancies": [{"rooms": 1, "adults": args.adults, "children": []}],
    })
    if "error" in rates_resp:
        print(json.dumps(rates_resp)); sys.exit(1)

    hotel_map = {h["id"]: h for h in hotel_list}
    results = []
    for item in rates_resp.get("data", []):
        hid = item.get("hotelId")
        offers = item.get("roomTypes", [])
        if not offers: continue
        best = min(offers, key=lambda x: float(x.get("offerRetailRate", {}).get("amount", 999999)))
        hi = hotel_map.get(hid, {})
        results.append({
            "hotelId": hid,
            "name": hi.get("name", "Unknown"),
            "stars": hi.get("starRating", ""),
            "rating": hi.get("guestScore", ""),
            "offerId": best.get("offerId"),
            "roomName": best.get("name", "Standard Room"),
            "price": best.get("offerRetailRate", {}).get("amount"),
            "currency": best.get("offerRetailRate", {}).get("currency", args.currency),
            "cancellation": best.get("cancellationPolicies", {}).get("cancelPolicyInfos", [{}])[0].get("type", "unknown"),
        })

    results.sort(key=lambda x: float(x["price"] or 999999))
    print(json.dumps({"hotels": results[:10]}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
