from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

select_lang = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="O'zbek tili 🇺🇿"),
            KeyboardButton(text="Rus tili 🇷🇺"),
        ],

    ], resize_keyboard=True
)

main_menu_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Avto ehtiyot qismlar"),
        ],
        [
            KeyboardButton(text="Avtosalonlar 🚗"), KeyboardButton(text="Avtoservislar 🔧")
        ],
        [KeyboardButton(text="AYOQSH ⛽"), KeyboardButton(text="Avtoyuvish xizmati")],
        [KeyboardButton(text="YHXBB 👮🏻‍♂"), KeyboardButton(text="Texnik ko`riklar 📝")],
        [KeyboardButton(text="Avtosugurta"), KeyboardButton(text="Evakuator")],
        [KeyboardButton(text="Tilni o`zgartirish 🇺🇿/🇷🇺"), KeyboardButton(text="Ma'lumot")]

    ], resize_keyboard=True

)

main_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Автозапчасти"),
        ],
        [
            KeyboardButton(text="Автосалоны 🚗"), KeyboardButton(text="Автосервисы 🔧")
        ],
        [KeyboardButton(text="АЗС ⛽"), KeyboardButton(text="Автомойки")],
        [KeyboardButton(text="ГУБДД 👮🏻‍♂"), KeyboardButton(text="Автотехосмотр 📝")],
        [KeyboardButton(text="Автострохования"), KeyboardButton(text="Эвакуатор")],
        [KeyboardButton(text="Изменения языка 🇺🇿/🇷🇺"), KeyboardButton(text="Инфо")]

    ], resize_keyboard=True
)


zapravka_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Benzin / Dizel"),
        ],
        [
            KeyboardButton(text="Metan"), KeyboardButton(text="Propan")
        ],
        [KeyboardButton(text="Asosiy menu 🏠")]

    ], resize_keyboard=True
)

zapravka_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Бензин / Дизел"),
        ],
        [
            KeyboardButton(text="Метан"), KeyboardButton(text="Пропан")
        ],
        [KeyboardButton(text="Главный меню 🏠")]

    ], resize_keyboard=True
)
#
# benzin_uz = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="Benzin yetkazib berish")
#         ],
#         [
#             KeyboardButton(text="Lokatsiya bo'yicha qidirish (📍 Manzilni yuboring)", request_location=True)
#         ],
#         [KeyboardButton(text="Hudud bo'yicha qidirish")],
#         [KeyboardButton(text="Asosiy menu 🏠"), KeyboardButton(text="Ortga ⬅")],
#
#     ], resize_keyboard=True
# )
#
# benzin_ru = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="Доставка бензина")
#         ],
#         [
#             KeyboardButton(text="Поиск по локации (📍 Отправте локацию)", request_location=True)
#         ],
#         [KeyboardButton(text="Поиск по регионам")],
#         [KeyboardButton(text="Главный меню 🏠"), KeyboardButton(text="Назад ⬅")],
#
#     ], resize_keyboard=True
# )

benzinmetanpropan_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Lokatsiya bo'yicha qidirish (📍 Manzilni yuboring)", request_location=True)
        ],
        [KeyboardButton(text="Hudud bo'yicha qidirish")],
        [KeyboardButton(text="Asosiy menu 🏠"), KeyboardButton(text="Ortga ⬅")],

    ], resize_keyboard=True
)

benzinmetanpropan_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Поиск по локации (📍 Отправте локацию)", request_location=True)
        ],
        [KeyboardButton(text="Поиск по регионам")],
        [KeyboardButton(text="Главный меню 🏠"), KeyboardButton(text="Назад ⬅")],

    ], resize_keyboard=True
)

moyka_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Avtoyuvish shaxobchalarini lokatsiya bo'yicha qidirish"),
        ],
        [
            KeyboardButton(text="Self car wash"), KeyboardButton(text="Avtoyuvish chaqiruv xizmati")
        ],
        [KeyboardButton(text="Asosiy menu 🏠")]

    ], resize_keyboard=True
)

moyka_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Поиск автомоек по локации"),
        ],
        [
            KeyboardButton(text="Автомойки самообслужования"), KeyboardButton(text="Вызов автомойки")
        ],
        [KeyboardButton(text="Главный меню 🏠")]

    ], resize_keyboard=True
)

servic_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Asosiy menu 🏠")
        ],
        [
            KeyboardButton(text="Avtomobillarga texnik xizmat ko'rsatish shaxobchalari"),
        ],
        [
            KeyboardButton(text="Tyuning atel'elar")
        ],
        [
            KeyboardButton(text="Avtoshinalar ta'mirlash xizmatlari")
        ],
        [
            KeyboardButton(text="Moy almashtirish shahobchalari")
        ],
        [KeyboardButton(text="Texnik xizmat chaqiruvi"), KeyboardButton(text="Asosiy menu 🏠")]

    ], resize_keyboard=True
)

servic_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Главный меню 🏠")
        ],
        [
            KeyboardButton(text="Тех-обслужования автомобилей"),
        ],
        [
          KeyboardButton(text="Замена масла")
        ],
        [
            KeyboardButton(text="Тюнинг ателе")
        ],
        [
            KeyboardButton(text="Шиномонтаж")
        ],
        [KeyboardButton(text="Вызов техобслуги"), KeyboardButton(text="Главный меню 🏠")]

    ], resize_keyboard=True
)