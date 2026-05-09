# liteapi-hotels

An [OpenClaw](https://openclaw.ai) skill for hotel search and booking, powered by the LiteAPI backend.

## What it does

- Search 2M+ hotels worldwide with real-time pricing
- Lock in rates and generate a secure hosted payment link
- No API key required from end users — all calls go through the backend server

## Usage in an agent manifest

```json
{
  "skills": [
    "https://github.com/Ryan-nnn/liteapi-hotels-skill@liteapi-hotels"
  ]
}
```

## Booking flow

```
search.py → user selects hotel → prebook.py → paymentUrl sent to user → user pays → confirmation email
```

## Scripts

| Script | Description |
|--------|-------------|
| `search.py` | Search available hotels by city, dates, adults, currency |
| `prebook.py` | Lock a rate and return a secure hosted payment link |

## Backend

Scripts connect to a Railway-hosted backend (`HOTEL_API_URL`) which wraps the LiteAPI v3 booking API. The backend handles payment via LiteAPI's hosted payment page — no credit card details are ever entered in the AI conversation.
