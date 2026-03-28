# кнопки с жанрами
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import GENRES

def genre_keyboard():
    # Кратко: создаёт inline-клавиатуру с кнопками жанров из `GENRES`.
    builder = InlineKeyboardBuilder()
    for gid, name in GENRES.items():
        builder.button(text=name, callback_data=f"genre:{gid}")
    builder.adjust(2)
    return builder.as_markup()