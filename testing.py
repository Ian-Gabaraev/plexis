import telebot
import wod
import remdict
import datetime
import os
import random
import time

token = '987997588:AAH4fLUIhpzrJCgDkk79kThB4iMBU1KjZKo'
bot = telebot.TeleBot(token)
path = '/home/a0251026/domains/cit.chrge.ru/public_html/telebot/dictionaries/'
users = os.listdir(path)


def load_dictionary(filename):
    return [line.rstrip('\n') for line in open(filename)]

def get_info_better(word):
    string = ""
    try:
        string += "📌 %s \n" % word
        string += "🔎 %s \n" % remdict.get_definition(word)
    except:
        raise Exception
    else:
        string += "📖 %s \n" % remdict.get_example_of_use(word)
        return string

def rape_me():
    for id in users:
        list_of_words = load_dictionary('/home/a0251026/domains/cit.chrge.ru/public_html/telebot/knowledgebase/devilish.dictionary')
        word = list_of_words[random.randint(0, len(list_of_words)-1)]
        bot.send_message(id, text= 'Good morning,\nThis is your word of the day 🧩')
        bot.send_message(id, text= get_info_better(word.lower()))



rape_me()