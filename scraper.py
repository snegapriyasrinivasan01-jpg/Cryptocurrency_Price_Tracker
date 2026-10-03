import time
from datetime import datetime
import pandas as pd
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def scrape_crypto_selenium(headless=True, top_n=10):
    """Primary Method: Web Scraping via Selenium."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    
    # Anti-bot detection flags
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
    )
    
    driver.set_page_load_timeout(30)
    data = []

    try:
        url = "https://coinmarketcap.com/"
        driver.get(url)

        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.cmc-table tbody tr")))

        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(2)

        rows = driver.find_elements(By.CSS_SELECTOR, "table.cmc-table tbody tr")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        count = 0
        for row in rows:
            if count >= top_n:
                break
            try:
                name_elem = row.find_element(By.CSS_SELECTOR, "p.coin-item-name, span.crypto-symbol")
                symbol_elem = row.find_element(By.CSS_SELECTOR, "p.coin-item-symbol, span.crypto-symbol")
                coin_name = f"{name_elem.text.strip()} ({symbol_elem.text.strip()})"

                price_elem = row.find_element(By.CSS_SELECTOR, "td:nth-child(4) div, td:nth-child(4) span")
                price = price_elem.text.strip()

                change_elem = row.find_element(By.CSS_SELECTOR, "td:nth-child(5) span")
                change_24h = change_elem.text.strip()

                market_cap_elem = row.find_element(By.CSS_SELECTOR, "td:nth-child(8) span:nth-child(2), td:nth-child(8)")
                market_cap = market_cap_elem.text.strip()

                data.append({
                    "Timestamp": timestamp,
                    "Coin Name": coin_name,
                    "Price": price,
                    "24h Change": change_24h,
                    "Market Cap": market_cap
                })
                count += 1
            except Exception:
                continue

    finally:
        driver.quit()

    return pd.DataFrame(data)


def fetch_crypto_api(top_n=10):
    """Fallback Method: Direct API Request."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": top_n,
        "page": 1,
        "sparkline": False
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, params=params, headers=headers, timeout=15)
    
    if response.status_code == 200:
        raw_data = response.json()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        data = []
        for coin in raw_data:
            data.append({
                "Timestamp": timestamp,
                "Coin Name": f"{coin['name']} ({coin['symbol'].upper()})",
                "Price": f"${coin['current_price']:,}",
                "24h Change": f"{coin['price_change_percentage_24h']:.2f}%",
                "Market Cap": f"${coin['market_cap']:,}"
            })
        return pd.DataFrame(data)
    return pd.DataFrame()


def scrape_crypto_data(headless=True, top_n=10):
    """Attempts Selenium scraping first; falls back to API if blocked or timed out."""
    try:
        df = scrape_crypto_selenium(headless=headless, top_n=top_n)
        if not df.empty:
            return df
    except Exception as e:
        print(f"Selenium loading issue: {e}\nFalling back to API method...")
    
    return fetch_crypto_api(top_n=top_n)