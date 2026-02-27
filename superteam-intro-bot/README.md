Superteam MY – Intro Gatekeeper Bot

Production-ready Telegram onboarding bot



This bot enforces structured introductions before allowing members to participate in the main group discussion.

Designed for real community deployment.

🚀 Features

✅ Detects new members automatically

🔒 Restricts messaging until intro is completed

🧵 Validates intro inside a specific forum thread

🎯 Light intro validation (minimum structure & length)

🎉 Automatically grants full permissions after approval

💾 Persistent SQLite storage

🛠 Admin reset command

🐳 Docker-ready deployment

🧾 Structured logging



🧠 How It Works

A user joins the group

Bot restricts them from sending messages

Bot DMs intro instructions

User posts intro in designated thread

Bot validates intro

If valid → permissions restored automatically



1️⃣ Create the Telegram Bot

Open Telegram

Search for @BotFather

Send:

/newbot

Follow instructions

Copy the Bot Token


2️⃣ Get Your Group ID
Method 1 (Recommended)

Add the bot to your group

Temporarily add this line inside handle_intro:

print(update.effective_chat.id)

Send a message in the group

Check console output

Group ID will look like:

-1001234567890


3️⃣ Get the Intro Thread ID

If your group uses Topics (Forum Mode):

Go to the Intro topic

Look at the message URL:

https://t.me/SuperteamMY/2238

The last number (2238) is your INTRO_THREAD_ID.


4️⃣ Environment Setup

Rename:

.env.example → .env

Then fill in:

BOT_TOKEN=YOUR_BOT_TOKEN
GROUP_ID=-100XXXXXXXXXX
INTRO_THREAD_ID=2238


5️⃣ Install & Run Locally
pip install -r requirements.txt
python -m bot.main

⚠️ Do NOT run python bot/main.py
The project uses proper package imports.



🐳 Docker Deployment

Build image:

docker build -t superteam-intro-bot .

Run container:

docker run --env-file .env superteam-intro-bot

For persistent database storage (recommended in production):

docker run -v $(pwd)/data:/app/data --env-file .env superteam-intro-bot


🔐 Required Bot Permissions

Make sure the bot is added as Administrator with:

✅ Restrict Members

✅ Delete Messages

✅ Send Messages

✅ Invite Users (optional but recommended)

Without Restrict permission, onboarding will fail.



🧵 Important: Forum Topics Must Be Enabled

If using thread-based intro validation:

Go to:

Group Settings → Enable Topics = ON

If Topics are disabled, message_thread_id will not work and validation will fail.



🛠 Admin Commands
Reset a User
/reset <user_id>

Resets intro status and restricts the user again.

(Admin-only command.)



📦 Project Structure
bot/
│
├── main.py
├── onboarding.py
├── intro_handler.py
├── admin.py
├── database.py
├── validators.py
├── config.py
└── __init__.py
⚙️ Optional Production Dependency

For improved rate limiting stability on platforms like Render or Railway:



python-telegram-bot[rate-limiter]==20.7
python-dotenv==1.0.1
🧾 License

MIT