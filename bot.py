from keyboard import keyboard
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data_base import sqlite_db
from dotenv import load_dotenv


import os
import settings
import logging
import sqlite3 as sq
import requests
import time

load_dotenv()

logging.basicConfig(level=logging.INFO)

VLAD_ID = settings.VLAD_ID
ROMA_ID = settings.ROMA_ID
EVAN_ID = settings.EVAN_ID
TOKEN = os.getenv('TOKEN')
API_TOKEN = os.getenv('API_TOKEN')

HEADERS = {'Authorization': f'OAuth {API_TOKEN}'}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
base = sq.connect('serials.db')
cur = base.cursor()


class FSMEvan(StatesGroup):
    name_serials = State()
    season = State()
    series = State()


class FSMRoma(StatesGroup):
    name_serials_roma = State()
    season_roma = State()
    series_roma = State()


class FSMVlad(StatesGroup):
    name_serials_vlad = State()
    season_vlad = State()
    series_vlad = State()


def get_api_answer(current_timestamp):
    """Request to API."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        requests.get(url=settings.ENDPOINT,
                     headers=HEADERS,
                     params=params)
    except Exception:
        raise Exception('Network problem, please try again later')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Чьи сериалы хочешь посмотреть?',
                           reply_markup=keyboard.mainMenu)


class Evan(object):
    """Главное меню Евана"""
    @dp.callback_query_handler(lambda call: call.data == 'evan')
    async def evan_serials(message: types.Message):
        await bot.send_message(message.from_user.id,
                               'Что хочешь сделать?',
                               reply_markup=keyboard.evanMenu)
        await message.answer()

    """Все сериалы Евана"""
    @dp.callback_query_handler(lambda call: call.data == 'evan_serials')
    async def evan_all_serials(message: types.Message):
        await bot.send_message(message.from_user.id,
                               text='Мои сериалы:')
        await message.answer()
        for slots in cur.execute(
                                 'SELECT name_serial FROM serials_evan'
                                 ).fetchall():
            await bot.send_message(message.from_user.id,
                                   text=f'{slots[0]}')

    """Машина состояний Евана"""
    @dp.callback_query_handler(lambda call: call.data == 'evan_new_serial',
                               state=None)
    async def choice_evan(message: types.Message):
        if message.from_user.id == EVAN_ID:
            await FSMEvan.name_serials.set()
            await bot.send_message(message.from_user.id,
                                   text='Введи название сериала')
            await message.answer()

    @dp.message_handler(state=FSMEvan.name_serials)
    async def name_serials_evan(message: types.Message, state: FSMContext):
        if message.from_user.id == EVAN_ID:
            async with state.proxy() as data:
                data['name_serials'] = message.text
            await message.reply('Введи номер сезона')
            await FSMEvan.next()

    @dp.message_handler(state=FSMEvan.season)
    async def season_evan(message: types.Message, state: FSMContext):
        if message.from_user.id == EVAN_ID:
            async with state.proxy() as data:
                data['season'] = message.text
            await message.reply('Введи номер серии')
            await FSMEvan.next()

    @dp.message_handler(state=FSMEvan.series)
    async def series_evan(message: types.Message, state: FSMContext):
        if message.from_user.id == EVAN_ID:
            async with state.proxy() as data:
                data['series'] = message.text
            sqlite_db.sql_start_evan()
            cur.execute(f'INSERT OR REPLACE INTO serials_evan(user_id, name_serial, season, series) VALUES ({message.from_user.id},?, ?, ?)', tuple(data.values()))
            base.commit()
            await message.reply('Сериал успешно добавлен')
            await state.finish()

    """Вспомнить серию Еван"""
    @dp.callback_query_handler(lambda call: call.data == 'evan_recall')
    async def recall_evan(message: types.Message):

        await bot.send_message(message.from_user.id,
                               text='Просмотренные серии',
                               reply_markup=keyboard.evanChoice)
        await message.answer()

    @dp.callback_query_handler(lambda call: call.data == 'evan_choice')
    async def evan_choice(message: types.Message):
        if message.from_user.id == EVAN_ID:
            for slots in cur.execute('SELECT DISTINCT name_serial FROM serials_evan').fetchall():
                for rat in cur.execute(f"SELECT name_serial, season, series FROM (SELECT DISTINCT * FROM serials_evan) WHERE name_serial='{slots[0]}'").fetchall():
                    await bot.send_message(message.from_user.id,
                                           text=f'Просмотренные серии\n{str(rat)}')
        await message.answer()


class Roma(object):
    """Главное меню Ромы"""
    @dp.callback_query_handler(lambda call: call.data == 'roma')
    async def roma_serials(message: types.Message):
        await bot.send_message(message.from_user.id,
                               'Что хочешь сделать?',
                               reply_markup=keyboard.romaMenu)
        await message.answer()

    """Все сериалы Ромы"""
    @dp.callback_query_handler(lambda call: call.data == 'roma_serials')
    async def evan_all_serials(message: types.Message):
        await bot.send_message(message.from_user.id,
                               text='Мои сериалы:')
        await message.answer()
        for slots in cur.execute('SELECT DISTINCT name_serial FROM serials_roma').fetchall():
            await bot.send_message(message.from_user.id,
                                   text=f'{slots[0]}')

    """Машина состояний Ромы"""
    @dp.callback_query_handler(lambda call: call.data == 'roma_new_serial')
    async def choice(message: types.Message):
        if message.from_user.id == ROMA_ID:
            await FSMRoma.name_serials_roma.set()
            await bot.send_message(message.from_user.id,
                                   text='Введи название сериала')
            await message.answer()

    @dp.message_handler(state=FSMRoma.name_serials_roma)
    async def name_serials_evan(message: types.Message, state: FSMContext):
        if message.from_user.id == ROMA_ID:
            async with state.proxy() as data:
                data['name_serials_roma'] = message.text
            await message.reply('Введи номер сезона')
            await FSMRoma.next()

    @dp.message_handler(state=FSMRoma.season_roma)
    async def season_evan(message: types.Message, state: FSMContext):
        if message.from_user.id == ROMA_ID:
            async with state.proxy() as data:
                data['season_roma'] = message.text
            await message.reply('Введи номер серии')
            await FSMRoma.next()

    @dp.message_handler(state=FSMRoma.series_roma)
    async def series_evan(message: types.Message, state: FSMContext):
        if message.from_user.id == ROMA_ID:
            async with state.proxy() as data:
                data['series_roma'] = message.text
            sqlite_db.sql_start_roma()
            cur.execute(f'INSERT OR REPLACE INTO serials_roma(user_id,name_serial, season, series) VALUES ({message.from_user.id},?, ?, ?)', tuple(data.values()))
            base.commit()
            await message.reply('Сериал успешно добавлен')
            await state.finish()

    """Вспомнить серию Рома"""
    @dp.callback_query_handler(lambda call: call.data == 'roma_recall')
    async def recall_evan(message: types.Message):

        await bot.send_message(message.from_user.id,
                               text='Просмотренные серии',
                               reply_markup=keyboard.romaChoice)
        await message.answer()

    @dp.callback_query_handler(lambda call: call.data == 'roma_choice')
    async def roma_choice(message: types.Message):
        if message.from_user.id == ROMA_ID:
            for slots in cur.execute('SELECT DISTINCT name_serial FROM serials_roma').fetchall():
                for rat in cur.execute(f"SELECT name_serial, season, series FROM (SELECT DISTINCT * FROM serials_roma) WHERE name_serial='{slots[0]}'").fetchall():
                    await bot.send_message(message.from_user.id,
                                           text=f'Просмотренные серии\n{str(rat)}')

        await message.answer()


class Vlad(object):
    """Главное меню Влада"""
    @dp.callback_query_handler(lambda call: call.data == 'vlad')
    async def vlad_serials(message: types.Message):
        await bot.send_message(message.from_user.id,
                               'Что хочешь сделать?',
                               reply_markup=keyboard.vladMenu)
        await message.answer()

    """Все сериалы Влада"""
    @dp.callback_query_handler(lambda call: call.data == 'vlad_serials')
    async def vlad_all_serials(message: types.Message):
        await bot.send_message(message.from_user.id,
                               text='Мои сериалы:')
        await message.answer()
        for slots in cur.execute('SELECT DISTINCT name_serial FROM serials_vlad').fetchall():
            await bot.send_message(message.from_user.id,
                                   text=f'{slots[0]}')

    """Машина состояний Влад"""
    @dp.callback_query_handler(lambda call: call.data == 'vlad_new_serial')
    async def choice(message: types.Message):
        if message.from_user.id == VLAD_ID:
            await FSMVlad.name_serials_vlad.set()
            await bot.send_message(message.from_user.id, text='Введи название сериала')
            await message.answer()

    @dp.message_handler(state=FSMVlad.name_serials_vlad)
    async def name_serials_vlad(message: types.Message, state: FSMContext):
        if message.from_user.id == VLAD_ID:
            async with state.proxy() as data:
                data['name_serials_vlad'] = message.text
            await message.reply('Введи номер сезона')
            await FSMVlad.next()

    @dp.message_handler(state=FSMVlad.season_vlad)
    async def season_vlad(message: types.Message, state: FSMContext):
        if message.from_user.id == VLAD_ID:
            async with state.proxy() as data:
                data['season_vlad'] = message.text
            await message.reply('Введи номер серии')
            await FSMVlad.next()

    @dp.message_handler(state=FSMVlad.series_vlad)
    async def series_vlad(message: types.Message, state: FSMContext):
        if message.from_user.id == VLAD_ID:
            async with state.proxy() as data:
                data['series_vlad'] = message.text
            sqlite_db.sql_start_vlad()
            cur.execute(f'INSERT OR REPLACE INTO serials_vlad(user_id, name_serial, season, series) VALUES ({message.from_user.id},?, ?, ?)', tuple(data.values()))
            base.commit()
            await message.reply('Сериал успешно добавлен')
            await state.finish()

    """Вспомнить серию Влад"""
    @dp.callback_query_handler(lambda call: call.data == 'vlad_recall')
    async def recall_vlad(message: types.Message):
        await bot.send_message(message.from_user.id,
                               text='Выбери сериал',
                               reply_markup=keyboard.vladChoice)
        await message.answer()

    @dp.callback_query_handler(lambda call: call.data == 'vlad_choice')
    async def vlad_series(message: types.Message):
        if message.from_user.id == VLAD_ID:
            for slots in cur.execute('SELECT DISTINCT name_serial FROM serials_vlad').fetchall():
                for rat in cur.execute(f"SELECT name_serial, season, series FROM (SELECT DISTINCT * FROM serials_vlad) WHERE name_serial='{slots[0]}'").fetchall():
                    await bot.send_message(message.from_user.id,
                                           text=f'Просмотренные серии\n{str(rat)}')
        await message.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
