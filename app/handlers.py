import random
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup 
from app.database.push import set_word, update_guess_word, auto_decriment_lifes, insert_letter
from app.database.requests import get_row, get_guess_word, is_win, is_lose, get_lifes, get_used_letters
from app.database.delete import delete_session

file = open('words/words.txt')
words_list = []
for line in file:
    words_list.extend(line.split())
file.close()

gallows = ['\n    &&&&&&&&&&&&&&&& \n    &              | \n    &              | \n    &              | \n    &              O \n    &            / | \\ \n    &             / \\ \n    & \n    & \n    & \n&&&&&&&&&', 
           '\n    &&&&&&&&&&&&&&&& \n    &              | \n    &              | \n    &              | \n    &              O \n    &            / | \\ \n    &             \n    & \n    & \n    & \n&&&&&&&&&', 
           '\n    &&&&&&&&&&&&&&&& \n    &              | \n    &              | \n    &              | \n    &              O \n    &              | \n    &             \n    & \n    & \n    & \n&&&&&&&&&', 
           '\n    &&&&&&&&&&&&&&&& \n    &              | \n    &              | \n    &              | \n    &               \n    &              \n    &             \n    & \n    & \n    & \n&&&&&&&&&', 
           '\n    &&&&&&&&&&&&&&&& \n    &              \n    &              \n    &              \n    &               \n    &              \n    &             \n    & \n    & \n    & \n&&&&&&&&&', 
           '\n& \n& \n& \n& \n& \n& \n& \n& \n& \n& \n&&&&&&&&&', 
           '\n& \n& \n& \n& \n& \n& \n& \n& \n& \n& \n&']

router = Router()

class Game(StatesGroup):
    letter = State()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет, это игра "Виселица". Воспользуйтесь командой "/help" для получения большей информации')

@router.message(Command('help'))
async def help(message: Message):
    await message.answer("""Это игра Виселица. Суть игры: я загадываю слово, состоящее из 4 - 7 букв. ваша цель его отгадать. Вы случайно называете 
                         одну букву за один ход. если вы угадали, я открываю все эти буквы в этом слове. если вы не угадали, 
                         к виселице дорисовывается деталь. вы проиграли, когда получится такой рисунок: 
                         \n    &&&&&&&&&&&&&&&& \n    &              | \n    &              | \n    &              | \n    &              O \n    &            / | \\ \n    &             / \\ \n    & \n    & \n    & \n&&&&&&&&&
                         \n Вам доступны команды: \n "/play" - начать игру \n "/help" - получение информации""")
    

@router.message(Command('play'))
async def play(message: Message, state: FSMContext):
    await state.set_state(Game.letter)
    if await get_row(message.from_user.id):
        await message.answer("Слово уже загадано. Можете начинать писать буквы")
    else:
        await set_word(message.from_user.id, words_list[random.randint(0, len(words_list) - 1)])
        await message.answer("Слово загадано. Можете начинать писать буквы")

@router.message(Game.letter)
async def get_letter(message: Message, state: FSMContext):
    if len(message.text.lower()) == 1:
        await insert_letter(message.from_user.id, message.text)
        word = (await get_row(message.from_user.id)).original_word
        if message.text.lower() in word:
            await update_guess_word(message.from_user.id, message.text.lower(), word)
            if await is_win(message.from_user.id):
                await message.answer(f'Вы угадали!!! слово: {word}. \n Напишите /play чтобы начать игру')
                await delete_session(message.from_user.id)
                await state.clear()
            else:
                await message.answer(f'Вы угадали букву: {await get_guess_word(message.from_user.id)}. \
                                    \n Использованные буквы: {await get_used_letters(message.from_user.id)}')
            
        else:
            await auto_decriment_lifes(message.from_user.id)
            if await is_lose(message.from_user.id):
                await message.answer(f'Вы проиграли. {gallows[0]} Слово было: {word}. \n Напишите /play чтобы начать игру')
                await delete_session(message.from_user.id)
                await state.clear()
            else:
                await message.answer(f'{gallows[await get_lifes(message.from_user.id)]} \
                                    \n Использованные буквы: {await get_used_letters(message.from_user.id)}')

    else:
        await message.answer('Вы должны писать по одной букве. \
                                    \n Использованные буквы: {await get_used_letters(message.from_user.id)}')


"""
\n    &&&&&&&&&&&&&&&& 
\n    &              | 
\n    &              | 
\n    &              | 
\n    &              O 
\n    &            / | \\ 
\n    &             / \\ 
\n    & 
\n    & 
\n    & 
\n&&&&&&&&&

\n    &&&&&&&&&&&&&&&& 
\n    &              | 
\n    &              | 
\n    &              | 
\n    &              O 
\n    &            / | \\ 
\n    &             
\n    & 
\n    & 
\n    & 
\n&&&&&&&&&

\n    &&&&&&&&&&&&&&&& 
\n    &              | 
\n    &              | 
\n    &              | 
\n    &              O 
\n    &              | 
\n    &             
\n    & 
\n    & 
\n    & 
\n&&&&&&&&&

\n    &&&&&&&&&&&&&&&& 
\n    &              | 
\n    &              | 
\n    &              | 
\n    &               
\n    &              
\n    &             
\n    & 
\n    & 
\n    & 
\n&&&&&&&&&

\n    &&&&&&&&&&&&&&&& 
\n    &              
\n    &              
\n    &              
\n    &               
\n    &              
\n    &             
\n    & 
\n    & 
\n    & 
\n&&&&&&&&&

\n    &
\n    &               
\n    &              
\n    &               
\n    &               
\n    &              
\n    &             
\n    & 
\n    & 
\n    & 
\n&&&&&&&&&

\n    &
\n    &               
\n    &              
\n    &               
\n    &               
\n    &              
\n    &             
\n    & 
\n    & 
\n    & 
\n    &

\n    

"""