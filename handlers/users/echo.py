from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()

@router.message()
async def bot_echo(message: Message, state: FSMContext):
    if await state.get_state() is not None:
        return
    await message.answer(message.text)
