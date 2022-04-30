import pandas as pd
from information import get_information
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from information import get_random_places

bot = Bot(token="5371672546:AAHX2cVPhqXQ-R5q4SAxOMsVMknNhblnXjQ")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
activity =0


@dp.message_handler(commands="start")
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["кинотеатр", "театр"]
    buttons1 = ["музей", "галерея"]
    buttons2 = ["кафе/ресторан", "библиотека"]
    keyboard.add(*buttons)
    keyboard.add(*buttons1)
    keyboard.add(*buttons2)
    await message.answer("Выберите вариант времяпрепровождения", reply_markup=keyboard)

@dp.message_handler(Text(equals="1"))
async def get_information(message):
    await message.answer(activity)

@dp.message_handler(Text(equals="2"))
async def make_random(message):
    keyboard =types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["1 вариант", "5 вариантов", "10 вариантов"]
    keyboard.add(*buttons)
    await message.answer("Выберите, сколько вариантов хотите получить", reply_markup=keyboard)

@dp.message_handler(Text(equals="5 вариантов"))
async def get_5(message):
    museums = pd.read_json('data/museums.json')
    answer1 = get_random_places(museums, 5)
    for i in range(5):
        await message.answer('\n'.join(answer1[i]))

@dp.message_handler()
async def choose(message):
    global activity
    if message.text == "кинотеатр":
        activity = 1
    elif message.text == "театр":
        activity = 2
    elif message.text == "музей":
        activity = 3
    elif message.text == "галерея":
        activity = 4
    elif message.text == "кафе/ресторан":
        activity = 5
    elif message.text == "библиотека":
        activity = 6
    await message.reply("Отличный выбор!")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["1", "2", "3", "4"]
    keyboard.add(*buttons)
    await message.answer(
        "Если хотите узнать общую информацию про конкретное место, нажмите 1\n"
        "Если хотите получить случайно выбранную ботом подборку, нажмите 2\n"
        "Если хотите указать желаемый район и получить подборку, нажмите 3\n"
        "Если хотите указать пожелания по расстоянию до центра Москвы и получить подборку, нажмите 4\n", reply_markup=keyboard)


# @dp.message_handler(Text(equals="Кинотеатр"))
# async def with_puree(message: types.Message):
#     await message.reply("Отличный выбор!")


# @dp.message_handler(lambda message: message.text == "Без пюрешки")
# async def without_puree(message: types.Message):
#     await message.reply("Так невкусно!")


if name == "main":
    executor.start_polling(dp, skip_updates=True)
#
# museums = pd.read_json('data/museums.json')
# print('\n'.join(get_information(5, museums)))