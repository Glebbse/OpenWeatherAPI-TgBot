from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kbd(
        *btns: str,
        placeholder: str,
        sizes: tuple
):
    kbd = ReplyKeyboardBuilder()
    for text in btns:
        kbd.add(KeyboardButton(text=text))

    return kbd.adjust(* sizes).as_markup(input_field_placeholder=placeholder, resize_keyboard=True)