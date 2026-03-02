# server.py — Real MCP Server with 2 tools
from mcp.server.fastmcp import FastMCP
from datetime import datetime
import aiohttp
import os

# ── Set port via environment variable ────────────────────────────
# Your mcp version 1.26.0 does not support port in run()
# Port is configured this way instead
os.environ["HOST"] = "0.0.0.0"
os.environ["PORT"] = "9000"

mcp = FastMCP("real-tools")


# TOOL 1 — Get current date and time (no internet needed)
@mcp.tool()
async def get_current_datetime() -> dict:
    """Get the current date, time and day of week"""
    now = datetime.now()
    return {
        "date": now.strftime("%d-%m-%Y"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A")
    }


# TOOL 2 — Currency converter (free API, no key needed)
@mcp.tool()
async def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Convert amount from one currency to another using live rates.
    Args:
        amount: Amount to convert (e.g. 100)
        from_currency: Source currency code (e.g. 'USD', 'INR', 'EUR')
        to_currency: Target currency code (e.g. 'INR', 'USD', 'EUR')
    """
    async with aiohttp.ClientSession() as session:
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

            rates = data.get("rates", {})
            to_curr = to_currency.upper()

            if to_curr not in rates:
                return {"status": "error", "message": f"Currency '{to_currency}' not found"}

            rate = rates[to_curr]
            converted = round(amount * rate, 2)

            return {
                "status": "success",
                "from": f"{amount} {from_currency.upper()}",
                "to": f"{converted} {to_currency.upper()}",
                "exchange_rate": rate
            }

        except aiohttp.ClientConnectorError:
            return {"status": "error", "message": "No internet connection"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    print("🚀 MCP Server running on http://localhost:9000")
    print("💡 Keep this terminal open and run client.py in new terminal\n")
    mcp.run(transport="streamable-http")