
import requests
import time
import random
import pandas as pd

# Function to scrape product ID's
def scrape_product_sales(product_id):
    url = f"https://mpapi.tcgplayer.com/v2/product/{product_id}/latestsales"
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json={}, headers=headers)

    if response.status_code == 200:
        data = response.json()["data"]

        # Extract relevant fields with date & time separated
        sales_data = [
            {
                "product_id": product_id,
                "title": sale["title"],
                "condition": sale["condition"],
                "variant": sale["variant"],
                "quantity": sale["quantity"],
                "price": sale["purchasePrice"],
                "shipping": sale["shippingPrice"],
                "date": sale["orderDate"].split("T")[0],  # Extract date
                "time": sale["orderDate"].split("T")[1].split("+")[0]  # Extract time
            }
            for sale in data
        ]
        return sales_data
    else:
        print(f"❌ Failed to fetch data for product {product_id}. Status Code: {response.status_code}")
        return []

# List of product IDs to scrape
product_ids = [610840, 584272, 558189, 559269]

# List of User-Agents for rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]

# Loop through all product IDs and collect data
all_sales_data = []
for product_id in product_ids:
    print(f"📦 Scraping sales data for Product ID: {product_id}...")

    sales_data = scrape_product_sales(product_id)
    all_sales_data.extend(sales_data)

    # Randomized wait time to avoid bot detection
    wait_time = random.randint(10, 20)
    print(f"⏳ Waiting {wait_time} seconds before next request...")
    time.sleep(wait_time)

# Save the collected data to a CSV file
df = pd.DataFrame(all_sales_data)
#Final = df.groupby(['title'])['price'].mean()
filename = f"tcg_sales_{pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M')}.csv"
df.to_csv(filename, index=False)

print(f"✅ Data scraping completed! Saved to {filename}")
