from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def constructor_keyboard(call):
    def func() -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        call(keyboard)
        return keyboard.as_markup()

    return func


@constructor_keyboard
def start(keyboard: InlineKeyboardBuilder):
    keyboard.row(InlineKeyboardButton(text='Start', callback_data='next_message'))


@constructor_keyboard
def get_first_signal(keyboard: InlineKeyboardBuilder):
    keyboard.row(InlineKeyboardButton(text='BOSHLANISHI', callback_data='get_signal'))


@constructor_keyboard
def get_me(keyboard: InlineKeyboardBuilder):
    keyboard.row(InlineKeyboardButton(text='Yordam 💬', url='https://t.me/axrorov_cash'))


@constructor_keyboard
def get_next_signals(keyboard: InlineKeyboardBuilder):
    keyboard.add(InlineKeyboardButton(text='Win💰', callback_data='get_signal'))
    keyboard.add(InlineKeyboardButton(text='Lose⛔️', callback_data='get_signal'))
