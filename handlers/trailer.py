from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aiohttp
import os

router = Router()

# ⚙️ Подставь свой ключ TMDB API
TMDB_API_KEY = os.getenv("TMDB_TOKEN") or "02f5fe68da344efd648bf9ea853e50b9"


# 🔹 Обработка кнопки "🎞 Трейлер"
@router.callback_query(F.data.startswith("trailer_"))
async def show_trailer(callback: types.CallbackQuery):
    parts = callback.data.split(":")
    base = parts[0] # trailer_<id или trailer_<genre>
    extra = parts[1] if len(parts) > 1 else None

    try:
        movie_id = base.split("_")[1] # всегда после trailer_
    except IndexError:
        await callback.answer("Ошибка данных", show_alert=True)
        return

    # 🔍 Запрос к TMDB API для получения видео
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=ru-RU"
        ) as resp:
            data = await resp.json()

    # 🔹 Фильтруем видео, чтобы найти YouTube-трейлер
    trailer_url = None
    for video in data.get("results", []):
        if video["site"] == "YouTube" and video["type"] in ("Trailer", "Teaser"):
            trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
            break

    # 🔹 Клавиатура
    builder = InlineKeyboardBuilder()

    if trailer_url:
        builder.row(
            types.InlineKeyboardButton(text="▶️ Смотреть на YouTube", url=trailer_url)
        )
        caption = f"🎞 <b>Трейлер фильма</b>\n\nСмотри на YouTube 👇"
    else:
        caption = "🚫 Трейлер не найден 😢"

    # Назад
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="back_to_watchlist" if "trailer_" in callback.data and len(
                data) < 3 else f"back_to_genre:{data[1]}"
        )
    )

    await callback.message.edit_caption(
        caption=caption,
        reply_markup=builder.as_markup()
    )

    await callback.answer()
