# server.py
from mcp.server.fastmcp import FastMCP, Context
from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel, Field, PositiveFloat
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create an MCP server
mcp = FastMCP("Ikman", dependencies=["bs4", "requests", "pydantic", "python-dotenv"])


class ProductSearchInput(BaseModel):
    product: str = Field(min_length=1, description="Product name to search for")
    budget: PositiveFloat = Field(description="Maximum budget for the product")
    location: str = Field(min_length=1, description="Location to search in")


def extract_price(price_list: list) -> float:
    """Extract and convert price string to float"""
    if not price_list or not price_list[0] or len(price_list[0]) <= 3:
        return 0
    price = price_list[0][3:]  # Extract substring after 3rd letter
    price = price.replace(",", "")  # Remove commas
    try:
        return float(price)
    except (ValueError, TypeError):
        return 0


async def process_product_page(url: str, budget: float, ctx: Context) -> list:
    """Process a single product page and return valid products."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        await ctx.error(f"Failed to fetch page: {str(e)}")
        return []

    products = []
    soup = BeautifulSoup(response.text, "html.parser")
    anchors = soup.select("a.gtm-ad-item")

    for anchor in anchors:
        title = anchor.get("title", "").strip()
        if not title:
            continue

        price_element = anchor.select_one("span")
        price = price_element.text if price_element else ""
        price_value = extract_price([price])

        if price_value == 0 or price_value > budget:
            continue

        products.append(
            {
                "title": title,
                "price": price_value,
                "link": "https://ikman.lk" + anchor.get("href", ""),
            }
        )

    return products


@mcp.tool()
async def top_three_products(
    product: str, budget: int, location: str, ctx: Context
) -> object:
    """Get the top products from ikman.lk
    within a given budget and location
    then include the link to the product and give top results
    with insights from google reviews and product description."""
    try:
        validated_input = ProductSearchInput(
            product=product, budget=budget, location=location
        )

        await ctx.info(
            f"Searching for {validated_input.product} under {validated_input.budget} LKR in {validated_input.location}"
        )

        encoded_product = validated_input.product.replace(" ", "%20")
        location_param = (
            "sri-lanka" if location.lower() == "sri lanka" else location.lower()
        )

        all_products = []
        pages_to_search = int(os.getenv("PAGES_TO_SEARCH", "4"))
        for page in range(1, pages_to_search + 1):
            await ctx.info(f"Scanning page {page}...")
            url = (
                f"https://ikman.lk/en/ads/{location_param}"
                f"?sort=date&order=desc&buy_now=0&urgent=0"
                f"&query={encoded_product}&page={page}"
            )

            page_products = await process_product_page(url, validated_input.budget, ctx)
            all_products.extend(page_products)

        await ctx.info(f"Found products: {all_products}")
        return "".join(
            [
                f"Title: {product['title']}, Price: {product['price']} LKR, Link: {product['link']}\n"
                for product in all_products[:3]
            ]
        )

    except Exception as e:
        await ctx.error(f"An error occurred: {str(e)}")
        return {"error": str(e), "products": []}


if __name__ == "__main__":
    mcp.run()
