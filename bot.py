import json
import html
__version__ = '0.0.1'
__author__ = 'Ahmed Hassan'
import traceback
import logging
import img2pdf
import os
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update, ParseMode
from wrapper import SlideShare, regex
from dotenv import dotenv_values
from requests import get
config = dotenv_values(".env")
token = config.get('token', os.environ.get('token'))
developer_id = config.get('developer_id', os.environ.get('developer_id'))

BASE_DIR = os.path.dirname(__file__)
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

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    context.bot.send_message(chat_id=developer_id,
                             text=message, parse_mode=ParseMode.HTML)

# ________________________________________________________
# ____Bot Functions_______________________________________


def start(update: Update, context: CallbackContext):
    slide_photo = open('photos/slideshare.jpg', 'rb')
    update.message.reply_photo(
        slide_photo, caption='ابعت اللينك يا برو واستنى العظمة')
    update.message.reply_text("""Make Sure That The link in this form 
    https://www.slideshare.net/******/****""")


def download_slides(update: Update, context: CallbackContext):
    meme_photo = open('photos/meme.jpg', 'rb')
    slideshare = SlideShare()
    message = update.message
    message_link = message.text
    validated_link = slideshare.valid_link(message_link.strip())
    # User data
    user_data = update.message.from_user
    if validated_link:

        slides_data = slideshare.slides(message_link)
        if slides_data is not None:
            photos = slides_data.get('slides')
            message.reply_text(f"""

        Title : {slides_data.get('title')}

        instructor : {slides_data.get('author')}

        Slides:{slides_data.get('count')}

            """)

            # for i, photo in enumerate(photos):
            #     update.message.reply_photo(
            #         photo, caption=f'{slides_data.get("title")} - {i+1}')

            photos_data = [get(_).content for _ in photos]
            pdf_data = img2pdf.convert(photos_data)
            update.message.reply_document(pdf_data, caption=slides_data.get(
                'title'), filename=f'{slides_data.get("title")}.pdf')

            notification_msg = (
                f'User:\n {user_data.first_name}'
                f'\nDownloaded This Slide:\n <strong>{slides_data.get("title")}</strong> Successfully'
                f'\nLink : {message_link}')
            context.bot.send_message(
                chat_id=developer_id, text=notification_msg, parse_mode=ParseMode.HTML)

        else:
            message.reply_photo(meme_photo, caption='اللينك دا مش شغال')

    else:

        message.reply_photo(meme_photo, caption='اللينك دا مش شغال')
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
