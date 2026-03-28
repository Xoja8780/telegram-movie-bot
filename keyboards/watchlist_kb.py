from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

#  🔹 1. Главная клавиатура списка "Смотреть позже"

def watchlist_main_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎬 Показать с постерами",
                             callback_data="show_posters"),

    )
    builder.row(
        InlineKeyboardButton(text="❌ Очистить весь список",
                             callback_data="clear_watchlist")
    )
    return builder.as_markup()

# 🔹 2. Клава для режима постеров (показ фильмов по одному)

def watchlist_poster_kb(movie_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️ Предыдущий", callback_data=f"prev_{movie_id}"),
        InlineKeyboardButton(text="Следующий ➡️", callback_data=f"next_{movie_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🎞 Трейлер", callback_data=f"trailer_{movie_id}"))

    builder.row(
        InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_{movie_id}"),
        InlineKeyboardButton(text="🔙 Назад к списку", callback_data="back_to_watchlist")
    )
    return builder.as_markup()

# 🔹 3. Подтверждение очистки (на случай, если пользователь нажмёт “Очистить всё”)
def confirm_clear_watchlist_kb():

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Да, очистить", callback_data="confirm_clear"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_clear")
    )
    return builder.as_markup()

