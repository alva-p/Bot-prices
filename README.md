CryptoPriceBot

A Telegram bot that sends you cryptocurrency price updates every minute, with the time adjusted to your local timezone.

How to use the bot

1. Start the bot:
   - Send the /start command to the bot on Telegram.
   - You’ll receive a message like:
     You’ve subscribed! You’ll receive prices every minute.
     Please set your country with:
     /setcountry <country>
     Examples: /setcountry Argentina, /setcountry Spain
   - This subscribes you to receive notifications.

2. Set your country:
   - Use the /setcountry <country> command to adjust the time to your local timezone.
   - Examples:
     - /setcountry Argentina → Sets the time to America/Argentina/Buenos_Aires (GMT-3).
     - /setcountry Spain → Sets the time to Europe/Madrid (GMT+1 or +2 depending on daylight saving time).
   - Supported countries: Argentina, Spain, USA, UK, Brazil, France, Germany, Italy.
   - You’ll get a confirmation with your local time, for example:
     Country set to Argentina. Local time now: 17:14:00 (America/Argentina/Buenos_Aires)

3. Receive notifications:
   - Every 1 minute, the bot will send you a message with updated prices and your local time.
   - Example message:
     📊 Price Update 📊
     BTC ₿: $95,850.00 | -0.01% ⬇️
     --------------------
     ETH Ξ: $2,812.65 | -0.01% ⬇️
     --------------------
     RON 🎮: $1.19 | 0.00% ➡️
     --------------------
     SOL ◎: $167.98 | 0.01% ⬆️
     --------------------
     BNB 💰: $653.68 | 0.03% ⬆️
     --------------------
     BANANA 🍌: $0.20 | -0.01% ⬇️
     --------------------
     AXS 🎮: $4.10 | 0.00% ➡️
     --------------------
     Local time: 17:14:00 (America/Argentina/Buenos_Aires)

Included Tokens
The bot displays prices for the following cryptocurrencies:
- BTC (Bitcoin)
- ETH (Ethereum)
- RON (Ronin)
- SOL (Solana)
- BNB (Binance Coin)
- BANANA (Banana)
- AXS (Axie Infinity)

Notification Frequency
- Updates are sent every 1 minute.

How to set up and run
1. Clone the repository:
   git clone https://github.com/AlvaroP1017/cryptoPrices.git
2. Install the dependencies:
   pip install -r requirements.txt
3. Create a .env file with your Telegram token:
   TELEGRAM_TOKEN=your_bot_token
4. Run the bot:
   python pricesBOT.py

Enjoy real-time cryptocurrency price updates!
