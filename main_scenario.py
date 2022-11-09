import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters import Text, ContentTypeFilter


import messages.messages_to_send as messages_to_send
from sys_files.creation_bot import bot,dp
import habr 


class FSM_user(StatesGroup):
    username = State() 
    category = State()
    sub_category = State()
    notifier = State()


# TODO Если id есть в базе данных 
# Если есть добавить измененное сообщение (Если хочешь можем поменять специальность)
# Вывести сообщение сейчас я оповещаю по {} специальностям


#@dp.message_handler(commands=['setup'])
async def setup_command (message: types.Message):
    await messages_to_send.welcome_sticker(chat_id=message.chat.id )
    await messages_to_send.setup_button()
    await FSM_user.username.set()


#@dp.message_handler(Text(equals="Хочу обратно, мне страшно"), state='*')
#@dp.message_handler(commands=['start','setup'], state='*')
async def cancel_setup (message: types.Message, state:FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Возвращаемся в главное меню!')
        # вставить возврат в главное меню 


#@dp.message_handler(FSM_user.username, Text(equals="Давай"))
async def setup_username_checker (message:types.Message , state:FSMContext):
    await messages_to_send.first_enter_message()
    await FSM_user.category.set()


#@dp.message_handler(state=FSM_user.category, content_types=['text'])
async def category_selector(message:types.Message, state:FSMContext):
    async with state.proxy () as data:
        data["name"] = message.text
        data['id'] = message.chat.id
    await messages_to_send.category_message(data['name'])
    await FSM_user.sub_category.set()

#@dp.message_handler(state=FSM_user.sub_category)
async def sub_category_development_selector (message: types.Message, state:FSMContext):
    async with state.proxy () as data:
        data["category"] = message.text
    await messages_to_send.sub_category_development_keybord (message = message.text )
    await FSM_user.notifier.set()


#@dp.callback_query_handler(state= FSM_user.notifier)
async def callback_sub_category_saver (callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['sub_category'] = callback.data 
    await bot.send_message (chat_id= data['id'] , text= "Сейчас посмотрим, что есть")
    parse_result = habr.categorize(categories= data['sub_category'])

    for result in parse_result:
        order = result['order_name']
        link = result [ 'link' ]
        price = result [ 'order_price' ]
        await bot.send_message (chat_id= data['id'], text = f'{order}\n\n{price}\n{link}')
        await asyncio.sleep(1)
    await messages_to_send.notifier(category=data ['category'], sub_category= data ['sub_category'])




#@dp.message_handler(state="*")
async def state_garbage_handler (message: types.Message, state:FSMContext):
    await message.reply('Есть ощущение, что ты написал что-то не то. Попробуй еще раз')
        


def register_handlers(dp:Dispatcher):
    dp.register_message_handler (setup_command, commands=['setup'])
    dp.register_message_handler (cancel_setup, Text(equals="В главное меню"), state="*")
    dp.register_message_handler (cancel_setup, commands=['start','setup'], state="*")
    dp.register_message_handler (setup_username_checker, Text(equals="Давай"), state=FSM_user.username)
    dp.register_message_handler (category_selector, state=FSM_user.category)
    dp.register_message_handler (sub_category_development_selector, state=FSM_user.sub_category)
    dp.register_callback_query_handler (callback_sub_category_saver, state=FSM_user.notifier)
    
    


    dp.register_message_handler(state_garbage_handler, state='*')