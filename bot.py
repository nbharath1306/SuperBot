import random
import requests
import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load Bot Token
BOT_TOKEN = '7825154936:AAH2rynN3g66h1mYcPLiqmK1IhDYWO4eidc'

# Motivational Quotes
quotes = [
    "Believe in yourself! 🔥",
    "You are stronger than you think. 💪",
    "Dream it. Wish it. Do it. 🚀",
    "Stay positive, work hard, make it happen. 🎯",
    "Push yourself, because no one else is going to do it for you. 🏆",
]

# Jokes
jokes = [
    "Why don’t scientists trust atoms? Because they make up everything! 😂",
    "Parallel lines have so much in common. It’s a shame they’ll never meet. 🤣",
    "I'm reading a book about anti-gravity. It's impossible to put down! 😜",
]

# Dictionary for saving user secrets
user_secrets = {}

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Hello {update.effective_user.first_name}! 🚀 Welcome to SuperBot!\nUse /help to see commands.")

# Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = """
Available Commands:
/start - Start the bot
/motivate - Get a motivational quote
/weather <city> - Get weather updates
/crypto <coin> - Get crypto price (e.g., /crypto bitcoin)
/remindme <minutes> <task> - Get a reminder
/joke - Get a random joke
/secret <message> - Save a secret note
/viewsecret - View your saved secret
    """
    await update.message.reply_text(commands)

# Motivation Command
async def motivate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(quotes))

# Joke Command
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(jokes))

# Weather Command
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        city = ' '.join(context.args)
        api_key = "API_KEY_HERE"  # We'll fix this soon
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_info = f"🌤️ Weather in {city}:\nTemp: {data['current']['temp_c']}°C\nCondition: {data['current']['condition']['text']}"
            await update.message.reply_text(weather_info)
        else:
            await update.message.reply_text("Couldn't fetch weather! Try again later.")
    else:
        await update.message.reply_text("Usage: /weather <city>")

# Crypto Command
async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        coin = context.args[0].lower()
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if coin in data:
                price = data[coin]['usd']
                await update.message.reply_text(f"💸 {coin.capitalize()} price: ${price}")
            else:
                await update.message.reply_text("Coin not found. Try a different one.")
        else:
            await update.message.reply_text("Couldn't fetch price! Try again later.")
    else:
        await update.message.reply_text("Usage: /crypto <coin>")

# Reminder Command
async def remindme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) >= 2:
        minutes = int(context.args[0])
        task = ' '.join(context.args[1:])
        await update.message.reply_text(f"⏰ Reminder set for {minutes} minutes to: {task}")

        await asyncio.sleep(minutes * 60)
        await update.message.reply_text(f"🔔 Reminder: {task}")
    else:
        await update.message.reply_text("Usage: /remindme <minutes> <task>")

# Save Secret Command
async def secret(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        secret_msg = ' '.join(context.args)
        user_secrets[update.effective_user.id] = secret_msg
        await update.message.reply_text("🤫 Your secret has been saved!")
    else:
        await update.message.reply_text("Usage: /secret <message>")

# View Secret Command
async def viewsecret(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_secrets:
        await update.message.reply_text(f"🤫 Your secret: {user_secrets[user_id]}")
    else:
        await update.message.reply_text("You have no secrets saved.")

# Bot App
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Adding Command Handlers
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('help', help_command))
app.add_handler(CommandHandler('motivate', motivate))
app.add_handler(CommandHandler('joke', joke))
app.add_handler(CommandHandler('weather', weather))
app.add_handler(CommandHandler('crypto', crypto))
app.add_handler(CommandHandler('remindme', remindme))
app.add_handler(CommandHandler('secret', secret))
app.add_handler(CommandHandler('viewsecret', viewsecret))

print("SuperBot is running... 🚀")
app.run_polling()
