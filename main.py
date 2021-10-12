from config import open_weather_token, telegram_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import datetime
import requests

bot = Bot(token=telegram_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Напиши название города чтобы увидеть сводку погоды!')


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': "Ясно \U00002600",
        'Clouds': "Облачно \U00002601",
        'Rain': "Дождь \U00002614",
        'Drizzle': "Ясно \U00002614",
        'Thunderstorm': "Гроза \U000026A1",
        'Snow': "Снег \U0001F328",
        'Mist': "Туман \U0001F32B",
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Отсутствует'

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        sunrise_time = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_time = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        await message.reply(f"————————————————\n"
                            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f"Город: {city}\n"
                            f"————————————————\n"
                            f"Температура: {cur_weather}С°\n"
                            f"Примечание к погоде: {wd}\n"
                            f"Влажность: {humidity}\n"
                            f"Давление: {pressure} мм.рт.ст\n"
                            f"Скорость верта: {wind_speed} м\с\n"
                            f"Рассвет: {sunrise_time}\n"
                            f"Закат: {sunset_time}\n"
                            f"————————————————")
    except:
        await message.reply(f'\U00002620 Возможно, вы неверно ввели название города. \U00002620')


if __name__ == '__main__':
    executor.start_polling(dp)
