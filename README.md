# Valley Protocol Telegram Bot

Point Accumulation and Ad Viewing System via Telegram Bot

## Features

- User/Group Registration & Management
- Point System
  - Earn points by watching ads
  - Daily point earning limit
  - Individual/group point management
- Multilingual Support
  - Korean/English supported
  - Per-user/group language settings
- Ad System
  - Random ad display
  - Ad viewing history management
  - Automatic point distribution

## Project Structure

```
valley/
├── bot.py              # Main bot execution file
├── requirements.txt    # Project dependencies
├── messages/           # Multilingual messages
│   ├── ko_texts.py    # Korean messages
│   └── en_texts.py    # English messages
├── model/             # Database models
│   └── init/         # Database initialization
│       └── 01_create_tables.sql
└── handler/          # Bot handlers
    └── button_handlers.py
```

## Installation & Execution

1. Install Dependencies
```bash
pip install -r requirements.txt
```

2. Database Setup
- Create a PostgreSQL database
- Execute model/init/01_create_tables.sql

3. Environment Variables
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
```

4. Run Bot
```bash
python bot.py
```

## Database Schema

### users
- Stores user information and language settings

### groups
- Stores group information and language settings

### points
- Manages points for users/groups

### ads
- Manages ad content and activation status

### ad_view_logs
- Tracks ad viewing history and point earnings

## Usage Guide

1. Start Bot
```
/start
```

2. Check Points
```
/points
```

3. Watch Ads
- Click AD button
- Earn points once per day

4. Language Settings
- Click Language button
- Choose Korean/English

## License

MIT License 
