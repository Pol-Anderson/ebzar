from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from services.db_api.sql_lite import Database

router = Router()

db = Database()


class RegisterStudent(StatesGroup):
    first_name = State()
    last_name = State()
    birth_date = State()
    student_class = State()
    phone = State()
    confirm = State()


class RegisterTeacher(StatesGroup):
    first_name = State()
    last_name = State()
    subject = State()
    experience_years = State()
    phone = State()
    confirm = State()


def role_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📘 O‘quvchi")],
            [KeyboardButton(text="📗 O‘qituvchi")],
        ],
        resize_keyboard=True,
    )


def confirm_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Tasdiqlash")],
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True,
    )


def cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True,
    )


async def show_student_confirmation(message: Message, state: FSMContext):
    data = await state.get_data()
    text = (
        "Ma’lumotlaringiz:\n"
        f"Ism: {data.get('first_name')}\n"
        f"Familiya: {data.get('last_name')}\n"
        f"Tug‘ilgan sana: {data.get('birth_date')}\n"
        f"Sinf: {data.get('student_class')}\n"
        f"Telefon raqami: {data.get('phone')}"
    )
    await message.answer(text, reply_markup=confirm_keyboard())


async def show_teacher_confirmation(message: Message, state: FSMContext):
    data = await state.get_data()
    text = (
        "Ma’lumotlaringiz:\n"
        f"Ism: {data.get('first_name')}\n"
        f"Familiya: {data.get('last_name')}\n"
        f"Fan: {data.get('subject')}\n"
        f"Ish tajribasi (yil): {data.get('experience_years')}\n"
        f"Telefon raqami: {data.get('phone')}"
    )
    await message.answer(text, reply_markup=confirm_keyboard())

@router.message(CommandStart())
async def bot_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Kim sifatida ro‘yxatdan o‘tasiz?", reply_markup=role_keyboard())


@router.message(F.text == "📘 O‘quvchi")
async def choose_student(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(RegisterStudent.first_name)
    await message.answer("Ismni kiriting:", reply_markup=cancel_keyboard())


@router.message(F.text == "📗 O‘qituvchi")
async def choose_teacher(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(RegisterTeacher.first_name)
    await message.answer("Ismni kiriting:", reply_markup=cancel_keyboard())


@router.message(F.text == "❌ Bekor qilish")
async def cancel_any(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bekor qilindi. Qaytadan tanlang:", reply_markup=role_keyboard())


@router.message(RegisterStudent.first_name)
async def student_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(RegisterStudent.last_name)
    await message.answer("Familiyani kiriting:", reply_markup=cancel_keyboard())


@router.message(RegisterStudent.last_name)
async def student_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(RegisterStudent.birth_date)
    await message.answer("Tug‘ilgan sanani kiriting:", reply_markup=cancel_keyboard())


@router.message(RegisterStudent.birth_date)
async def student_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await state.set_state(RegisterStudent.student_class)
    await message.answer("Sinfni kiriting:", reply_markup=cancel_keyboard())


@router.message(RegisterStudent.student_class)
async def student_class(message: Message, state: FSMContext):
    await state.update_data(student_class=message.text)
    await state.set_state(RegisterStudent.phone)
    await message.answer("Telefon raqamini kiriting:", reply_markup=cancel_keyboard())


@router.message(RegisterStudent.phone)
async def student_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(RegisterStudent.confirm)
    await show_student_confirmation(message, state)


@router.message(RegisterStudent.confirm, F.text == "✅ Tasdiqlash")
async def student_confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    await db.add_student(
        tg_id=message.from_user.id,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        birth_date=data.get("birth_date"),
        student_class=data.get("student_class"),
        phone=data.get("phone"),
    )
    await state.clear()
    await message.answer("Saqlandi.", reply_markup=role_keyboard())


@router.message(RegisterStudent.confirm)
async def student_confirm_fallback(message: Message, state: FSMContext):
    await show_student_confirmation(message, state)


@router.message(RegisterTeacher.first_name)
async def teacher_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(RegisterTeacher.last_name)
    await message.answer("Familiyani kiriting:", reply_markup=cancel_keyboard())


@router.message(RegisterTeacher.last_name)
async def teacher_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(RegisterTeacher.subject)
    await message.answer("Fanni kiriting:", reply_markup=cancel_keyboard())


@router.message(RegisterTeacher.subject)
async def teacher_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(RegisterTeacher.experience_years)
    await message.answer("Ish tajribasini (yil) kiriting:", reply_markup=cancel_keyboard())


@router.message(RegisterTeacher.experience_years)
async def teacher_experience(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    if not text.isdigit():
        await message.answer("Ish tajribasini faqat raqamda kiriting:", reply_markup=cancel_keyboard())
        return

    await state.update_data(experience_years=int(text))
    await state.set_state(RegisterTeacher.phone)
    await message.answer("Telefon raqamini kiriting:", reply_markup=cancel_keyboard())


@router.message(RegisterTeacher.phone)
async def teacher_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(RegisterTeacher.confirm)
    await show_teacher_confirmation(message, state)


@router.message(RegisterTeacher.confirm, F.text == "✅ Tasdiqlash")
async def teacher_confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    await db.add_teacher(
        tg_id=message.from_user.id,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        subject=data.get("subject"),
        experience_years=data.get("experience_years"),
        phone=data.get("phone"),
    )
    await state.clear()
    await message.answer("Saqlandi.", reply_markup=role_keyboard())


@router.message(RegisterTeacher.confirm)
async def teacher_confirm_fallback(message: Message, state: FSMContext):
    await show_teacher_confirmation(message, state)
