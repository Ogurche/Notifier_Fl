import asyncio
from datetime import datetime
from sys_files.creation_bot import bot,dp
from aiogram import types
from aiogram import executor
import main_scenario
from sys_files.config import ADMIN_ID

async def startup(_):
    print('Бот запущен!')


@dp.message_handler(commands=['start'])
async def start_command(message:types.Message):
    await message.answer(""" Привет, я бот для фрилансеров.
Я помогу тебе получать напоминания, если на бирже появится новый заказ.
Для начала нажми /setup

Я еще нахожусь в разработке.
Если найдешь баги или будут предложения, пиши сюда https://t.me/ogurch1k. 
Хорошей работы !) """)


main_scenario.register_handlers(dp)


@dp.message_handler()
async def echo_answers( message: types.Message):
    await message.reply(text="Честно скажу, я не понял чего ты хочешь.")

async def sheduleder (waiting_time):
    n=0
    while True: 
        await asyncio.sleep(waiting_time)
        
        now = datetime.now()
        await bot.send_message (chat_id = '',text = now )



if __name__ == '__main__':
    #TODO поменять get_event_loop (Выдает DeprecationWarning)

    # loop = asyncio.get_event_loop()
    # loop.create_task (sheduleder(5))

    executor.start_polling (dp, skip_updates =True, on_startup=startup)