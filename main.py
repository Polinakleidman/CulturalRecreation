import pandas as pd
from information import get_information
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from information import get_random_places, get_information_about_certain_place
activities = ['cinemas', 'theaters', 'museums', 'galaies', 'food', 'libraries']
bot = Bot(token="5371672546:AAHX2cVPhqXQ-R5q4SAxOMsVMknNhblnXjQ")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
activity =0
find_by_name = False
find_by_distict = False
find_by_distance_to_centre = False



async def get_n(message, n):
    places = pd.read_json(f'data/{activities[activity - 1]}.json')
    answer1 = get_random_places(places, n)
    print(answer1)
    for i in range(n):
        await message.answer('\n'.join(answer1[i]))

def create_number_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["1 вариант", "5 вариантов", "10 вариантов"]
    keyboard.add(*buttons)
    return keyboard

@dp.message_handler(commands="start")
async def start(message: types.Message):
    global activity, find_by_name, find_by_distance_to_centre, find_by_distict
    activity = 0
    find_by_name = False
    find_by_distict = False
    find_by_distance_to_centre = False
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
    global find_by_name, find_by_distict, find_by_distance_to_centre
    find_by_distict = False
    find_by_distance_to_centre = False
    find_by_name = True
    find_by_name = True
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/start"]
    keyboard.add(*buttons)
    await message.answer("Введите название места без кавычек через пробел", reply_markup=keyboard)

@dp.message_handler(Text(equals="2"))
async def make_random(message):
    keyboard =create_number_keyboard()
    await message.answer("Выберите, сколько вариантов хотите получить", reply_markup=keyboard)

@dp.message_handler(Text(equals="3"))
async def get_in_district(message):
    find_by_distict = True
    pass

@dp.message_handler(Text(equals="5 вариантов"))
async def get_5(message):
    await get_n(message, 5)

@dp.message_handler(Text(equals="1 вариант"))
async def get_1(message):
    await get_n(message, 1)

@dp.message_handler(Text(equals="10 вариантов"))
async def get_10(message):
    await get_n(message, 10)

@dp.message_handler()
async def choose(message):
    global find_by_name
    global find_by_distict
    global find_by_distance_to_centre
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
    elif find_by_name:
        museums = pd.read_json(f'data/{activities[activity - 1]}.json')
        answer1 = get_information_about_certain_place(museums, message.text)

        await message.answer('\n'.join(answer1[0]))
        await start(message)
        return
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


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
#
# museums = pd.read_json('data/museums.json')
# print('\n'.join(get_information(5, museums)))