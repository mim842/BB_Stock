import streamlit as st 
import requests
import time

st.set_page_config(page_title="Best Buy RTX FE Stock Checker", layout="wide")
st.title("🖥️ Best Buy RTX FE In-Store Stock Checker")

# User Inputs
api_key = st.text_input("🔑 Enter your Best Buy API Key", type="password")
zip_code = st.text_input("📍 Enter ZIP Code", value="77449")
loop_count = st.number_input("🔁 Number of Checks (every 5 mins)", min_value=1, max_value=1000, value=3)

# Default SKU input
sku_input = st.text_input("🎯 Enter SKUs (comma-separated)", value="6614151, 6614153")

radius = 250  # miles
interval = 300  # seconds

# Parse SKU input into clean list of SKUs
def parse_skus(raw_input):
    return [sku.strip() for sku in raw_input.split(",") if sku.strip().isdigit()]

sku_list = parse_skus(sku_input)

# Check availability
def check_availability(sku, api_key, zip_code, radius):
    url = f"https://api.bestbuy.com/v1/stores(area({zip_code},{radius}))+products(sku={sku})"
    params = {
        "apiKey": api_key,
        "format": "json",
        "show": "storeId,name,city,region,products.name,products.inStoreAvailability"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            stores = data.get("stores", [])
            if not stores:
                return [f"⚠️ No stores found for SKU {sku}."]
            result_lines = []
            product_name = stores[0]["products"][0].get("name", "Unknown Product")
            result_lines.append(f"\n🆔 SKU: {sku} | 🏷️ Product: {product_name}")
            for store in stores:
                name = store["name"]
                city = store["city"]
                state = store["region"]
                available = store["products"][0]["inStoreAvailability"]
                status = "✅ In Stock" if available else "❌ Out of Stock"
                result_lines.append(f"{status} - {name} ({city}, {state})")
            return result_lines
        else:
            return [f"❌ API error {response.status_code}: {response.text}"]
    except Exception as e:
        return [f"⚠️ Error fetching availability: {e}"]

# Run loop
if st.button("▶️ Start Checking"):
    if not api_key or not zip_code:
        st.error("Please enter both your API key and ZIP code.")
    elif not sku_list:
        st.error("Please enter at least one valid SKU.")
    else:
        output_area = st.empty()
        for i in range(loop_count):
            all_results = [f"🔁 Check {i+1} of {loop_count} at ZIP {zip_code} (Radius: {radius} miles):\n"]
            for sku in sku_list:
                results = check_availability(sku, api_key, zip_code, radius)
                all_results.extend(results)
                time.sleep(1.5)  # Delay between requests
            output_area.text("\n".join(all_results))
            if i < loop_count - 1:
                time.sleep(interval)
        st.success("✅ Finished all checks.")
