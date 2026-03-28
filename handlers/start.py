# /start, приветствие, кнопки категорий
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards.genre_keyboard import genre_keyboard
from database.database import add_user

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name
    await add_user(user_id, username)

    welcome_text = (
        "👋 Привет! Я твой кино-бот 🎬\n\n"
        "Я помогу тебе искать фильмы по жанрам и сохранять их в 'Смотреть позже'.\n"
        "Выбирай жанр или управляй через команды:\n\n"
        "• /genres — показать жанры\n"
        "• /watch_later — список отложенных фильмов\n"
        "• /help — помощь"
    )
    await message.answer(
        text=welcome_text,
        reply_markup=genre_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    from keyboards.movie_keyboard import main_reply_keyboard
    help_text = (
        "🆘 <b>Помощь по командам</b>\n\n"
        "🎬 /start — запустить бота\n"
        "🎭 /genres — выбрать жанр фильма\n"
        "⭐ /watch_later — показать список 'Смотреть позже'\n"
        "ℹ️ /about — информация о проекте\n\n"
        "👇 <b>Быстрый доступ:</b>"
    )
    await message.answer(help_text, parse_mode="HTML", reply_markup=main_reply_keyboard())


@router.message(Command("about"))
async def about_cmd(message: types.Message):
    text = (
        "🎬 <b>MovieBot</b> — бот, созданный для удобного поиска фильмов по жанрам.\n"
        "Ты можешь листать фильмы, добавлять их в список 'Смотреть позже' и открывать снова когда захочешь.\n\n"
        "👨‍💻 Разработчик: <b>Xoja Dev</b>\n"
        "📚 Написан на <b>Python + Aiogram 3</b>\n"
        "💡 Идея: улучшить киновечера и практиковаться в кодинге 😎"
    )
    await message.answer(text=text, parse_mode="HTML")


@router.message(Command("genres"))
async def show_genres_cmd(message: types.Message):
    from keyboards.genre_keyboard import genre_keyboard
    await message.answer("🎬 Выбери жанр фильма:", reply_markup=genre_keyboard())


@router.message(F.text == "🎭 Жанры")
async def show_genres(message: types.Message):
    from keyboards.genre_keyboard import genre_keyboard
    await message.answer("🎬 Выбери жанр фильма:", reply_markup=genre_keyboard())
