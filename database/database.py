import aiosqlite

DB_NAME = "tmdb_bot.db"  # добавил точку перед db — это важно!
# database.py (добавь/замени части)
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        # Таблица пользователей
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Таблица "Смотреть позже"
        await db.execute("""
            CREATE TABLE IF NOT EXISTS watch_later (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                movie_id INTEGER,
                title TEXT,
                poster_url TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
             CREATE UNIQUE INDEX IF NOT EXISTS ux_watch_user_movie
             ON watch_later (user_id, movie_id)
        """)
        await db.commit()
        print("✅ Таблицы инициализированы.")

async def add_user(user_id: int, username: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users(user_id, username) VALUES (?, ?)",
            (user_id, username)
        )
        await db.commit()

async def add_to_watch_later_db(user_id: int, movie_id: int, title: str, poster_url: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO watch_later(user_id, movie_id, title, poster_url) VALUES (?, ?, ?, ?)",
            (user_id, movie_id, title, poster_url)

        )
        await db.commit()

async def get_watch_later_db(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT id, movie_id, title, poster_url FROM watch_later WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            return await cursor.fetchall()


async def remove_from_watch_later_db(user_id: int, movie_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM watch_later WHERE user_id = ? AND movie_id = ?",
                         (user_id, movie_id))
        await db.commit()


