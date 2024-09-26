from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# инициализируем бота и диспетчера для работы с ним
bot = Bot(token='7554613342:AAHq7G6wfPpUpNc8TsHCdrffzu4lJ-sJrjo', default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
