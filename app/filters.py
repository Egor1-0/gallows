from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message
from app.database.requests import get_row

class Len_message(BaseFilter):
    async def __call__(self, message: Message):
        return len(message.text) == 1
class Is_in_word(BaseFilter):
    async def __call__(self, message: Message):
        word = (await get_row(message.from_user.id)).original_word
        return message.text in word
# @router.message(Game.letter)
# async def get_letter(message: Message, state: FSMContext):
#     if len(message.text.lower()) == 1:
#         await insert_letter(message.from_user.id, message.text)
#         word = (await get_row(message.from_user.id)).original_word
#         if message.text.lower() in word:
#             await update_guess_word(message.from_user.id, message.text.lower(), word)
#             if await is_win(message.from_user.id):
#                 await message.answer(f'Вы угадали!!! слово: {word}. \n Напишите /play чтобы начать игру')
#                 await delete_session(message.from_user.id)
#                 await state.clear()
#             else:
#                 await message.answer(f'Вы угадали букву: {await get_guess_word(message.from_user.id)}. \
#                                     \n Использованные буквы: {await get_used_letters(message.from_user.id)}')
            
#         else:
#             await auto_decriment_lifes(message.from_user.id)
#             if await is_lose(message.from_user.id):
#                 await message.answer(f'Вы проиграли. {gallows[0]} Слово было: {word}. \n Напишите /play чтобы начать игру')
#                 await delete_session(message.from_user.id)
#                 await state.clear()
#             else:
#                 await message.answer(f'{gallows[await get_lifes(message.from_user.id)]} \
#                                     \n Использованные буквы: {await get_used_letters(message.from_user.id)}')

#     else:
#         await message.answer('Вы должны писать по одной букве. \
#                                     \n Использованные буквы: {await get_used_letters(message.from_user.id)}')