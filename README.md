An automated, fault-tolerant Python application that scrapes real-time cryptocurrency market data and logs timestamped records into a structured CSV file with console summary outputs.

📌 Features

- **Automated Web Scraping:** Scrapes live crypto rates (Name, Symbol, Price, 24h Change, Market Cap) using **Selenium WebDriver**.
- **Fault-Tolerant Failover:** Automatically switches to **Requests API** fallback if web page DOM elements fail to load or time out.
- **Data Processing:** Cleans and formats extracted data using **Pandas**.
- **Persistent Logging:** Appends timestamped records (`YYYY-MM-DD HH:MM:SS`) to `crypto_prices.csv` for historical tracking.
- **Terminal Output:** Displays neat summary tables directly in the console using `tabulate`.

---

 🏗️ System Architecture

```text
[ Live Market Data / Web Pages ]
               │
               ▼
   [ Primary: Selenium Engine ]
               │
      (If Web Page Fails)
               │
               ▼
   [ Fallback: Requests API ]
               │
               ▼
   [ Pandas Data Processing ]
               │
       ┌───────┴───────┐
       ▼               ▼
[ Terminal View ]  [ CSV File ]

🛠️ Tech Stack & Dependencies
 * Language: Python 3.x
 * Libraries & Tools:
   * selenium & webdriver-manager (Web Scraping & Browser Automation)
   * requests (API Fallback Layer)
   * pandas (Data Processing & CSV Storage)
   * tabulate (Formatted Console Tables)
🚀 Getting Started
1. Clone the Repository
git clone [https://github.com/snegapriyasri/Cryptocurrency_Price_Tracker.git](https://github.com/snegapriyasri/Cryptocurrency_Price_Tracker.git)
cd Cryptocurrency_Price_Tracker

2. Set Up Virtual Environment
# Create virtual environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Run the Script
python main.py

📊 Sample Output
Terminal View:
| Rank | Name | Symbol | Price ($)|24h Change (%)| Market Cap ($) | Timestamp           |
| 1 | Bitcoin | BTC | 63,450.20   | +1.85        | 1.25T          | 2026-10-04 09:30:00 |
| 2 | Ethereum| ETH | 3,450.75    | -0.42        | 415B           | 2026-10-04 09:30:00 |
CSV File (crypto_prices.csv):
Extracted data is automatically appended to crypto_prices.csv on every run.
🔮 Future Enhancements
 * [ ] Automated execution using cron / Task Scheduler.
 * [ ] Interactive visualization dashboard with Streamlit.
 * [ ] Instant price threshold alerts via Telegram/Email.
