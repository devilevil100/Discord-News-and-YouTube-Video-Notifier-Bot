# Discord News and YouTube Video Notifier Bot

This project is a Discord bot that monitors news and YouTube videos related to stock market, cryptocurrency, and economy topics and posts updates to configured Discord channels. It also includes a web scraper to fetch the latest news from specified sources.

---

### Features

- Scrapes latest news headlines and links from websites (Investing.com for stock market, crypto, and economy news).
- Polls YouTube channels for the latest videos using `scrapetube`.
- Posts updates to configured Discord channels using Discord bot commands.
- Maintains a local SQLite database to avoid reposting duplicate news or video notifications.
- Sends welcome messages to new Discord members.
- Periodically runs background tasks to check for news and new videos.

---

### Components

- **bot.py**: Main Discord bot implementation.
  - Uses `discord.py` with command prefix `!`.
  - Background tasks for news and video checking.
  - Maintains member count channel update.
  - Sends notifications to specified Discord channels.
- **scrape.py**: Web scraper module.
  - Functions to scrape stock market, cryptocurrency, and economy news from Investing.com.
- **test.py**: Simple test script to print videos from a YouTube channel using `scrapetube`.
- **youtubedata.json**: JSON configuration containing YouTube channel IDs, Discord channel IDs, and other metadata for notification routing.

---

### Requirements

- Python 3.7+
- `discord.py`
- `requests`
- `beautifulsoup4`
- `scrapetube`
- `sqlite3` (standard Python library)
- `python-dotenv` (for managing Discord bot token securely)

Install dependencies with:

---

### Setup Instructions

1. Clone the repository:
2. Create a `.env` file in the root directory containing your Discord bot token:
3. Configure the `youtubedata.json` file with YouTube channel IDs and corresponding Discord channel IDs for notifications.
4. Run the bot:

---

### Usage

- The bot will automatically post new news and YouTube videos to the configured Discord channels.
- Use the `!update` command in Discord to manually trigger member count updates.
- New members will receive a welcome direct message automatically.

---

### Notes

- The bot stores fetched news and video titles in a local SQLite database (`database.db`) to avoid duplicate postings.
- Scraper uses user-agent headers to mimic a browser request.
- Make sure your Discord bot has the necessary permissions to send messages and manage channels on your server.

---
### Acknowledge

This bot is designed for educational purposes and can be extended for various notification and scraping needs.
