import asyncio
from asyncio.log import logger
import logging
import os

import dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
dotenv.load_dotenv()
from wrapper import SlideShare,regex
log = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(__file__)
logging.basicConfig(filename=os.path.join(BASE_DIR,'log.txt'),level=logging.INFO)

TOKEN = str(os.getenv('token'))
bot = AsyncTeleBot(TOKEN)

STORAGE = os.path.join(BASE_DIR,'storage')
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
        Hi there, I am SlideShare downloader Bot.
            """)


@bot.message_handler(regexp=regex)
async def handle_msg(msg:Message):
    print(msg.text)
    sh = SlideShare()
    data  = await sh.slides(msg.text)  # type: ignore


if __name__ == '__main__':
    logger.info('[*] bot started')
    asyncio.run(bot.polling())
    logger.warning('[*] bot stopped')