# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telebot import apihelper

#apihelper.proxy = {'https': 'socks5://2150772:WMybmRSO@orbtl.s5.opennetwork.cc:999'}

bot = telebot.TeleBot('656786010:AAEhpC9B1zKF_YI2-t8W-z5_5urxi_GPdbg')


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
    bot.register_next_step_handler(message, get_vitamin)


def get_vitamin(message):
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('<5')
    itembtnv = types.KeyboardButton('6')
    itembtn1 = types.KeyboardButton('8')
    itembtn2 = types.KeyboardButton('>8')
    markup.add(itembtna, itembtnv, itembtn1, itembtn2)
    bot.send_message(message.from_user.id, 'А сколько спал ночью?', reply_markup=markup)
    bot.register_next_step_handler(message, get_sleep)


def get_sleep(message):
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('Да')
    itembtnv = types.KeyboardButton('Нет')
    markup.add(itembtna, itembtnv)
    bot.send_message(message.from_user.id, 'Бухал?', reply_markup=markup)
    bot.register_next_step_handler(message, get_alko)


def get_alko(message):
    bot.send_message(message.from_user.id, 'Зарядку делал?')
    bot.register_next_step_handler(message, get_exercise)


def get_exercise(message):
    bot.send_message(message.from_user.id, 'И, конечно, курил?')
    bot.register_next_step_handler(message, get_smoking)


def get_smoking(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Ясно', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Hi!":
        bot.send_message(message.from_user.id, "Hiiii!!")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "привет")
    else:
        bot.send_message(message.from_user.id, "Write /help.")


bot.polling(none_stop=True, interval=0)