import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '8576952171:AAE3Z3FrwkvTIUxnWuqtvmfgRqYFIMrofsA'
bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Узнать погоду'))
keyboard.add(KeyboardButton('О проекте'))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = '''Привет! Я бот для определения погоды
    Чтобы узнать погоду, присылай координаты и я всё тебе расскажу'''
    bot.send_message(bot.chat.id, text)

@bot.message_handler(regexp='Узнать погоду')
def send_about_weather(message):
    bot.send_message(bot.chat.id, 'Скажи мне свои координаты и я скажу твою погоду')

@bot.message_handler(regexp='О проекте')
def send_about(message):
    text = '''Этот бот создан с помощью @BotFather и разработан @wansed239
    Сам этот проект реализован и защищен в рамках программы "Код будущего"
    Разработки велись недолго, всего несколько дней
    Даже если этот бот довольно примитивный, мне понравился опыт разработки, и верю, что дальнейшие проекты будут ещё лучше
    Надеюсь, вам понравилось'''
    bot.send_message(bot.chat.id, text)

@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon, lat = message.location.longitude, message.location.latitude
    text = get_weather(lon, lat)
    bot.send_message(bot.chat.id, text)

@bot.message_handler(commands=['text'])
def send(message):
    text = '''Извини, я пока не могу работать с текстовым форматом
    Если хочешь скинуть координаты, пришли их в виде геопозиции'''
    bot.send_message(bot.chat.id, text)

def get_weather(lon, lat):
    import requests

    URL = 'https://api.openweathermap.org/data/2.5/weather'
    API = '863bb56ef29bf0f48d3ae70a759a5463'
    PARAMS = {
        'appid': API,
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'lang': 'ru'
    }
    EMOJI = {
        200: '⛈️',
        201: '⛈️',
        202: '⛈️',
        210: '🌩️',
        211: '🌩️',
        212: '🌩️',
        221: '🌩️',
        230: '⛈️',
        231: '⛈️',
        232: '⛈️',
        301: '🌧️',
        302: '🌧️',
        310: '🌧️',
        311: '🌧️',
        312: '🌧️',
        313: '🌧️',
        314: '🌧️',
        321: '🌧️',
        500: '🌧️',
        501: '🌧️',
        502: '🌧️',
        503: '🌧️',
        504: '🌧️',
        511: '🌧️',
        520: '🌧️',
        521: '🌧️',
        522: '🌧️',
        531: '🌧️',
        600: '🌨️',
        601: '🌨️',
        602: '🌨️',
        611: '🌨️',
        612: '🌨️',
        613: '🌨️',
        615: '🌨️',
        616: '🌨️',
        600: '🌨️',
        620: '🌨️',
        621: '🌨️',
        622: '🌨️',
        701: '🌫️',
        711: '🌫️',
        721: '🌫️',
        731: '🌫️',
        741: '🌫️',
        751: '🌫️',
        761: '🌫️',
        762: '🌫️',
        771: '🌫️',
        781: '🌫️',
        800: '☀️',
        801: '🌤️',
        802: '☁️',
        803: '☁️',
        804: '☁️'
    }

    response = requests.get(URL, PARAMS)
    json = response.json()

    city_name = json['name']
    description = json['weather'][0]['description']
    code = json['weather'][0]['id']
    temp = json['main']['temp']
    temp_feels_like = json['main']['feels_like']
    humidity = json['main']['humidity']

    text_city = f'🏙️ Погода в: {city_name}\n'
    text_description = f'{EMOJI[code]} {description}\n'
    text_temp1 = f'🌡️ Температура {temp}\n'
    text_temp2 = f'🌡️ Ощущается как {temp_feels_like}\n'
    text_humidity = f'💧 Влажность {humidity}'
    text = text_city + text_description + text_temp1 + text_temp2 + text_humidity

    return text

bot.infinity_polling()