from aiogram import Dispatcher, Bot
from sys_files.config import TOKEN_BOT
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

bot = Bot(token=TOKEN_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)