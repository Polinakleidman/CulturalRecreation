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
activity = 0
find_by_name = False
find_by_distict = False
find_by_distance_to_centre = False
curr_district = ""
from_centre =0


async def get_n(message, n):
    places = pd.read_json(f'data/{activities[activity - 1]}.json')
    if (not find_by_distict) and (not find_by_distance_to_centre):
        answer1 = get_random_places(places, n)
    elif find_by_distict:
        global curr_district
        answer1 = []
        #answer1 = get_random_in_district(curr_district, n)
    else:
        global from_centre
        answer1 = []
        #answer1 = get_random_in_area(from_centre, n)
    for i in range(n):
        await message.answer('\n'.join(answer1[i]))
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/start"]
    keyboard.add(*buttons)
    await message.answer("Для выбора нового места нажмите кнопку start", reply_markup=keyboard)


def create_number_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["1 вариант", "5 вариантов", "10 вариантов"]
    keyboard.add(*buttons)
    return keyboard

def make_dist_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["5 км", "10 км", "15 км"]
    keyboard.add(*buttons)
    return keyboard


def make_disrict_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Восточный", "Западный"]
    buttons1 = ["Зеленоградский", "Северо-Восточный"]
    buttons2 = ["Центральный", "Юго-Восточный"]
    buttons3 = ["Юго-Западный", "Южный"]
    keyboard.add(*buttons)
    keyboard.add(*buttons1)
    keyboard.add(*buttons2)
    keyboard.add(*buttons3)
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
    buttons = ["back to menu"]
    keyboard.add(*buttons)
    await message.answer("Введите название места без кавычек через пробел", reply_markup=keyboard)


@dp.message_handler(Text(equals="2"))
async def make_random(message):
    keyboard = create_number_keyboard()
    await message.answer("Выберите, сколько вариантов хотите получить", reply_markup=keyboard)


@dp.message_handler(Text(equals="3"))
async def get_in_district(message):
    global find_by_name, find_by_distict, find_by_distance_to_centre
    find_by_distict = True
    find_by_distance_to_centre = False
    find_by_name = False
    keyboard = make_disrict_keyboard()
    await message.answer("Укажите желаемый округ", reply_markup=keyboard)
    pass

@dp.message_handler(Text(equals="4"))
async  def get_by_distance_to_centre(message):
    global find_by_name, find_by_distict, find_by_distance_to_centre
    find_by_distict = False
    find_by_distance_to_centre = True
    find_by_name = False
    keyboard = make_dist_keyboard()
    await message.answer("Укажите желаемый округ", reply_markup=keyboard)


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
    elif message.text == "back to menu":
        await start(message)
        return
    elif find_by_name:
        place = pd.read_json(f'data/{activities[activity - 1]}.json')
        answer1 = get_information_about_certain_place(place, message.text)
        for i in range(len(answer1)):
            await message.answer('\n'.join(answer1[i]))
        await start(message)
        return
    elif find_by_distict:
        global curr_district
        curr_district = message.text
        keyboard = create_number_keyboard()
        await message.answer("Выберите, сколько вариантов хотите получить", reply_markup=keyboard)
        return
    elif find_by_distance_to_centre:
        global from_centre
        from_centre = int(message.text[:-3])
        keyboard = create_number_keyboard()
        await message.answer("Выберите, сколько вариантов хотите получить", reply_markup=keyboard)
    await message.reply("Отличный выбор!")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["1", "2", "3", "4"]
    keyboard.add(*buttons)
    await message.answer(
        "Если хотите узнать общую информацию про конкретное место, нажмите 1\n"
        "Если хотите получить случайно выбранную ботом подборку, нажмите 2\n"
        "Если хотите указать желаемый округ и получить подборку, нажмите 3\n"
        "Если хотите указать пожелания по расстоянию до центра Москвы и получить подборку, нажмите 4\n",
        reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
#
# museums = pd.read_json('data/museums.json')
# print('\n'.join(get_information(5, museums)))
