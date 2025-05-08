# CSFloat Async API Client (Unofficial)

An **unofficial**, **asynchronous** Python library for interacting with the [CSFloat](https://csfloat.com) API. This library provides full support for programmatic access to listings, buy orders, user data, exchange rates, and more. All prices returned by the server are in **cents**.

## Key Features

* **Asynchronous design**: Built on `aiohttp` for non-blocking I/O.
* **Fetch listings**: Retrieve detailed listings with filters (price in cents, float, rarity, etc.).
* **Buy orders**: Get and manage buy orders for specific items.
* **User information**: Access your own profile, trades, and stall data.
* **Listing management**: Create, delete, and modify listings and buy orders.
* **Proxy support**: Optional SOCKS4/5 and HTTP(S) proxy support.
* **Error handling**: Clear exceptions with descriptive messages.

## Installation

Install via pip:

```bash
pip install csfloat_api
```

## Quick Start

```python
import asyncio
from csfloat_api.csfloat_client import Client

async def main():
    # Initialize the client (prices are in cents)
    client = Client(api_key="YOUR_API_KEY")

    # Fetch up to 50 listings priced between $1.00 and $10.00 (i.e., 100–1000 cents)
    listings = await client.get_all_listings(min_price=100, max_price=1000)
    for listing in listings:
        print(f"ID: {listing.id}, Price: {listing.price} cents, Float: {listing.item.float_value}")

    # Create a buy order for an item
    buy_order = await client.create_buy_order(
        market_hash_name="AK-47 | Redline (Field-Tested)",
        max_price=5000,  # 5000 cents = $50.00
        quantity=1
    )
    print(buy_order)

asyncio.run(main())
```

## Core Methods

* `get_exchange_rates()` – Retrieve current exchange rates.
* `get_all_listings(...)` – List items with optional filters (prices in cents).
* `get_specific_listing(listing_id)` – Get detailed info for a specific listing.
* `get_buy_orders(listing_id)` – Retrieve buy orders for a listing.
* `get_my_buy_orders(...)` – List your own buy orders.
* `get_me()` – Fetch authenticated user profile.
* `get_stall(user_id)` – Get a user's stall (listed items).
* `create_listing(asset_id, price, ...)` – Create a new listing (price in cents).
* `create_buy_order(market_hash_name, max_price, quantity)` – Place a buy order.
* `make_offer(listing_id, price)` – Make an offer on a listing.
* `buy_now(total_price, listing_id)` – Instantly buy one or more listings.
* `delete_buy_order(id)` – Cancel an existing buy order.

For a full list of methods and parameters, refer to the library's source code.

## Proxy Support

Optionally provide a proxy URL in the constructor:

```python
client = Client(
    api_key="YOUR_API_KEY",
    proxy="socks5://user:pass@host:port"
)
```

## Error Handling

The client raises exceptions for HTTP errors with clear messages:

* **401** Unauthorized – Invalid API key.
* **404** Not Found – Resource missing.
* **429** Too Many Requests – Rate limit exceeded.
* **500** Internal Server Error – Server-side issue.

## Contributing

Contributions are welcome! Please submit issues and pull requests on the [GitHub repository](https://github.com/Rushifakami/csfloat_api).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
