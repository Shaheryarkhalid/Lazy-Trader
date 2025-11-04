# Lazy-Trader — Autonomous AI-Driven News-Based Trading Agent

   TradeAI is an **autonomous trading system** that listens to **Live News Stream** and executes trades based on real-time financial news and market context.  
It leverages **Google’s Gemini 2.0 Flash** model to analyze articles, predict market sentiment, and automatically make trades using Alpaca’s brokerage API.

---

## 🚀 Features

- 📡 **Live News Stream Integration** — subscribes to all U.S. market news in real time  
- 🧠 **AI-Driven Trade Decisions** — powered by `gemini-2.0-flash`, which analyzes each news article and predicts short-term (24 h) market movement  
- 💼 **Automatic Trading via Alpaca API** — executes buy/sell orders with profit and stop-loss targets  
- 💾 **Persistent Trade Logging** — saves trade data, decisions, and reasoning locally  
- 🔄 **Resilient Reconnection Logic** — automatically reconnects to Alpaca stream in case of timeouts or drops  
- 🧩 **Extensible Modular Architecture** — easy to add new data sources or replace AI models  

---

## 🏗️ Project Structure

```
TradeAI/  
│  
├── main.py                          # Entry point — initializes clients & starts the agent  
├── Constants.py                     # Shared constants and configuration  
├── helpers.py                       # Utility helpers (logging, colorized console, etc.)  
│  
├── internals/  
│   └── Config.py                    # Loads environment variables and system config  
│  
├── Alpaca/  
│   ├── NewsClient.py                # WebSocket client for Alpaca news stream  
│   ├── MarketDataClient.py          # Fetches live and historical stock data  
│   ├── TradeClient.py               # Handles trade execution and order tracking  
│   ├── test_*.py                    # Unit tests for Alpaca modules  
│  
├── AI/  
│   ├── Context.py                   # Builds global financial and geopolitical context  
│   ├── TradeAgent.py                # Core AI agent using Gemini 2.0 Flash model  
│   ├── test_*.py                    # Tests for AI components  
│  
├── functions/  
│   ├── Trade.py                     # Local database logic of trades
│   ├── test_Trade.py                # Unit test for trading functions  
│  
├── ._env                            # Template environment variables file (rename to `.env`)  
```

## ⚙️ Setup Instructions

### 1. 🐍 Install Python and Dependencies

Make sure you’re using **Python 3.10+**

```
git clone https://github.com/Shaheryarkhalid/Lazy-Trader/
cd Lazy-Trader
```
# Create virtual environment  
```
python -m venv venv  
source venv/bin/activate      # macOS/Linux  
venv\Scripts\activate         # Windows  
```

# Install dependencies  
```
pip install -r requirements.txt  
```

If you don’t yet have a `requirements.txt`, use:

```
python-dotenv  
google-genai  
alpaca-py  
colorama  
```

### 2. 🧾 Configure Environment Variables

Copy the template file and rename it:

```
cp ._env .env  
```

Edit `.env` and fill in your credentials:

```
DB_Url="./trader_db.sql"  

# Gemini Model Configuration  
Model="gemini-2.0-flash"  
Context_AI_API_Key="YOUR_GOOGLE_GENAI_API_KEY"  
Trade_AI_API_Key="YOUR_GOOGLE_GENAI_API_KEY"  

# Alpaca Configuration  
Alpaca_Stream_Url="wss://stream.data.alpaca.markets/v1beta1/news"  
Alpaca_API_Key_ID="YOUR_ALPACA_API_KEY"  
Alpaca_API_Key_Secret="YOUR_ALPACA_SECRET_KEY"  
```

> 💡 **Note:** Gemini-2.0-Flash is the only fully tested model.  
> Other smaller models may fail to handle long context or function calls properly.

---

### 3. ▶️ Running the Agent

```
./run.sh
```

Expected console output:

```
⏳ Opening Database Connection...  
🟢 Database Connection Opened Successfully.  
⏳ Connecting to Alpaca News Stream...  
🟢 Connection Successful.  
🟢 Authentication Successful.  
⏳ Waiting for news article...  
💬 Article: BTIG Reiterates Buy on Kontoor Brands, Maintains $95 Price Target
🛠️ Calling function: get_context Args : f{}
🛠️ Calling function: get_available_assets Args : f{}
💬 Total Available Assets: 32327
🛠️ Calling function: get_asset_price Args : f{'symbol': 'KTB'}
⏳ Getting Price for 'KTB'
🟢 Price for 'KTB': 73.675
🛠️ Calling function: get_asset_history_week Args : f{'symbol': 'KTB'}
🛠️ Calling function: get_older_bets Args : f{'symbol': 'KTB'}
🟠 No Trades found for 'KTB'
🛠️ Calling function: make_trade Args : f{'profit': 75, 'symbol': 'KTB', 'qty': 10, 'stop_loss': 73, 'side': 'BUY'}
🟢 Successfully Placed Trade For 'KTB' Of Quantity 10, Position OrderSide.BUY, Profit Limit 75, Stop Loss 73
🛠️ Calling function: save_trade_locally Args : f{'trade_id': '9098ab8e-bca8-4a1d-a95f-2e5f55ecfb42', 'profit_limit': 75, 'reason': "Based on BTIG's reiterated buy rating and $95 price target, combined with a recent dip in the stock price, I am initiating a buy position. The conflict in the middle east also seems to cool off so this stock might have room to grow.", 'symbol': 'KTB', 'stop_loss': 73, 'position': 'BUY', 'price': 73}
🟢 Successfully saved trade in db.
🟢 Task has been finished.
⏳ Waiting for news article...  
```

Once a news article is received, the agent will:

1. Fetch global market context  
2. Retrieve available assets  
3. Analyze the news impact  
4. Predict direction (BUY/SELL)  
5. Execute trade via Alpaca  
6. Log and save reasoning locally  

```

## 🧠 Workflow Overview

1. Connects to **Alpaca News Stream** (WebSocket)  
2. On each article:  
   - Calls `get_context()` → build global context  
   - Fetches tradable assets → `get_available_assets()`  
   - Chooses symbol & gets history → `get_asset_history_week()`  
   - Loads past bets → `get_older_bets()`  
   - Gets live price → `get_asset_price()`  
   - Places trade → `make_trade()`  
   - Saves reasoning → `save_trade_locally()`  
3. Trades auto-close after 24 hours  
4. Client auto-reconnects on disconnect  

```

```

## 🔍 Troubleshooting

| Issue | Cause | Solution |  
|-------|--------|-----------|  
| `Error: no close frame received or sent` | Alpaca closed connection unexpectedly | The client automatically reconnects. |  
| Model not responding | Wrong API key or context too large | Use `gemini-2.0-flash` and verify API key. |  
| No trades executed | Article didn’t map to a tradable asset | Check logs; not all news triggers trades. |  

```

## 🧱 Tech Stack

- **Language:** Python 3.10+  
- **AI Model:** Gemini 2.0 Flash (Google GenAI)  
- **Brokerage API:** Alpaca Markets  
- **Database:** Local SQLite (`trader_db.sql`)  
- **Libraries:** `alpaca-py`, `google-genai`, `colorama`, `python-dotenv`  

---


## ⚠️ Disclaimer

> **This project is for research and educational purposes only.**  
> Do **not** use it for real-money trading without extensive testing, risk controls, and regulatory compliance.  
> The author assumes no liability for financial loss.

---

## 📄 License

MIT License © 2025 Your Name
