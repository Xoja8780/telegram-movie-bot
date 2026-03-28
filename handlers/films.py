from aiogram import Router, types, F
from services.tmdb_api import get_movies_by_genre, get_movie_videos, get_youtube_trailer_url
from config import GENRES
from keyboards.movie_keyboard import movie_keyboard
from keyboards.genre_keyboard import genre_keyboard
from aiogram.types import InputMediaPhoto

router = Router()

import random
def make_movie_caption(film, genre_name):
    """Формирует красивый текст описания фильма."""


    title = film.get("title", "Без названия")
    date = film.get("release_date", "Дата неизвестна")
    rating = film.get("vote_average", 0)
    description = film.get("overview")

    no_desc_phrases = [
        "Создатели забыли рассказать, о чём фильм 🤫",
        "Описание где-то затерялось между кадрами 🎞️",
        "Пока без описания — видимо, сюжет держат в секрете 👀",
        "Сюжет засекречен, как рецепт кока-колы 🕵️",
    ]

    if description and description.strip():
        desc_text = description.strip()
    else:
        desc_text = random.choice(no_desc_phrases)

    return (
        f"🎬 <b>{title}</b> ({date})\n"
        f"⭐ {rating}\n\n"
        f"📖 {desc_text}\n\n"
        f"🎭 Жанр: <b>{genre_name}</b>"
    )


@router.callback_query(F.data.startswith("genre:"))
async def show_movies_by_genre(callback: types.CallbackQuery):
    genre_id = int(callback.data.split(":")[1])
    genre_name = GENRES.get(genre_id, "Неизвестный жанр")

    await callback.message.edit_text(f"🔍 Загружаю фильмы жанра <b>{genre_name}</b>...")

    try:
        await callback.message.delete()
    except:
        pass

    try:
        films = get_movies_by_genre(genre_id)
        if not films:
            await callback.answer("😕 Фильмы не найдены.", show_alert=True)
            return
        # 🎲 Выбираем первый фильм
        film = films[0]
        poster_url = f"https://image.tmdb.org/t/p/w500{film.get('poster_path', '')}"
        caption = make_movie_caption(film, genre_name)


        await callback.message.answer_photo(
            photo=poster_url,
            caption=caption,
            parse_mode="HTML",
            reply_markup=movie_keyboard(genre_id, 0, len(films)))

    except Exception as e:
        await callback.message.answer(f"❌ Ошибка: {e}")


@router.callback_query(F.data == "back_to_genres")
async def back_to_genres(callback: types.CallbackQuery):
    await callback.message.answer("🎬 Выбери жанр фильма:", reply_markup=genre_keyboard())


@router.callback_query(F.data.startswith("next_movie:"))
async def next_movies(callback: types.CallbackQuery):
    try:
        genre_id, movie_index = map(int, callback.data.split(":")[1:3])
        films = get_movies_by_genre(genre_id)
        total_movies = len(films)

        if not films or movie_index >= total_movies:
            await callback.answer("😕 Фильмы не найдены.", show_alert=True)
            return

        film = films[movie_index]
        genre_name = GENRES.get(genre_id, "Неизввестный жанр")
        poster_url = f"https://image.tmdb.org/t/p/w500{film.get('poster_path', '')}"
        caption = make_movie_caption(film, genre_name)

        # text = (
        #     f"🎬 <b>{title}</b>\n"
        #     f"📅 Год: {date[:4] if date else '—'}\n"
        #     f"⭐ Рейтинг: {rating}/10\n\n"
        #     f"📖 <i>{overview[:400]}...</i>\n\n"
        #     f"🎭 Жанр: <b>{genre_name}</b>"
        # )

        await callback.message.edit_media(
            InputMediaPhoto(media=poster_url, caption=caption, parse_mode="HTML"),
            reply_markup=movie_keyboard(genre_id, movie_index, total_movies)
        )

    except Exception as e:
        await callback.message.answer(f"❌ Ошибка: {e}")


@router.callback_query(F.data.startswith("prev_movie:"))
async def prev_movie(callback: types.CallbackQuery):
    genre_id, movie_index = map(int, callback.data.split(":")[1:3])
    films = get_movies_by_genre(genre_id)
    total_movies = len(films)

    if movie_index < 0:
        await callback.answer("Это первый фильм!", show_alert=True)
        return

    film = films[movie_index]
    genre_name = GENRES.get(genre_id, "Неизвестный жанр")
    poster_url = f"https://image.tmdb.org/t/p/w500{film.get('poster_path', '')}"
    caption = make_movie_caption(film, genre_name)

    await callback.message.edit_media(
        InputMediaPhoto(media=poster_url, caption=caption, parse_mode="HTML"),
        reply_markup=movie_keyboard(genre_id, movie_index, total_movies)
    )





