import asyncio
import random
import time

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
import keyboards
import db_api
import os

TOKEN = '6337362490:AAHhSiWLamaeUB5Cc4Jk2mVMmt4xMDwfOxI'
bot = Bot(TOKEN)
dp = Dispatcher()
PASSWORD = '123'
IMAGES_PATH = os.path.join(os.path.dirname(__file__), 'images')
COOLDOWN = 4 * 60 * 60
PLAYERS_WAIT = set()


@dp.message(Command('start'))
async def start(message: Message):
    db_api.add_user(message.chat.id)
    album_builder = MediaGroupBuilder(
        caption="Do'stim, qarang, odamlar bu bilan qanday qilib pul topishadi!"
    )
    for i in range(1, 4):
        album_builder.add_photo(
            media=FSInputFile(os.path.join(IMAGES_PATH, f"img{i}.png"))
        )
    await message.answer_media_group(
        media=album_builder.build()
    )
    await asyncio.sleep(2)
    await message.answer('💰Bu bot sizga kamida 120 000 daromad olish imkonini beradi! 💰\n'
                         '🚀Va bu 1 soat ichida! 🚀\n'
                         'Start tugmasini bosing va pul ishlashni boshlang!📈💵', reply_markup=keyboards.start())


@dp.callback_query(F.data == 'next_message')
async def next_message(call: CallbackQuery):
    await call.message.answer(
        'Balansingiz 140 000 bo\'lishi kerak! Aks holda bot ishlamaydi!',
        reply_markup=keyboards.get_first_signal()
    )


@dp.callback_query(F.data == 'get_signal')
async def get_signal(call: CallbackQuery):
    if call.message.chat.id in PLAYERS_WAIT:
        return

    user = db_api.get_user(call.message.chat.id)
    if (user[1] >= 20) and (time.time() - user[2] < COOLDOWN):
        return await call.message.answer(
            '⛔️!STOP! ⛔️\n'
            'O\'yinda shubhali faoliyat bor!\n'
            'Bot ishlashda davom etishi uchun siz 70 000 ga to\'ldirishingiz kerak! 📈💵',
            reply_markup=keyboards.get_me()
        )

    tries = user[1]
    if tries >= 20:
        db_api.update_tries(call.message.chat.id, 0)
        tries = 0

    PLAYERS_WAIT.add(call.message.chat.id)
    await call.message.answer('Tikishlarni tekshirish🚀')
    await asyncio.sleep(random.randint(1, 3))

    await call.message.answer(
        f'PLAYER: @{call.message.from_user.username}\n'
        f'*CASHOUT: %.2f ✅*' % round(random.randint(100, 250)/100, 2),
        parse_mode='markdown',
        reply_markup=keyboards.get_next_signals()
    )

    PLAYERS_WAIT.remove(call.message.chat.id)
    db_api.update_timestamp_user(call.message.chat.id)
    db_api.update_tries(call.message.chat.id, tries+1)


asyncio.run(dp.start_polling(bot, storage=MemoryStorage()))
