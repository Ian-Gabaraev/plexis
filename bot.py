#!/home/a0251026/domains/cit.chrge.ru/public_html/telebot/env/bin/python

import telebot
import wod
import remdict
import datetime
import os
import random

token = '987997588:AAH4fLUIhpzrJCgDkk79kThB4iMBU1KjZKo'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['hi', 'bye'])
def send_welcome(message):
    bot.reply_to(message, "Ciao!")


def extract_arg(arg):
    return ' '.join(arg.split()[1:])


def create_dictionary(uid):
    if not os.path.exists('dictionaries/'+str(uid)):
        with open('dictionaries/'+str(uid), 'w'): 
            pass


@bot.message_handler(commands = ['add', 'a'])
def add_to_dictionary(message):
    uid = message.from_user.id
    word = extract_arg(message.text)
    try:
        definition = get_definition(word)
    except:
        bot.reply_to(message, 'Not a word. Check spelling 🤔')
    else:
        try:
            f = open("dictionaries/%d" % uid,"a+")
        except:
            bot.reply_to(message, 'ERROR.Cannot write to file.')
        else:
            f.write("%s : %s \n" % (word, definition))
            f.close()
            bot.reply_to(message, 'Your dictionary was updated.')


def get_info():
    string = ""
    try:
        rm = wod.random_word(7)
        string += rm + "\n"
        string += remdict.get_definition(rm) + "\n"
    except:
        raise Exception
    else:
        string += remdict.get_example_of_use(rm)
        return string


def get_definition(word):
    definition = remdict.get_definition(word)
    return definition
    

@bot.message_handler(commands=['define', 'd'])
def define(message):
    word = extract_arg(message.text)
    try:
        definition = get_definition(word)
    except:
        bot.reply_to(message, 'Not a word. Check spelling 🤔')
    else:
        bot.reply_to(message, definition)
    
    
@bot.message_handler(commands=['random', 'r'])
def random_word(message):
    try:
        bot.reply_to(message, get_info())
    except:
        random_word(message)


@bot.message_handler(commands=['help', 'h'])
def random_word(message):
    commands_list = """ 
    /a word or /add word - add a word to your dictionary
    /h or /help  - list all commands
    /d word or /define word - define a word
    /r or /random - returns a random word 
    """
    bot.reply_to(message, commands_list)
    

@bot.message_handler(commands=['start'])
def greet(message):

    uid = message.from_user.id
    username = str(message.from_user.first_name) + " " + str(message.from_user.last_name)
    create_dictionary(uid)
    f = open("stats/userlist.log","a+")
    f.write("%d %s %s \n" % (uid, username, datetime.datetime.now()))
    f.close()
    bot.reply_to(message, send_greetings(username))

def send_greetings(username):
    salutations = [
        "Good to see you, ",
        "Nice to see you,",
        "Look what the cat dragged in!",
        "Howdy, ",
        "Long time no see",
        "Look who it is!"
    ]
    return "%s %s." % (salutations[random.randint(0, len(salutations)-1)], username)

bot.infinity_polling(True)    
bot.polling()