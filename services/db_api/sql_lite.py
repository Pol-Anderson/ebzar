import aiosqlite

class Database:
    def __init__(self, db_path = "config/main.db"):
        self.db_path = db_path

    async def execute(self, sql, parameters = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()

        # Ma'lumotlar bazasiga ulanish
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(sql, parameters)

            data = None
            if fetchone:
                data = await cursor.fetchone()
            if fetchall:
                data = await cursor.fetchall()

            if commit:
                await db.commit()

            return data

    async def create_tables(self):
        await self.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                first_name TEXT,
                last_name TEXT,
                birth_date TEXT,
                class TEXT,
                phone TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """,
            commit=True,
        )

        await self.execute(
            """
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                first_name TEXT,
                last_name TEXT,
                subject TEXT,
                experience_years INTEGER,
                phone TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """,
            commit=True,
        )

    async def add_student(self, tg_id: int, first_name: str, last_name: str, birth_date: str, student_class: str, phone: str):
        await self.execute(
            """
            INSERT INTO students (tg_id, first_name, last_name, birth_date, class, phone)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (tg_id, first_name, last_name, birth_date, student_class, phone),
            commit=True,
        )

    async def add_teacher(self, tg_id: int, first_name: str, last_name: str, subject: str, experience_years: int, phone: str):
        await self.execute(
            """
            INSERT INTO teachers (tg_id, first_name, last_name, subject, experience_years, phone)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (tg_id, first_name, last_name, subject, experience_years, phone),
            commit=True,
        )
