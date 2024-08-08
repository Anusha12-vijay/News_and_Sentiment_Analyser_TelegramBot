import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from utils import get_reply, fetch_news

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

Token = "7313342895:AAE1HGAQigzgkPlOY_Vx_UhRdEsY8eGy6z0"
Webhook_URL = "https://73988946a8434c571a12cc91a6500a34.serveo.net"  # Your public URL

app = Flask(__name__)

# Initialize the bot
bot = Bot(Token)

@app.route('/')
def index():
    return "Hello!"

@app.route(f'/{Token}', methods=['GET', 'POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    application.update_queue.put(update)  # Add the update to the application queue
    return "Ok"

async def start(update: Update, context: CallbackContext) -> None:
    author = update.message.from_user.first_name
    reply = f"Hi! {author}"
    await context.bot.send_message(chat_id=update.message.chat_id, text=reply)

async def _help(update: Update, context: CallbackContext) -> None:
    help_text = "Heyy! This is a help text."
    await context.bot.send_message(chat_id=update.message.chat_id, text=help_text)

async def reply_text(update: Update, context: CallbackContext) -> None:
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == 'get_news':
        logger.info(f"Fetching news with parameters: {reply}")
        articles = fetch_news(reply)
        if not articles:
            await context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, no news articles were found.")
        else:
            for article in articles:
                logger.info(f"Sending article: {article['link']}")
                await context.bot.send_message(chat_id=update.message.chat_id, text=article['link'])
    else:
        await context.bot.send_message(chat_id=update.message.chat_id, text=reply)

async def echo_sticker(update: Update, context: CallbackContext) -> None:
    await context.bot.send_sticker(chat_id=update.message.chat_id, sticker=update.message.sticker.file_id)

async def error(update: Update, context: CallbackContext) -> None:
    logger.error("Update '%s' caused error '%s'", update, context.error)

async def sentiment(update: Update, context: CallbackContext) -> None:
    sentiment_link = "http://localhost:8501"  # Replace with your actual link
    await context.bot.send_message(chat_id=update.message.chat_id, text=f"Check out this sentiment analysis tool: {sentiment_link}")

def main():
    global application
    application = Application.builder().token(Token).build()
    
    # Set up handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", _help))
    application.add_handler(CommandHandler("sentiment", sentiment))  # Add the new handler here
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_text))
    application.add_handler(MessageHandler(filters.Sticker.ALL, echo_sticker))

    # Error handler
    application.add_error_handler(error)

    # Set webhook
    bot.set_webhook(Webhook_URL + '/' + Token)
    
    # Run the application
    application.run_polling()

if __name__ == "__main__":
    main()
    #asyncio.run(main())s
    app.run(port=80)
