import asyncio
from typing import Union
from aiogram import types
from sys_files.creation_bot import bot
from aiogram.utils.exceptions import BotBlocked
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


async def get_chat_id() -> int:
    """This function used to get current chat id"""
    return types.Chat.get_current().id

async def send_message(
        message_text: str,
        reply_markup: Union[
            types.ReplyKeyboardMarkup,
            types.InlineKeyboardMarkup,
            types.ReplyKeyboardRemove] = None,
        user_id: Union[int, None] = None,
        photo: Union[
            str,
            types.InputFile
        ] = None,
        reply_to_message_id: int = None,
        disable_web_page_preview: bool = True) -> Union[types.Message, None]:
    """
    This function used to send message to user, with default keyboard if keyboard not given in arg
    if user is admin method send message using admin keyboard

    :param message_text: message text, required parameter
    :param reply_markup: keyboard sent with message
    :param parse_mode: message parse mode
    :param user_id: to message user id
    :param photo: photo sent with message
    :param reply_to_message_id: reply to message id
    :param disable_web_page_preview: disable web page preview
    :return: sent message
    """

    try:
        if user_id is None:
            user_id = await get_chat_id()

        if photo:
            return await bot.send_photo(user_id, photo=photo, caption=message_text,
                                        reply_markup=reply_markup, reply_to_message_id=reply_to_message_id)

        return await bot.send_message(user_id, message_text, reply_markup=reply_markup,
                                      reply_to_message_id=reply_to_message_id,
                                      disable_web_page_preview=disable_web_page_preview)
    except BotBlocked:
        return


async def first_enter_message ():
    await send_message(message_text="Мы видимся впервые, давай знакомится)\nКак к тебе обращаться?")


async def welcome_sticker(chat_id):
    await bot.send_sticker (chat_id=chat_id , sticker="CAACAgEAAxkBAAEGKBdjUoaZb12tmQ39SJqVHQdkbN2e2AACFAADRLsVDB0MX0W0MQqOKgQ")


async def yes_no_keybord ():
    keybord = ReplyKeyboardMarkup(resize_keyboard=True , one_time_keyboard= True)
    keybord.add ("Давай", "В главное меню")
    return keybord

async def setup_button():
    keybord = await yes_no_keybord()
    await send_message (message_text="Ну что, давай настроим уведомления", reply_markup= keybord)

async def category_message (name):
    keybord = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keybord.add ("Разработка","Тестирование")
    keybord.add ("Администрирование","Дизайн")
    keybord.add ("Контент", "Маркетинг")
    await send_message (message_text= f'Привет {name} выбери категорию',reply_markup=keybord)


async def sub_category_development_keybord(message):
    in_keybord = InlineKeyboardMarkup (row_width= 2)

# TODO переделать колбэк дату под парсер 
    if message == 'Разработка':
        category_list = [
            "Сайты «под ключ»",
            'Бэкенд',
            'Фронтенд',
            'Прототипирование',
            'iOS',
            'Android',
            'Десктопное ПО',
            'Боты и парсинг данных',
            'Разработка игр',
            '1С-программирование',
            'Скрипты и плагины',
            'Голосовые интерфейсы',
            'Разное'
            ]
        callback = [ 'development_all_inclusive', 'development_backend', 'development_frontend',
        'development_prototyping', 'development_ios', 'development_android', 'development_desktop',
        'development_bots', 'development_games', 'development_1c_dev',
        'development_scripts','development_voice_interfaces','development_other' ]
        menu = []

        while len(menu) < len(category_list):
            menu.append (InlineKeyboardButton (text= category_list[len(menu)], callback_data= callback[len(menu)]))
        all_callback = ','.join(callback)
        select_all_button = InlineKeyboardButton (text="Выбрать все", callback_data= all_callback)

        in_keybord.add (*menu)
        in_keybord.insert (select_all_button)
        await send_message(message_text= f"В категории {message} есть такие подкатегории:" , reply_markup=in_keybord)
    
    else: 
        await send_message(f'Категория {message} пока не работает')


async def notifier (category,sub_category):
    keybord = await yes_no_keybord()
    await send_message(f'Запускаю напоминания по категории {category} - {sub_category}', reply_markup = keybord)
