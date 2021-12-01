import traceback
import logging
import os
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
from wrapper import SlideShare, regex
from dotenv import dotenv_values
config = dotenv_values(".env")
token = config.get('token')
developer_id = config.get('developer_id')

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""

    logger.error(msg="Exception while handling an update:",
                 exc_info=context.error)
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

# ________________________________________________________
# ____Bot Functions_______________________________________


def start(update: Update, context: CallbackContext):
    photo = open('photos//slideshare.jpg', 'rb')
    update.message.reply_photo(
        photo, caption='ابعت اللينك يا برو واستنى العظمة')
    update.message.reply_text("""Make Sure That The link in this form 
    https://www.slideshare.net/victorhernandez9/mobile-me-programming-for-wearables""")


def download_slides(update: Update, context: CallbackContext):
    slideshare = SlideShare()
    message_link = update.message.text
    validated_link = slideshare.valid_link(message_link.strip())
    if validated_link:
        slides_data = slideshare.slides(message_link)
        photos = slides_data.get('slides')
        update.message.reply_text(f"""

        Title : {slides_data.get('title')}

        instructor : {slides_data.get('author')}

        Slides:{slides_data.get('count')}

        *** Due To Server Limitations The Slides Will Be Sent as Photos ***
        """)
        for i, photo in enumerate(photos):
            update.message.reply_photo(
                photo, caption=f'{slides_data.get("title")} - {i+1}')
    else:
        update.message.reply_text('اللينك دا مش شغال')
# ________________________________________________________


def main() -> None:
    """Start the bot."""
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_error_handler(error_handler)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(
        Filters.regex(regex), download_slides))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
