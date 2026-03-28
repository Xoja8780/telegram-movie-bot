# обработка кнопки "Смотреть позже"
from aiogram.filters import Command

from aiogram import F, types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.tmdb_api import get_movies_by_genre

from database.database import (
    add_to_watch_later_db,
    get_watch_later_db,
    remove_from_watch_later_db
)
from keyboards.watchlist_kb import (
    watchlist_main_kb,
    watchlist_poster_kb,
    confirm_clear_watchlist_kb
)

router = Router()


# ==============================
# 🔹 Добавление фильма в список
# ==============================


@router.callback_query(F.data.startswith("watch_later:"))
async def add_to_watch_later(callback: types.CallbackQuery):
    genre_id, movie_index = map(int, callback.data.split(":")[1:3])
    user_id = callback.from_user.id

    films = get_movies_by_genre(genre_id)
    if not films or movie_index >= len(films):
        await callback.answer("😕 Фильм не найден.", show_alert=True)
        return

    film = films[movie_index]
    movie_id = film.get("id")
    title = film.get("title", "Без названия")
    poster_path = film.get("poster_path")
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

    await add_to_watch_later_db(user_id, movie_id, title, poster_url)

    await callback.answer(f"🎬 '{title}' добавлен(а) в «Смотреть позже»", show_alert=True)


@router.message(Command("watch_later"))
@router.message(F.text == "📺 Смотреть позже")
async def show_watch_later_cmd(message: types.Message):
    """Открывает главное меню 'Смотреть позже'"""
    user_id = message.from_user.id
    rows = await get_watch_later_db(user_id)

    if not rows:
        await message.answer("📭 У вас пока нет фильмов в списке 'Смотреть позже'.")
        return

    # Список фильмов без постеров (только названия)
    movie_list = "\n".join([f"• {r[2]}" for r in rows])
    text = f"🎬 <b>Ваш список фильмов:</b>\n\n{movie_list}\n\n👇 Выберите действие:"
    await message.answer(text, parse_mode="HTML", reply_markup=watchlist_main_kb())


# ===================================================
# 🔹 Показ фильмов с постерами (по одному, листание)
# ===================================================
@router.callback_query(F.data == "show_posters")
async def show_posters(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    rows = await get_watch_later_db(user_id)

    if not rows:
        await callback.answer("📭 У вас пока нет фильмов в списке 'Смотреть позже'.", show_alert=True)
        return

    # Сохраняем позицию пользователя
    current_index = 0
    movie = rows[current_index]
    await send_movie_card(callback.message, movie, current_index, len(rows))


async def send_movie_card(message, movie, index, total):
    db_id, movie_id, title, poster_url = movie
    caption = f"🎬 <b>{title}</b>\n\n📍 Фильм {index + 1}/{total}"
    await message.edit_media(
        media=types.InputMediaPhoto(
            media=poster_url,
            caption=caption,
            parse_mode="HTML"
        ),
        reply_markup=watchlist_poster_kb(movie_id)
    )

    # ===========================================
    # 🔹 Листание (след / предыдущий фильм)
    # ===========================================
    @router.callback_query(F.data.startswith(("next_", "prev_")))
    async def navigate_watchlist(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        rows = await get_watch_later_db(user_id)

        if not rows:
            await callback.answer("📭 У вас пока нет фильмов в списке 'Смотреть позже'.", show_alert=True)
            return

        movie_id = int(callback.data.split("_")[1])
        current_index = next((i for i, r in enumerate(rows) if r[1] == movie_id), 0)
        if "next_" in callback.data:
            current_index = (current_index + 1) % len(rows)
        else:
            current_index = (current_index - 1) % len(rows)

        movie = rows[current_index]
        await send_movie_card(callback.message, movie, current_index, len(rows))

    @router.callback_query(F.data.startswith("delete_"))
    async def delete_movie(callback: types.CallbackQuery):
        movie_id = int(callback.data.split("_")[1])
        user_id = callback.from_user.id

        await remove_from_watch_later_db(user_id, movie_id)
        await callback.answer("✅ Удалено из 'Смотреть позже'.", show_alert=True)

        try:
            await callback.message.delete()
        except:
            pass

    # ===========================================
    # 🔹 Очистка всего списка
    # ===========================================
    @router.callback_query(F.data == "clear_watchlist")
    async def confirm_clear(callback: types.CallbackQuery):
        await callback.message.answer("⚠️ Вы уверены, что хотите очистить весь список 'Смотреть позже'?",
                                      reply_markup=confirm_clear_watchlist_kb())

    @router.callback_query(F.data == "confirm_clear")
    async def clear_watchlist(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        rows = await get_watch_later_db(user_id)

        if not rows:
            await callback.answer("📭 Ваш список уже пуст.", show_alert=True)
            return

        # Удаляем всё по одному (чтобы не писать отдельную функцию в БД)
        for r in rows:
            await remove_from_watch_later_db(user_id, r[1])

        await callback.message.answer("✅ Список успешно очищен.")
        await callback.message.delete()

    @router.callback_query(F.data == "cancel_clear")
    async def cancel_clear(callback: types.CallbackQuery):
        await callback.message.answer("❌ Очистка отменена.")
        await callback.message.delete()

    @router.callback_query(F.data == "back_to_watchlist")
    async def back_to_watchlist(callback: types.CallbackQuery):
        await callback.answer()
        user_id = callback.from_user.id

        rows = await get_watch_later_db(user_id)

        if not rows:
            await callback.message.edit_text("📭 У вас пока нет фильмов в списке 'Смотреть позже'.")
            return

        # удаляем старое сообщение (если было)
        try:
            await callback.message.delete()
        except:
            pass

        movie_list = "\n".join([f"• {r[2]}" for r in rows])
        text = f"🎬 <b>Ваш список фильмов:</b>\n\n{movie_list}\n\n👇 Выберите действие:"
        await callback.message.answer(
            text,
            parse_mode="HTML",
            reply_markup=watchlist_main_kb()
        )


