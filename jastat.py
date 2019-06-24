# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telebot import apihelper
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time


class OneDay:
    def __init__(self):
        descr = ""
        date = None
        caption = None
        calend = None


# apihelper.proxy = {'https': 'socks5://2150772:WMybmRSO@orbtl.s5.opennetwork.cc:999'}

bot = telebot.TeleBot('656786010:AAEhpC9B1zKF_YI2-t8W-z5_5urxi_GPdbg')
od = OneDay()
od.date = datetime.datetime.utcnow().isoformat() + 'Z'
od.caption = 'Health_Score'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def calend_connect():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    od.calend = service


def event_add():
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    event = {
        'summary': od.caption,
        'location': '',
        'description': od.descr,
        'start': {
            'dateTime': od.date

        },
        'end': {
            'dateTime': od.date
        },
        'recurrence': [

        ],
        'attendees': [
        ],
        'reminders': {
        },
    }

    event = od.calend.events().insert(calendarId='f2c4fjmov87b3vgtvqbaf0aabo@group.calendar.google.com',
                                      body=event).execute()


def delDay():
    now1 = datetime.datetime.now()
    start_date = datetime.datetime(now1.year, now1.month, now1.day, 00, 00, 00, 0).isoformat() + 'Z'
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC timedate.today

    eventsResult = od.calend.events().list(
        calendarId='f2c4fjmov87b3vgtvqbaf0aabo@group.calendar.google.com', timeMin=start_date, timeMax=now,
        maxResults=5, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('нет событий на ближайшие сутки')
    else:
        msg = '<b>События на ближайшие сутки:</b>\n'
        for event in events:
            od.calend.events().delete(calendarId='f2c4fjmov87b3vgtvqbaf0aabo@group.calendar.google.com',
                                      eventId=event['id']).execute()


# Handle '/start'
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('Да')
    itembtnv = types.KeyboardButton('Нет')
    markup.add(itembtna, itembtnv)
    bot.send_message(message.from_user.id, 'Занимался спортом сегодня?', reply_markup=markup)
    bot.register_next_step_handler(message, get_sport)


def get_sport(message):
    bot.send_message(message.from_user.id, 'Ел витамины?')
    od.descr = 'Спорт:' + message.text + '\n'
    bot.register_next_step_handler(message, get_vitamin)


def get_vitamin(message):
    od.descr = od.descr + 'Витамины:' + message.text + '\n'
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('<5')
    itembtnv = types.KeyboardButton('6')
    itembtn1 = types.KeyboardButton('8')
    itembtn2 = types.KeyboardButton('>8')
    markup.add(itembtna, itembtnv, itembtn1, itembtn2)
    bot.send_message(message.from_user.id, 'А сколько спал ночью?', reply_markup=markup)
    bot.register_next_step_handler(message, get_sleep)


def get_sleep(message):
    od.descr = od.descr + 'Сон:' + message.text + '\n'
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('Да')
    itembtnv = types.KeyboardButton('Нет')
    markup.add(itembtna, itembtnv)
    bot.send_message(message.from_user.id, 'Бухал?', reply_markup=markup)
    bot.register_next_step_handler(message, get_alko)


def get_alko(message):
    od.descr = od.descr + 'Алкоголь:' + message.text + '\n'
    bot.send_message(message.from_user.id, 'Зарядку делал?')
    bot.register_next_step_handler(message, get_exercise)


def get_exercise(message):
    od.descr = od.descr + 'Зарядка:' + message.text + '\n'
    bot.send_message(message.from_user.id, 'И, конечно, курил?')
    bot.register_next_step_handler(message, get_smoking)


def get_smoking(message):
    od.descr = od.descr + 'Курение:' + message.text + '\n'
    print(od.descr)
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Ясно. Вот твой день: ' + '\n' + od.descr, reply_markup=markup)
    calend_connect()
    delDay()
    event_add()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Hi!":
        bot.send_message(message.from_user.id, "Hiiii!!")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "привет")
    else:
        bot.send_message(message.from_user.id, "Write /help.")


bot.polling(none_stop=True, interval=0)