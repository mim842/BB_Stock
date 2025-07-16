import streamlit as st
import requests
import time

st.set_page_config(page_title="Best Buy RTX FE Stock Checker", layout="wide")

st.title("🖥️ Best Buy RTX 5090/5080 FE In-Store Stock Checker")

# User Inputs
api_key = st.text_input("🔑 Enter your Best Buy API Key", type="password")
zip_code = st.text_input("📍 Enter ZIP Code", value="77449")
loop_count = st.number_input("🔁 Number of Checks (every 5 mins)", min_value=1, max_value=1000, value=3)

skus = {
    "RTX 5090 FE": "6614151",
    "RTX 5080 FE": "6614153"
}

radius = 250  # miles
interval = 300  # seconds

def check_availability(product_name, sku, api_key, zip_code, radius):
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
            result_lines = []
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

# Run button
if st.button("▶️ Start Checking"):
    if not api_key or not zip_code:
        st.error("Please enter both your API key and ZIP code.")
    else:
        output_area = st.empty()
        for i in range(loop_count):
            all_results = [f"🔁 Check {i+1} of {loop_count} at ZIP {zip_code} (Radius: {radius} miles):\n"]
        for name, sku in skus.items():
            results = check_availability(name, sku, api_key, zip_code, radius)
            all_results.append(f"\n--- {name} (SKU: {sku}) ---")
            all_results.extend(results)
            time.sleep(1.5)  # Delay between requests to avoid 403 rate limit
            output_area.text("\n".join(all_results))
            if i < loop_count - 1:
                time.sleep(interval)
        st.success("✅ Finished all checks.")
