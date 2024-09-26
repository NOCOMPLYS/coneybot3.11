from aiogram import Router, Dispatcher, F
from aiogram.methods.send_message import SendMessage
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from database.sqlite_db import db
from decouple import config
from create_bot import bot

# переменные для работы
ADMIN_ID = config('ADMIN_ID')
ADMIN_ID_2 = config('ADMIN_ID_2')
ADMIN_ID_3 = config('ADMIN_ID_3')
BOT_TOKEN = config("BOT_TOKEN")
HOST = config("HOST")
PORT = int(config("PORT"))
WEBHOOK_PATH = f'/{BOT_TOKEN}'
BASE_URL = config("BASE_URL")

admins = [int(ADMIN_ID), int(ADMIN_ID_2), int(ADMIN_ID_3)]
router = Router()

def is_int(text):
    try:
        val = int(text)
        return True
    except ValueError:
        return False

# функция для реагирования на команду /start
@router.message(CommandStart())
async def start_command(message: Message):
    user = message.from_user.id
    users = []
    for m in db.get_users():
        users.append(m[0])
    if user not in users:
        await message.answer('Приветствую! 👋\nЗдесь вы можете пройти регистрацию на бесплатный онлайн вебинар.')
        await message.answer('Как вас зовут?')
    else:
        await message.answer('Вы уже зарегистрированы.')
        await message.answer('🔔 Не забудьте включить уведомления, чтобы не пропусить напоминание о вебинаре.')

# Функция для реагирования на кнопку Зарабатывать
@router.message(F.text.lower() == "зарабатывать")
async def send_mentor(message: Message):
    users = []
    for m in db.get_users():
         users.append(m[0])
    if message.from_user.id in users:
        await message.answer('Я вижу вы готовы перейти к заработку. Вашим личным менеджером будет ')
    else:
        await message.answer('Уже скоро. Сперва скажите как вас зовут')

# функция для реагирования на команду /sql
@router.message(F.text, Command("sql"))
async def send_sql_db(message: Message):
    if message.from_user.id in admins:
        table = open('database.db', 'rb')
        await message.answer('Текущая таблица прикреплена ниже')
        await message.answer_document(FSInputFile("database.db"))

# функция для реагирования на команду /cancel
@router.message(F.text, Command("cancel"))
async def cancel_notif(message: Message):
    if message.from_user.id in admins:
        for i in range(len(admins)):
            if admins[i] == message.from_user.id:
                id = i + 1
        db.cancel_waiting(id)
        await message.answer('Действие отменено')

# функция для реагирования на команду /send
@router.message(F.text, Command("send"))
async def send_notif(message: Message):
    if message.from_user.id in admins:
        for i in range(len(admins)):
            if admins[i] == message.from_user.id:
                id = i + 1
        db.set_waiting(id, 'waiting')
        await message.answer('Пришли текст оповещения')

# функция для реагирования на команду /add
@router.message(F.text, Command("add"))
async def add_mentor(message: Message):
    if message.from_user.id in admins:
        for i in range(len(admins)):
            if admins[i] == message.from_user.id:
                id = i + 1
        db.set_waiting(id, 'waiting_mentor_add')
        await message.answer('Пришли никнейм и имя ментора как показано снизу:\n@jhonybeegood Николай')

# функция для реагирования на команду /del
@router.message(F.text, Command("del"))
async def add_mentor(message: Message):
    if message.from_user.id in admins:
        for i in range(len(admins)):
            if admins[i] == message.from_user.id:
                id = i + 1
        db.set_waiting(id, 'waiting_mentor_del')
        await message.answer('Пришли никнейм ментора как показано снизу:\n@jhonybeegood')

@router.message(F.text)
async def no_type_message(message: Message):
    # Приcваивание переменной user значение id пользователя для дальнейшега удобства в использовании
    user = message.from_user.id
    users = []
    for m in db.get_users():
        users.append(m[0])
    if user in admins:
        for i in range(len(admins)):
            if admins[i] == user:
                id = i + 1
        data = db.get_waiting(id)
        if data[1] == 1:
            db.cancel_waiting(id)
            for bot_user in users:
                try:
                    await bot.send_message(bot_user, message.text)
                except:
                    pass
            await message.answer('Сообщение успешно разослано пользователям!')
        elif data[2] == 1:
            db.cancel_waiting(id)
            nick, name = map(str, message.text.split())
            nick = nick.replace("@", "")
            db.add_mentor(nick, name)
            await message.answer("Вы успешно добавили ментора!")
        elif data[3] == 1:
            db.cancel_waiting(id)
            nick = message.text.replace("@", "")
            db.del_mentor(nick)
            await message.answer("Вы успешно удалили ментора!")
            #except:
                #await message.answer("Ошибка! Проверь правильно ли введён никнейм")

    if user not in users:
        db.add_user(user_id=message.from_user.id, nickname=message.from_user.username)
        db.set_name(user, message.text)
        await message.answer('Приятно познакомиться! Подскажи, сколько тебе лет?')

    elif user in users and db.get_name(user)[0] != None and db.get_age(user)[0] == None:
        if is_int(message.text):
            db.set_age(user, int(message.text))
            await message.answer('Регистрация прошла успешно!')
            await message.answer('https://t.me/+n4Vp4UpZJgs4ZDAy')
        else:
            await message.answer('Я тебя не понял. Пришли мне свой возраст числом.')

#def register_client_handlers(dp: Dispatcher):
 #   dp.message.register(start_command, commands=['start'])
  #  dp.register_message_handler(send_sql_db, commands=['sql'])
   # dp.register_message_handler(send_notif, commands=['send'])
    #dp.register_message_handler(no_type_message, content_types=['text'])
