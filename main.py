import requests as req

class RateChecker:
    def __init__(self, key, start_curr="USD"):
        self.key = key
        self.base = start_curr.upper()
        self.link = f"https://v6.exchangerate-api.com/v6/{self.key}/latest/{self.base}"
        self.raw_info = None

    def get_rates(self):
        """Fetches data based on the current base currency."""
        try:
            res = req.get(self.link)
            if res.status_code == 200:
                data = res.json()
                if data.get("result") == "error":
                    print(f" API Error: {data.get('error-type')}")
                    return None
                self.raw_info = data
                return data.get('conversion_rates', {})
            else:
                print(f" Connection failed (Status: {res.status_code})")
        except Exception as e:
            print(f" Network error: {e}")
        return None

    def show_conversions(self, amount=1.0):
        """Displays the 2025 Global Top 10 + INR with converted values."""
        if not self.raw_info: 
            return
        
        # 2025 Top 10 Most Traded + Indian Rupee (INR)
        # Included CNY, HKD, and INR for 2025 market relevance
        top_tracked = ["USD", "EUR", "JPY", "GBP", "INR", "CNY", "CHF", "AUD", "CAD", "HKD", "SGD"]
        all_rates = self.raw_info.get('conversion_rates', {})
        
        print("\n" + "="*75)
        print(f" GLOBAL MONITOR | Amount: {amount:,.2f} {self.base}")
        print(f" Last Updated: {self.raw_info.get('time_last_update_utc')[:16]}")
        print("="*75)
        print(f"{'Ticker':<10} | {'Current Rate':<15} | {'Converted Value'}")
        print("-" * 75)

        for tick in top_tracked:
            if tick == self.base:
                print(f"{tick:<10} | {1.0:<15.4f} | {amount:,.2f} {tick}")
                continue 
            
            rate = all_rates.get(tick)
            if rate:
                total_value = amount * rate
                print(f"{tick:<10} | {rate:<15.4f} | {total_value:,.2f} {tick}")
            else:
                print(f"{tick:<10} | {'Not Found':<15} | ---")
        print("="*75 + "\n")

# -- Main block --
if __name__ == "__main__":
    MY_KEY = "ADD YOUR API KEY HERE"  # Replace with your actual API key
    
    print("--- Welcome to Global Value Tracker ---")
    
    # --- STEP 1: DEFAULT PREVIEW (INR Benchmark) ---
    print("Loading live market preview (Base: INR)...")
    # Setting default to 10,000 INR for a clear comparison
    default_bot = RateChecker(MY_KEY, "INR")
    if default_bot.get_rates():
        default_bot.show_conversions(10000.0)
    
    # -- STEP 2: CUSTOM USER INPUT --
    user_base = input("Enter your base currency (e.g., USD, EUR, GBP) [Skip for INR]: ").strip().upper()
    if not user_base:
        user_base = "INR"
    
    if len(user_base) != 3:
        print("Invalid format. Please use a 3-letter currency code.")
    else:
        # Create a new bot instance for the custom currency if it's different
        bot = RateChecker(MY_KEY, user_base)
        if bot.get_rates():
            try:
                amt_input = input(f"Enter amount in {user_base} to convert: ").strip()
                amt = float(amt_input) if amt_input else 1.0
                bot.show_conversions(amt)
            except ValueError:
                print("Invalid number. Showing conversion for 1.00 unit.")

                bot.show_conversions(1.0)


