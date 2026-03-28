# кнопки для фильмов ("Назад", "Вперёд", "Смотреть позже")

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def movie_keyboard(genre_id: int, movie_index: int, total_movies: int) -> InlineKeyboardMarkup:
    kb = []

    nav_row = []

    if movie_index > 0:
        nav_row.append(
            InlineKeyboardButton
                  (text="⬅️ Предыдущий",
                   callback_data=f"prev_movie:{genre_id}:{movie_index - 1}"
            )
        )

    if movie_index < total_movies - 1:
        nav_row.append(
            InlineKeyboardButton
                  (text="Следующий ➡️",
                   callback_data=f"next_movie:{genre_id}:{movie_index + 1}"
            )
        )
    if nav_row:
        kb.append(nav_row)

    kb.append([
        InlineKeyboardButton(
            text="🎞 Трейлер",
            callback_data=f"trailer_{genre_id}:{movie_index}"
        )
    ])


    kb.append([
        InlineKeyboardButton(
        text="⭐ Смотреть позже",
        callback_data=f"watch_later:{genre_id}:{movie_index}"
        )
    ])
    kb.append([
        InlineKeyboardButton(
            text="🔙 Назад к жанрам",
            callback_data="back_to_genres"
        )
    ])


    return InlineKeyboardMarkup(inline_keyboard=kb)


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎭 Жанры"),
             KeyboardButton(text="📺 Смотреть позже")]
        ],
        resize_keyboard=True
    )
