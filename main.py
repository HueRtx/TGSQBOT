import logging, config, sys, psutil, cpuinfo, sqlite3
from aiogram import Bot, Dispatcher, executor, types
from cpuinfo import get_cpu_info
#базовые переменные
bot = Bot(config.token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
#подключение бд
conn = sqlite3.connect('users.db')
cur = conn.cursor()
#создание таблицы
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INT PRIMARY KEY,
   username TEXT,
   firstname TEXT,
   lastname TEXT);
""")
conn.commit()
#хэндлер на старт
@dp.message_handler(commands=["start"])
async def cmd_inline_url(message: types.Message):
    #получаем ID для проверки в бд
    userid = message.from_user.id
    #инлайн клавиатура
    buttons = [
        types.InlineKeyboardButton(text="Обо мне", callback_data="bio"),
        types.InlineKeyboardButton(text="Сайт владельца", url="https://floduat.org/"),
        types.InlineKeyboardButton(text="Блог владельца", url="tg://resolve?domain=kegablog"),
    ]
    #смотрим в бд
    info = cur.execute('SELECT * FROM users WHERE userid=?', (userid,))
    #если юзера в бд нет
    if info.fetchone() is None:
        cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}", "@{message.from_user.username}", "{message.from_user.first_name}","{message.from_user.last_name}" )')
        conn.commit()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await message.answer("Привет! Ты попал в бота который может рассказать информацию об Floduat.(@Alobzbz)",
                         reply_markup=keyboard)
    #если есть
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await message.answer("Привет! Ты попал в бота который может рассказать информацию об Floduat.(@Alobzbz)",
                         reply_markup=keyboard)
#а дальше комментировать мне лень
@dp.callback_query_handler(text_contains='bio')
async def bio(call: types.CallbackQuery):
    newButtons = [
        types.InlineKeyboardButton(text="⬅Назад", callback_data="back1"),
        types.InlineKeyboardButton(text="Мой пк", callback_data="pc"),
    ]
    secondKeyboard = types.InlineKeyboardMarkup(row_width=1)
    secondKeyboard.add(*newButtons)
    await bot.edit_message_text(text = f'Привет! Это кега или же FLoduat, простой человек из Беларуси(UTC+3 - Moscow '
                                       f'Time)!\n Я немного разбираюсь в python и JavaScript. Еще чуть-чуть в '
                                       f'компах.\n Мой талисман - хомяк.', chat_id = call.message.chat.id,
                                message_id = call.message.message_id, reply_markup = secondKeyboard)
@dp.callback_query_handler(text_contains='back1')
async def back1(call: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Обо мне", callback_data="bio"),
        types.InlineKeyboardButton(text="Сайт владельца", url="https://floduat.org/"),
        types.InlineKeyboardButton(text="Блог владельца", url="tg://resolve?domain=kegablog"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await bot.edit_message_text(text="Привет! Ты попал в бота который может рассказать информацию об Floduat.(@Alobzbz)",chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
@dp.callback_query_handler(text_contains='pc')
async def pc(call: types.CallbackQuery):
    Buttons = [
        types.InlineKeyboardButton(text="⬅Назад", callback_data="bio"),
        types.InlineKeyboardButton(text="Техническая информация о боте", callback_data="server"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*Buttons)
    await bot.edit_message_text(
        text="Характеристики моего пк:\n Процессор: Ryzen 5 3600\n Материнская плата: B550 Aorus Pro\n Оперативная "
             "память: Geil evo spear 3000mhz, kit 2pcs 8gb\n Видеокарта: RTX 2060 palit (6gb VRAM)",
        chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
@dp.callback_query_handler(text_contains='servertex')
async def servertex(call: types.CallbackQuery):
    Buttons = [
        types.InlineKeyboardButton(text="⬅Назад", callback_data="server"),
        types.InlineKeyboardButton(text="⬅В начало", callback_data="back1")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*Buttons)
    cpumodel=cpuinfo.get_cpu_info()['brand_raw']
    cpuarch=cpuinfo.get_cpu_info()['arch']
    amountram=round(psutil.virtual_memory().total / (1024.0**3), 2)
    await bot.edit_message_text(
        text=f"CPU сервера: {cpumodel}\n Архитектура CPU: {cpuarch}\nСколько RAM в сервере: {amountram}GB\n",
        chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

@dp.callback_query_handler(text_contains='server')
async def server(call: types.CallbackQuery):
    Buttons = [
        types.InlineKeyboardButton(text="⬅Назад", callback_data="pc"),
        types.InlineKeyboardButton(text="Техническия характеристики на сервере бота", callback_data="servertex"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    platforma=sys.platform
    pyver=sys.version
    keyboard.add(*Buttons)
    await bot.edit_message_text(
        text=f"Bot version 0.3 (Alpha), спасибо @i3sey (и другим)!\n Ядро ОС: {platforma}\n Версия python: {pyver}",
        chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)



if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
#cpu model cpuinfo.get_cpu_info()['brand_raw']