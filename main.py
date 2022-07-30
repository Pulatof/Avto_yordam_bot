import aiogram
from aiogram import Bot, Dispatcher, executor
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters import Text, BoundFilter, Command
from config import bot_token
import io
import asyncio
import datetime
import re
from aiogram.utils.exceptions import BadRequest
import sqlite3

from distance import distance
from sqlite import *

db = Database()

from buttons import *

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    user_id = message.from_user.id
    try:
        # db.create_table_users()
        user = db.select_user(user_id=user_id)
        if not user:
            try:
                db.add_user(user_id=message.from_user.id,
                            user_name=message.from_user.username,
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name)
            except sqlite3.IntegrityError:
                pass
            await message.answer("Iltimos, tilni tanlang. Пожалуйста, выберите язык.", reply_markup=select_lang)
        else:
            if user[6] == "uz":
                await message.answer("Avto yordam botiga hush kelibsiz", reply_markup=main_menu_uz)
            else:
                await message.answer("Добро пожаловать на avtoy_yordam бот", reply_markup=main_menu_ru)
    except:
        pass

@dp.message_handler(Text(equals=["Tilni o`zgartirish 🇺🇿/🇷🇺", "Изменения языка 🇺🇿/🇷🇺"]))
async def lang(message: Message):
    await message.answer("Tilni tanlang / Измените язык", reply_markup=select_lang)


@dp.message_handler(Text(equals="O'zbek tili 🇺🇿"))
async def lang(message: Message):
    user_id = message.from_user.id
    try:
        db.update_user_lang("uz", user_id)
    except:
        pass
    await message.answer("Avto yordam botiga hush kelibsiz", reply_markup=main_menu_uz)


@dp.message_handler(Text(equals="Rus tili 🇷🇺"))
async def lang(message: Message):
    user_id = message.from_user.id
    try:
        db.update_user_lang("ru", user_id)
    except:
        pass
    await message.answer("Добро пожаловать на avtoy_yordam бот", reply_markup=main_menu_ru)


@dp.message_handler(Text(equals=["Avtosalonlar 🚗", "Автосалоны 🚗"]))
async def avtosalonlar(message: Message):
    try:

        db.update_user_state("Avtosalonlar", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)
        if user_state[1] == "uz":
            avtosalonlar = db.select_all_avtosalon("uz")
            avtosalonlar_keyboard = []
            avtosalonlar_keyboard.append([KeyboardButton(text="Asosiy menu 🏠")])
            for avtosalon in avtosalonlar:
                avtosalonlar_keyboard.append([KeyboardButton(text=avtosalon[0])])
            avtosalonlar_keyboard.append([KeyboardButton(text="Asosiy menu 🏠")])

            avtosalonlar_uz = ReplyKeyboardMarkup(
                keyboard=avtosalonlar_keyboard, resize_keyboard=True
            )
            await message.answer("Ushbu bo'limda siz UZAM avtomobillari, chet elda ishlab chiqarilgan avtomobillari, "
                                 "elektr motorli avtotransportlar, yuk avtomobillari va boshqa turli xildagi texnika vositalari "
                                 "bilan shugullanuvchi avtosalonlar bilan tanishishingiz mumkin",
                                 reply_markup=avtosalonlar_uz)
        else:
            avtosalonlar = db.select_all_avtosalon("ru")
            avtosalonlar_keyboard = []
            avtosalonlar_keyboard.append([KeyboardButton(text="Главный меню 🏠")])
            for avtosalon in avtosalonlar:
                avtosalonlar_keyboard.append([KeyboardButton(text=avtosalon[0])])
            avtosalonlar_keyboard.append([KeyboardButton(text="Главный меню 🏠")])

            avtosalonlar_ru = ReplyKeyboardMarkup(
                keyboard=avtosalonlar_keyboard, resize_keyboard=True
            )
            await message.answer(
                "В этом разделе вы можете ознакомиться с автосалонами  УЗАМ, автомобилями зарубежного производства,  электромобилями, грузовыми автомобилями и другими видами транспортных средств.",
                reply_markup=avtosalonlar_ru)

    except:
        pass


@dp.message_handler(Text(equals="Asosiy menu 🏠"))
async def main_menu(message: Message):
    await message.answer("Asosiy menu", reply_markup=main_menu_uz)


@dp.message_handler(Text(equals="Главный меню 🏠"))
async def main_menu(message: Message):
    await message.answer("Главный меню", reply_markup=main_menu_ru)


@dp.message_handler(Text(equals="Ortga 🔙"))
async def main_menu(message: Message):
    try:
        db.update_user_state("gaihudud", message.from_user.id)
        hududs = db.select_all_hudud("uz")
        hududs_keyboard = []
        hududs_keyboard.append([KeyboardButton(text="Asosiy menu 🏠")])
        for hudud in hududs:
            hududs_keyboard.append([KeyboardButton(text=hudud[0])])
        hududs_keyboard.append([KeyboardButton(text="Asosiy menu 🏠")])

        hududs_uz = ReplyKeyboardMarkup(
            keyboard=hududs_keyboard, resize_keyboard=True
        )
        await message.answer("Ushbu bo'limda YHXB manzillari bilan tanishishingiz mumkin",
                             reply_markup=hududs_uz)
    except:
        pass


@dp.message_handler(Text(equals="Назад 🔙"))
async def main_menu(message: Message):
    try:
        db.update_user_state("gaihudud", message.from_user.id)
        hududs = db.select_all_hudud("ru")
        hududs_keyboard = []
        hududs_keyboard.append([KeyboardButton(text="Главный меню 🏠")])
        for hudud in hududs:
            hududs_keyboard.append([KeyboardButton(text=hudud[0])])
        hududs_keyboard.append([KeyboardButton(text="Главный меню 🏠")])

        hududs_ru = ReplyKeyboardMarkup(
            keyboard=hududs_keyboard, resize_keyboard=True
        )
        await message.answer("В этом разделе вы сможете ознакомиться с адресами отделени ГИБДД",
                             reply_markup=hududs_ru)
    except:
        pass


@dp.message_handler(Text(equals=["Texnik ko`riklar 📝", "Автотехосмотр 📝"]))
async def texosmotrlar(message: Message):
    try:
        db.update_user_state("Texnik_korik", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)

        if user_state[1] == "uz":
            texosmotrlar = db.select_all_texosmotr("uz")
            texosmotrlar_keyboard = []
            texosmotrlar_keyboard.append([KeyboardButton(text="Asosiy menu 🏠")])
            for texosmotr in texosmotrlar:
                texosmotrlar_keyboard.append([KeyboardButton(text=texosmotr[0])])
            texosmotrlar_keyboard.append([KeyboardButton(text="Asosiy menu 🏠")])

            texosmotrlar_uz = ReplyKeyboardMarkup(
                keyboard=texosmotrlar_keyboard, resize_keyboard=True
            )
            await message.answer("Ushbu bo'limda siz 'Avtotexnik ko'rik'lar manzillari bilan tanishishingiz mumkin",
                                 reply_markup=texosmotrlar_uz)
        else:
            texosmotrlar = db.select_all_texosmotr("ru")
            texosmotrlar_keyboard = []
            texosmotrlar_keyboard.append([KeyboardButton(text="Главный меню 🏠")])
            for texosmotr in texosmotrlar:
                texosmotrlar_keyboard.append([KeyboardButton(text=texosmotr[0])])
            texosmotrlar_keyboard.append([KeyboardButton(text="Главный меню 🏠")])

            texosmotrlar_ru = ReplyKeyboardMarkup(
                keyboard=texosmotrlar_keyboard, resize_keyboard=True
            )
            await message.answer(
                "В этом разделе вы сможете ознакомиться с адресами и контактами отделении технического осмотра вашего автомототранспорта.",
                reply_markup=texosmotrlar_ru)

    except:
        pass


#

@dp.message_handler(Text(equals=["Avtosugurta", "Автострохования"]))
async def avtostaxovaniya(message: Message):
    try:
        db.update_user_state("Avtosugurta", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)

        if user_state[1] == "uz":
            avtostaxovaniya = db.select_all_straxovka("uz")
            avtostaxovaniya_keyboard = []
            avtostaxovaniya_keyboard.append([KeyboardButton(text="Asosiy menu 🏠")])
            for avtostrax in avtostaxovaniya:
                avtostaxovaniya_keyboard.append([KeyboardButton(text=avtostrax[0])])
            avtostaxovaniya_keyboard.append([KeyboardButton(text="Asosiy menu 🏠")])

            avtostaxovaniya_uz = ReplyKeyboardMarkup(
                keyboard=avtostaxovaniya_keyboard, resize_keyboard=True
            )
            await message.answer("Ushbu bo'limda siz Avtosugurta kompaniyalari manzillari bilan tanishishingiz mumkin",
                                 reply_markup=avtostaxovaniya_uz)
        else:
            avtostaxovaniya = db.select_all_straxovka("ru")
            avtostaxovaniya_keyboard = []
            avtostaxovaniya_keyboard.append([KeyboardButton(text="Главный меню 🏠")])
            for avtostrax in avtostaxovaniya:
                avtostaxovaniya_keyboard.append([KeyboardButton(text=avtostrax[0])])
            avtostaxovaniya_keyboard.append([KeyboardButton(text="Главный меню 🏠")])

            avtostaxovaniya_ru = ReplyKeyboardMarkup(
                keyboard=avtostaxovaniya_keyboard, resize_keyboard=True
            )
            await message.answer(
                "В этом разделе вы сможете ознакомиться с адресами и контактами Автостраховой компании.",
                reply_markup=avtostaxovaniya_ru)

    except:
        pass


#
@dp.message_handler(Text(equals=["Evakuator", "Эвакуатор"]))
async def evokuatsiya(message: Message):
    try:
        db.update_user_state("Evokuator", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)

        if user_state[1] == "uz":
            evokuatsiya = db.select_all_evakuatr("uz")
            evokuatsiya_keyboard = []
            evokuatsiya_keyboard.append([KeyboardButton(text="Asosiy menu 🏠")])
            for evokuat in evokuatsiya:
                evokuatsiya_keyboard.append([KeyboardButton(text=evokuat[0])])
            evokuatsiya_keyboard.append([KeyboardButton(text="Asosiy menu 🏠")])

            evokuatsiya_uz = ReplyKeyboardMarkup(
                keyboard=evokuatsiya_keyboard, resize_keyboard=True
            )
            await message.answer("Ushbu bo'limda siz Avtosugurta kompaniyalari manzillari bilan tanishishingiz mumkin",
                                 reply_markup=evokuatsiya_uz)
        else:
            evokuatsiya = db.select_all_evakuatr("ru")
            evokuatsiya_keyboard = []
            evokuatsiya_keyboard.append([KeyboardButton(text="Главный меню 🏠")])
            for evokuat in evokuatsiya:
                evokuatsiya_keyboard.append([KeyboardButton(text=evokuat[0])])
            evokuatsiya_keyboard.append([KeyboardButton(text="Главный меню 🏠")])

            evokuatsiya_ru = ReplyKeyboardMarkup(
                keyboard=evokuatsiya_keyboard, resize_keyboard=True
            )
            await message.answer(
                "В этом разделе вы сможете ознакомиться с адресами и контактами Автостраховой компании.",
                reply_markup=evokuatsiya_ru)

    except:
        pass


#
@dp.message_handler(Text(equals=["YHXBB 👮🏻‍♂", "ГУБДД 👮🏻‍♂"]))
async def gaihudud(message: Message):
    try:
        db.update_user_state("gaihudud", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)

        if user_state[1] == "uz":
            hududs = db.select_all_hudud("uz")
            hududs_keyboard = []
            hududs_keyboard.append([KeyboardButton(text="Asosiy menu 🏠")])
            for hudud in hududs:
                hududs_keyboard.append([KeyboardButton(text=hudud[0])])
            hududs_keyboard.append([KeyboardButton(text="Asosiy menu 🏠")])

            hududs_uz = ReplyKeyboardMarkup(
                keyboard=hududs_keyboard, resize_keyboard=True
            )
            await message.answer("Ushbu bo'limda YHXB manzillari bilan tanishishingiz mumkin",
                                 reply_markup=hududs_uz)
        else:
            hududs = db.select_all_hudud("ru")
            hududs_keyboard = []
            hududs_keyboard.append([KeyboardButton(text="Главный меню 🏠")])
            for hudud in hududs:
                hududs_keyboard.append([KeyboardButton(text=hudud[0])])
            hududs_keyboard.append([KeyboardButton(text="Главный меню 🏠")])

            hududs_ru = ReplyKeyboardMarkup(
                keyboard=hududs_keyboard, resize_keyboard=True
            )
            await message.answer("В этом разделе вы сможете ознакомиться с адресами отделени ГИБДД",
                                 reply_markup=hududs_ru)

    except:
        pass


@dp.message_handler(Text(equals=["AYOQSH ⛽", "АЗС ⛽", "Ortga ⬅", "Назад ⬅", "Ortga ⬅", "Назад ⬅"]))
async def zapravka(message: Message):
    try:
        db.update_user_state("zapravka", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)
        if user_state[1] == "uz":
            await message.answer(
                "Ushbu bo'limda siz AYOQSHlar manzillarini qidirib topishingiz mumkin. Marhamat kerakli yoqilg'i turini tanlang:",
                reply_markup=zapravka_uz)
        else:
            await message.answer(
                "В этом разделе вы сможете ознакомиться с адресами АЗС. Пожалуйста выберите вид топлива:",
                reply_markup=zapravka_ru)
    except:
        pass
#
@dp.message_handler(Text(equals=["Avtoservislar 🔧", "Автосервисы 🔧"]))
async def avtoservis(message: Message):
    try:
        user_state = db.get_user_state(message.from_user.id)
        if user_state[1] == "uz":
            await message.answer(
                "Ushbu bo'limda siz avtombillarga texnik xizmat ko'rsatish shaxobchalari manzillari bilan tanishishingiz mumkin. Marhamat kerakli bo'limni tanlang:",
                reply_markup=servic_uz)
        else:
            await message.answer(
                "В этом разделе вы сможете ознакомиться с адресами автосервисов. Пожалуйста выберите раздел:",
                reply_markup=servic_ru)
    except:
        pass

@dp.message_handler(
    Text(equals=["Avtomobillarga texnik xizmat ko'rsatish shaxobchalari", "Тех-обслужования автомобилей"]))
async def avtoservisloc(message: Message):
    try:
        db.update_user_state("servis", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)
        if user_state[1] == "uz":
            await message.answer(
                "Avtoservislarni lokatsiya bo'yicha qidirish uchun lokatsiyani yuboring:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Manzilni yuboring", request_location=True)],
                              [KeyboardButton(text="Asosiy menu 🏠")]], resize_keyboard=True))
        else:
            await message.answer(
                "Поиск автосервисов по локацию:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Отправьте локацию", request_location=True)],
                              [KeyboardButton(text="Главный меню 🏠")]], resize_keyboard=True))
    except:
        pass


@dp.message_handler(
    Text(equals=["Tyuning atel'elar", "Тюнинг ателе"]))
async def avtotuningloc(message: Message):
    try:
        db.update_user_state("tuning", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)
        if user_state[1] == "uz":
            await message.answer(
                "Avtotuning va avtoatel'elarni lokatsiya bo'yicha qidirish uchun lokatsiyani yuboring:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Manzilni yuboring", request_location=True)],
                              [KeyboardButton(text="Asosiy menu 🏠")]], resize_keyboard=True))
        else:
            await message.answer(
                "Поиск центров автотюнинга по локацию:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Отправьте локацию", request_location=True)],
                              [KeyboardButton(text="Главный меню 🏠")]], resize_keyboard=True))
    except:
        pass


#
@dp.message_handler(
    Text(equals=["Avtoshinalar ta'mirlash xizmatlari", "Шиномонтаж"]))
async def shinomontaj(message: Message):
    try:
        db.update_user_state("Vulkanizatsiya", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)
        if user_state[1] == "uz":
            await message.answer(
                "Avtoshinalarni ta'mirlash, balansirovka va boshqa xizmatlarni qidirish uchun lokatsiyani yuboring:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Manzilni yuboring", request_location=True)],
                              [KeyboardButton(text="Asosiy menu 🏠")]], resize_keyboard=True))
        else:
            await message.answer(
                "Поиск шиномонтажа и вулкнизции по локации:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Отправьте локацию", request_location=True)],
                              [KeyboardButton(text="Главный меню 🏠")]], resize_keyboard=True))
    except:
        pass

#

@dp.message_handler(
    Text(equals=["Moy almashtirish shahobchalari", "Замена масла"]))
async def moyalmashtirish(message: Message):
    try:
        db.update_user_state("Zamenamasla", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)
        if user_state[1] == "uz":
            await message.answer(
                "Avtomobillar moyini almashtirish xizmatlarini qidirish uchun lokatsiyani yuboring:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Manzilni yuboring", request_location=True)],
                              [KeyboardButton(text="Asosiy menu 🏠")]], resize_keyboard=True))
        else:
            await message.answer(
                "Поиск пунктов заменамаслы по локации:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Отправьте локацию", request_location=True)],
                              [KeyboardButton(text="Главный меню 🏠")]], resize_keyboard=True))
    except:
        pass

#
@dp.message_handler(
    Text(equals=["Avtoyuvish shaxobchalarini lokatsiya bo'yicha qidirish", "Поиск автомоек по локации"]))
async def avtomoykaloc(message: Message):
    try:
        db.update_user_state("moyka", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)
        if user_state[1] == "uz":
            await message.answer(
                "Avtoyuvish shaxobchalarini lokatsiya bo'yicha qidirish uchun lokatsiyani yuboring:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Manzilni yuboring", request_location=True)],
                              [KeyboardButton(text="Asosiy menu 🏠")]], resize_keyboard=True))
        else:
            await message.answer(
                "Поиск автомоек по локацию:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Отправьте локацию", request_location=True)],
                              [KeyboardButton(text="Главный меню 🏠")]], resize_keyboard=True))
    except:
        pass
#
@dp.message_handler(Text(equals=["Avtoyuvish xizmati", "Автомойки"]))
async def avtomoyka(message: Message):
    try:
        user_state = db.get_user_state(message.from_user.id)
        if user_state[1] == "uz":
            await message.answer(
                "Ushbu bo'limda siz avtombil yuvish shahobchalari manzillarini qidirib topishingiz mumkin. Marhamat kerakli bo'limni tanlang:",
                reply_markup=moyka_uz)
        else:
            await message.answer(
                "В этом разделе вы сможете ознакомиться с адресами Автомоек. Пожалуйста выберите раздел:",
                reply_markup=moyka_ru)
    except:
        pass


#
@dp.message_handler(
    Text(equals=["Avtoyuvish shaxobchalarini lokatsiya bo'yicha qidirish", "Поиск автомоек по локации"]))
async def avtomoykaloc(message: Message):
    try:
        db.update_user_state("moyka", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)
        if user_state[1] == "uz":
            await message.answer(
                "Avtoyuvish shaxobchalarini lokatsiya bo'yicha qidirish uchun lokatsiyani yuboring:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Manzilni yuboring", request_location=True)],
                              [KeyboardButton(text="Asosiy menu 🏠")]], resize_keyboard=True))
        else:
            await message.answer(
                "Поиск автомоек по локацию:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Отправьте локацию", request_location=True)],
                              [KeyboardButton(text="Главный меню 🏠")]], resize_keyboard=True))
    except:
        pass


@dp.message_handler(
    Text(equals=["Self car wash", "Автомойки самообслужования"]))
async def avtomoykaloc(message: Message):
    try:
        db.update_user_state("moysam", message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)
        if user_state[1] == "uz":
            await message.answer(
                "O'z o'ziga xizmat ko'rsatish avtoyuvish shahobchalarini lokatsiya bo'yicha qidirish:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Manzilni yuboring", request_location=True)],
                              [KeyboardButton(text="Asosiy menu 🏠")]], resize_keyboard=True))
        else:
            await message.answer(
                "Поиск автомоек самообслужования по локации:",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="📍 Отправьте локацию", request_location=True)],
                              [KeyboardButton(text="Главный меню 🏠")]], resize_keyboard=True))


    except:
        pass


@dp.message_handler(content_types=['location'])
async def hadlelocation(message: Message):
    try:
        user_state = db.get_user_state(message.from_user.id)
        if user_state[0] == "Benzin" or user_state[0] == "Metan" or user_state[0] == "Propan":
            lat = message.location.latitude
            lon = message.location.longitude
            zapravkalar = db.select_all_zapravka(user_state[0])
            if zapravkalar:
                masofa = []
                for zapravka in zapravkalar:
                    loc = zapravka[6].split(",")
                    masofa1 = [distance(lat, lon, float(loc[0]), float(loc[1]), "K"), zapravka]
                    masofa.append(masofa1)
                masofa.sort(key=lambda x: x[0])
                for i in range(5):
                    mas = masofa[i]
                    if user_state[1] == "uz":
                        txt = f"AYOQSH nomi: {mas[1][1]}\nManzil: {mas[1][5]}" \
                              f" \nMasofa: {round(mas[0], 2)} km"
                    else:
                        txt = f"АЗС: {mas[1][2]}\nАдрес: {mas[1][5]}" \
                              f" \nРасстояния: {round(mas[0], 2)} км"

                    location_button = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Lokatsiya 📍", callback_data=f"location={mas[1][6]}"),
                            ],
                        ]
                    )

                    await message.answer(txt, reply_markup=location_button)

        elif user_state[0] == "moyka":
            lat = message.location.latitude
            lon = message.location.longitude
            moykalar = db.select_all_moyka(user_state[0])
            if moykalar:
                masofa = []
                for moyka in moykalar:
                    loc = moyka[4].split(",")
                    masofa1 = [distance(lat, lon, float(loc[0]), float(loc[1]), "K"), moyka]
                    masofa.append(masofa1)
                masofa.sort(key=lambda x: x[0])
                for i in range(5):
                    mas = masofa[i]
                    if user_state[1] == "uz":
                        txt = f"Avtoyuvish shahobchasi nomi: {mas[1][1]}\nManzil: {mas[1][3]}" \
                              f" \nMasofa: {round(mas[0], 2)} km"
                    else:
                        txt = f"Автомойка: {mas[1][2]}\nАдрес: {mas[1][3]}" \
                              f" \nРасстояния: {round(mas[0], 2)} км"

                    location_button = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Lokatsiya 📍", callback_data=f"location={mas[1][4]}"),
                            ],
                        ]
                    )

                    await message.answer(txt, reply_markup=location_button)

        elif user_state[0] == "moysam":
            lat = message.location.latitude
            lon = message.location.longitude
            carwash = db.select_all_moysam(user_state[0])
            if carwash:
                masofa = []
                for carw in carwash:
                    loc = carw[4].split(",")
                    masofa1 = [distance(lat, lon, float(loc[0]), float(loc[1]), "K"), carw]
                    masofa.append(masofa1)
                masofa.sort(key=lambda x: x[0])
                for i in range(5):
                    mas = masofa[i]
                    if user_state[1] == "uz":
                        txt = f"Self car wash nomi: {mas[1][1]}\nManzil: {mas[1][3]}" \
                              f" \nMasofa: {round(mas[0], 2)} km"
                    else:
                        txt = f"Мойка самообслужования: {mas[1][2]}\nАдрес: {mas[1][3]}" \
                              f" \nРасстояния: {round(mas[0], 2)} км"

                    location_button = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Lokatsiya 📍", callback_data=f"location={mas[1][4]}"),
                            ],
                        ]
                    )

                    await message.answer(txt, reply_markup=location_button)

        elif user_state[0] == "servis":
            lat = message.location.latitude
            lon = message.location.longitude
            servis = db.select_all_servis()
            if servis:
                masofa = []
                for serv in servis:
                    loc = serv[5].split(",")
                    masofa1 = [distance(lat, lon, float(loc[0]), float(loc[1]), "K"), serv]
                    masofa.append(masofa1)
                masofa.sort(key=lambda x: x[0])
                for i in range(5):
                    mas = masofa[i]
                    if user_state[1] == "uz":
                        txt = f"Avtorervis nomi: {mas[1][1]}\nManzil: {mas[1][3]}\nTel: {mas[1][4]}" \
                              f" \nMasofa: {round(mas[0], 2)} km"
                    else:
                        txt = f"Автосервись: {mas[1][2]}\nАдрес: {mas[1][3]}\nTeл: {mas[1][4]}" \
                              f" \nРасстояния: {round(mas[0], 2)} км"

                    location_button = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Lokatsiya 📍", callback_data=f"location={mas[1][5]}"),
                            ],
                        ]
                    )

                    await message.answer(txt, reply_markup=location_button)

        elif user_state[0] == "tuning":
            lat = message.location.latitude
            lon = message.location.longitude
            tuning = db.select_all_tuning()
            if tuning:
                masofa = []
                for tun in tuning:
                    loc = tun[5].split(",")
                    masofa1 = [distance(lat, lon, float(loc[0]), float(loc[1]), "K"), tun]
                    masofa.append(masofa1)
                masofa.sort(key=lambda x: x[0])
                for i in range(5):
                    mas = masofa[i]
                    if user_state[1] == "uz":
                        txt = f"Tuning atel'e nomi: {mas[1][1]}\nManzil: {mas[1][3]}\nTel: {mas[1][4]}" \
                              f" \nMasofa: {round(mas[0], 2)} km"
                    else:
                        txt = f" Названия студии автотюнинга: {mas[1][2]}\nАдрес: {mas[1][3]}\nTeл: {mas[1][4]}" \
                              f" \nРасстояния: {round(mas[0], 2)} км"

                    location_button = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Lokatsiya 📍", callback_data=f"location={mas[1][5]}"),
                            ],
                        ]
                    )

                    await message.answer(txt, reply_markup=location_button)


        elif user_state[0] == "Vulkanizatsiya":
            lat = message.location.latitude
            lon = message.location.longitude
            shinomontaj = db.select_all_shinomontaj()
            if shinomontaj:
                masofa = []
                for shino in shinomontaj:
                    loc = shino[5].split(",")
                    masofa1 = [distance(lat, lon, float(loc[0]), float(loc[1]), "K"), shino]
                    masofa.append(masofa1)
                masofa.sort(key=lambda x: x[0])
                for i in range(5):
                    mas = masofa[i]
                    if user_state[1] == "uz":
                        txt = f"Shinomontaj nomi: {mas[1][1]}\nManzil: {mas[1][3]}\nTel: {mas[1][4]}" \
                              f" \nMasofa: {round(mas[0], 2)} km"
                    else:
                        txt = f" Названия вулканизации: {mas[1][2]}\nАдрес: {mas[1][3]}\nTeл: {mas[1][4]}" \
                              f" \nРасстояния: {round(mas[0], 2)} км"

                    location_button = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Lokatsiya 📍", callback_data=f"location={mas[1][5]}"),
                            ],
                        ]
                    )

                    await message.answer(txt, reply_markup=location_button)

        elif user_state[0] == "Zamenamasla":
            lat = message.location.latitude
            lon = message.location.longitude
            masla = db.select_all_masla()
            if masla:
                masofa = []
                for masl in masla:
                    loc = masl[5].split(",")
                    masofa1 = [distance(lat, lon, float(loc[0]), float(loc[1]), "K"), masl]
                    masofa.append(masofa1)
                masofa.sort(key=lambda x: x[0])
                for i in range(5):
                    mas = masofa[i]
                    if user_state[1] == "uz":
                        txt = f"Moy almashtirish shaxobchasi nomi: {mas[1][1]}\nManzil: {mas[1][3]}\nTel: {mas[1][4]}" \
                              f" \nMasofa: {round(mas[0], 2)} km"
                    else:
                        txt = f" Названия пунктов замены масла: {mas[1][2]}\nАдрес: {mas[1][3]}\nTeл: {mas[1][4]}" \
                              f" \nРасстояния: {round(mas[0], 2)} км"

                    location_button = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Lokatsiya 📍", callback_data=f"location={mas[1][5]}"),
                            ],
                        ]
                    )

                    await message.answer(txt, reply_markup=location_button)



    except:
        pass
#

@dp.message_handler(Text(equals=["Metan", "Метан", "Propan", "Пропан", "Бензин / Дизел", "Benzin / Dizel"]))
async def benzinmetanpropan(message: Message):
    try:
        statetxt = ""
        if message.text == "Metan" or message.text == "Метан":
            statetxt = "Metan"
        elif message.text == "Propan" or message.text == "Пропан":
            statetxt = "Propan"
        elif message.text == "Бензин / Дизел" or message.text == "Benzin / Dizel":
            statetxt = "Benzin"
        db.update_user_state(statetxt, message.from_user.id)
        user_state = db.get_user_state(message.from_user.id)
        if user_state[1] == "uz":
            await message.answer(
                "Kerakli bo'limni tanlang",
                reply_markup=benzinmetanpropan_uz)
        else:
            await message.answer(
                "Выберите нужный раздел",
                reply_markup=benzinmetanpropan_ru)
    except:
        pass


@dp.message_handler(Text(equals=["Hudud bo'yicha qidirish", "Поиск по регионам", "🔙 Ortga", "🔙 Назад"]))
async def zapravkahudud(message: Message):
    try:
        txt = ""
        user_state = db.get_user_state(message.from_user.id)
        print(user_state[0])
        db.update_user_state(f"zapravkahududs={user_state[0]}", message.from_user.id)

        if user_state[1] == "uz":
            zapravkahududs = db.select_all_hudud("uz")
            zapravkahududs_keyboard = []
            zapravkahududs_keyboard.append(
                [KeyboardButton(text="Asosiy menu 🏠"), KeyboardButton(text="AYOQSH ⛽")])
            for zapravkahudud in zapravkahududs:
                zapravkahududs_keyboard.append([KeyboardButton(text=zapravkahudud[0])])
            zapravkahududs_keyboard.append(
                [KeyboardButton(text="Asosiy menu 🏠"), KeyboardButton(text="AYOQSH ⛽")])

            zapravkahududs_uz = ReplyKeyboardMarkup(
                keyboard=zapravkahududs_keyboard, resize_keyboard=True
            )
            await message.answer("Ushbu bo'limda AYOQSH manzillari bilan tanishishingiz mumkin",
                                 reply_markup=zapravkahududs_uz)
        else:
            zapravkahududs = db.select_all_hudud("ru")
            zapravkahududs_keyboard = []
            zapravkahududs_keyboard.append(
                [KeyboardButton(text="Главный меню 🏠"), KeyboardButton(text="АЗС ⛽")])

            for zapravkahudud in zapravkahududs:
                zapravkahududs_keyboard.append([KeyboardButton(text=zapravkahudud[0])])
            zapravkahududs_keyboard.append(
                [KeyboardButton(text="Главный меню 🏠"), KeyboardButton(text="АЗС ⛽")])

            zapravkahududs_ru = ReplyKeyboardMarkup(
                keyboard=zapravkahududs_keyboard, resize_keyboard=True
            )
            await message.answer("В этом разделе вы сможете ознакомиться с адресами АЗС",
                                 reply_markup=zapravkahududs_ru)

    except:
        pass


@dp.callback_query_handler(text_startswith="location=")
async def showlocation(query: CallbackQuery):
    loc = query.data.split("=")[1].split(",")
    await query.message.answer_location(float(loc[0]), float(loc[1]))


@dp.message_handler()
async def echo(message: Message):
    user_state = db.get_user_state(message.from_user.id)
    if user_state[0] == "Avtosalonlar":
        avtosalon = db.select_one_avtosalon(user_state[1], message.text)
        if avtosalon:
            if user_state[1] == "uz":
                txt = f"Avtosalom nomi: {avtosalon[1]}\nYuridik nomi: {avtosalon[3]}\nManzil: {avtosalon[4]}" \
                      f" \nTel: {avtosalon[5]}\nWeb sayti: {avtosalon[8]}\nTelegram: {avtosalon[9]}, " \
                      f"\nEmail: {avtosalon[10]}\nNarx-navo: {avtosalon[7]}"
            else:
                txt = f"Avtosalom nomi: {avtosalon[2]}\nYuridik nomi: {avtosalon[3]}\nManzil: {avtosalon[4]}" \
                      f" \nTel: {avtosalon[5]}\nWeb sayti: {avtosalon[8]}\nTelegram: {avtosalon[9]}, " \
                      f"\nEmail: {avtosalon[10]}\nNarx-navo: {avtosalon[7]}"

            location_button = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Lokatsiya 📍", callback_data=f"location={avtosalon[6]}"),
                    ],
                ]
            )

            await message.answer(txt, reply_markup=location_button)

    elif user_state[0] == "Texnik_korik":

        texosmotr = db.select_one_texosmotr(user_state[1], message.text)
        if texosmotr:
            if user_state[1] == "uz":
                txt = f"Texnik ko'rikchi nomi: {texosmotr[1]}\nManzil: {texosmotr[3]}\nTel: {texosmotr[4]}"
            else:
                txt = f"Названия организации: {texosmotr[2]}\nАдрес: {texosmotr[3]}\nTeл: {texosmotr[4]}"

            location_button = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Lokatsiya 📍", callback_data=f"location={texosmotr[5]}"),
                    ],
                ]
            )

            await message.answer(txt, reply_markup=location_button)
    #
    elif user_state[0] == "Evokuator":

        evokuat = db.select_one_evakuatr(user_state[1], message.text)
        if evokuat:
            if user_state[1] == "uz":
                txt = f"Evakuator: {evokuat[1]}\nTel: {evokuat[3]}"
            else:
                txt = f"Эвокутор: {evokuat[2]}\nТел: {evokuat[3]}"

            await message.answer(txt)
    #

    elif user_state[0] == "Avtosugurta":

        avtostrax = db.select_one_straxovka(user_state[1], message.text)
        if avtostrax:
            if user_state[1] == "uz":
                txt = f"Avtosugurta kompaniyasi nomi: {avtostrax[1]}\nManzil: {avtostrax[3]}\nTel: {avtostrax[4]}"
            else:
                txt = f"Названия организации: {avtostrax[2]}\nАдрес: {avtostrax[3]}\nTeл: {avtostrax[4]}"

            location_button = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Lokatsiya 📍", callback_data=f"location={avtostrax[5]}"),
                    ],
                ]
            )

            await message.answer(txt, reply_markup=location_button)


    #

    elif user_state[0] == "gaihudud":
        hudud = db.select_one_hudud(user_state[1], message.text)
        if hudud:
            db.update_user_state("gaituman", message.from_user.id)
            if user_state[1] == "uz":
                tumans = db.select_all_tuman(user_state[1], hudud[0])
                tumans_keyboard = []
                tumans_keyboard.append([KeyboardButton(text="Asosiy menu 🏠"), KeyboardButton(text="Ortga 🔙")])
                for tuman in tumans:
                    tumans_keyboard.append([KeyboardButton(text=tuman[0])])
                tumans_keyboard.append([KeyboardButton(text="Asosiy menu 🏠"), KeyboardButton(text="Ortga 🔙")])

                tumans_uz = ReplyKeyboardMarkup(
                    keyboard=tumans_keyboard, resize_keyboard=True
                )
                await message.answer("Ushbu bo'limda YHXB manzillari bilan tanishishingiz mumkin",
                                     reply_markup=tumans_uz)
            else:
                tumans = db.select_all_tuman(user_state[1], hudud[0])
                tumans_keyboard = []
                tumans_keyboard.append([KeyboardButton(text="Главный меню 🏠"), KeyboardButton(text="Назад 🔙")])
                for tuman in tumans:
                    tumans_keyboard.append([KeyboardButton(text=tuman[0])])
                tumans_keyboard.append([KeyboardButton(text="Главный меню 🏠"), KeyboardButton(text="Назад 🔙")])

                tumans_ru = ReplyKeyboardMarkup(
                    keyboard=tumans_keyboard, resize_keyboard=True
                )
                await message.answer("В этом разделе вы сможете ознакомиться с адресами отделени ГИБДД",
                                     reply_markup=tumans_ru)

    elif user_state[0] == "gaituman":
        tuman = db.select_one_tuman(user_state[1], message.text)
        if tuman:
            db.update_user_state("gaituman", message.from_user.id)
            gaihudud = db.select_one_gai(tuman[0])
            if user_state[1] == "uz":
                txt = f"YHXB nomi: {gaihudud[1]}\nManzil: {gaihudud[3]}"
            else:
                txt = f"Названия организации: {gaihudud[2]}\nАдрес: {gaihudud[3]}"

            location_button = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Lokatsiya 📍", callback_data=f"location={gaihudud[4]}"),
                    ],
                ]
            )
            await message.answer(txt, reply_markup=location_button)


    elif user_state[0] == "zapravkahududs=Benzin" or user_state[0] == "zapravkahududs=Metan" or \
            user_state[0] == "zapravkahududs=Propan":
        hudud = db.select_one_hudud(user_state[1], message.text)
        oil_type_txt = user_state[0].split("=")[1]
        if hudud:
            db.update_user_state(f"zapravkatuman={oil_type_txt}", message.from_user.id)
            if user_state[1] == "uz":
                tumans = db.select_all_tuman(user_state[1], hudud[0])
                tumans_keyboard = []
                tumans_keyboard.append([KeyboardButton(text="Asosiy menu 🏠"), KeyboardButton(text="🔙 Ortga")])
                for tuman in tumans:
                    tumans_keyboard.append([KeyboardButton(text=tuman[0])])
                tumans_keyboard.append([KeyboardButton(text="Asosiy menu 🏠"), KeyboardButton(text="🔙 Ortga")])

                tumans_uz = ReplyKeyboardMarkup(
                    keyboard=tumans_keyboard, resize_keyboard=True
                )
                await message.answer("Ushbu bo'limda AYOQSH manzillari bilan tanishishingiz mumkin",
                                     reply_markup=tumans_uz)
            else:
                tumans = db.select_all_tuman(user_state[1], hudud[0])
                tumans_keyboard = []
                tumans_keyboard.append([KeyboardButton(text="Главный меню 🏠"), KeyboardButton(text="🔙 Назад")])
                for tuman in tumans:
                    tumans_keyboard.append([KeyboardButton(text=tuman[0])])
                tumans_keyboard.append([KeyboardButton(text="Главный меню 🏠"), KeyboardButton(text="🔙 Назад")])

                tumans_ru = ReplyKeyboardMarkup(
                    keyboard=tumans_keyboard, resize_keyboard=True
                )
                await message.answer("В этом разделе вы сможете ознакомиться с адресами АЗС",
                                     reply_markup=tumans_ru)

    elif user_state[0] == "zapravkatuman=Benzin" or user_state[0] == "zapravkatuman=Metan" \
            or user_state[0] == "zapravkatuman=Propan":
        tuman = db.select_one_tuman(user_state[1], message.text)
        oil_type_txt = user_state[0].split("=")[1]
        if tuman:
            db.update_user_state("zapravkatuman", message.from_user.id)
            zapravkahududs = db.select_all_zapravkatuman(oil_type_txt, tuman[0])
            for zapravkahudud in zapravkahududs:
                if user_state[1] == "uz":
                    txt = f"AYOQSH nomi: {zapravkahudud[1]}\nManzil: {zapravkahudud[5]}"

                else:
                    txt = f"АЗС: {zapravkahudud[2]}\nАдрес: {zapravkahudud[5]}"
                location_button = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="Lokatsiya 📍", callback_data=f"location={zapravkahudud[6]}"),
                        ],
                    ]
                )

                await message.answer(txt, reply_markup=location_button)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
