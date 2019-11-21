#!/home/a0251026/domains/cit.chrge.ru/public_html/telebot/env/bin/python

import telebot
import wod
import requests
import remdict
import datetime
import os
import utils
import crypto
import random
import time
import socket
import timeit
import morning_reading
import ud
from classes import wordreference

TOKEN = '987997588:AAH4fLUIhpzrJCgDkk79kThB4iMBU1KjZKo'
bot = telebot.TeleBot(TOKEN)

PATH_TO_DICTIONARIES = '/home/a0251026/domains/cit.chrge.ru/public_html/telebot/dictionaries/'
PATH_TO_DEVIL = '/home/a0251026/domains/cit.chrge.ru/public_html/telebot/knowledgebase/devilish.dictionary'
ABS_PATH = '/home/a0251026/domains/cit.chrge.ru/public_html/telebot/'


def load_dictionary(filename):
    return [line.rstrip('\n') for line in open(filename)]


def notify_user_by(uid, message):
    bot.send_message(uid, text= message)    


def open_user_dictionary(message):
    try:
        f = open("%s%s" % (PATH_TO_DICTIONARIES, str(message.from_user.id)), "a+")
    except:
        bot.reply_to(message, '№Ё Can\'t open file')
        raise Exception
    else:
        return f


@bot.message_handler(commands=['article', 'art'])
def post_random_article(message):
    bot.send_message(message.from_user.id, text = morning_reading.pick_an_article())


@bot.message_handler(commands=['podcast', 'pod'])
def send_podcast(message):

    link = utils.pick_a_podcast()
    _file = requests.get(link[0])
    
    if _file.status_code != 200:
        bot.send_message(message.from_user.id, text = 'Something went wrong.')
        
    else:
        if os.path.exists('/home/a0251026/domains/cit.chrge.ru/public_html/telebot/podcasts/%s.mp3' % link[1]):
            audio = open('/home/a0251026/domains/cit.chrge.ru/public_html/telebot/podcasts/%s.mp3' % link[1], 'rb')
            try:
                bot.send_audio(message.from_user.id, audio, performer = 'Moth Radio - pLexis', title = link[1].replace('_', ' '))
            except telebot.apihelper.ApiException:
                send_podcast(message)
            
        else:
            try:
                with open('/home/a0251026/domains/cit.chrge.ru/public_html/telebot/podcasts/%s.mp3' % link[1], 'wb') as f:
                    f.write(_file.content)
                audio = open('/home/a0251026/domains/cit.chrge.ru/public_html/telebot/podcasts/%s.mp3' % link[1], 'rb')
                bot.send_audio(message.from_user.id, audio, performer = 'Moth Radio - pLexis', title = link[1].replace('_', ' '))
            except telebot.apihelper.ApiException:
                send_podcast(message)
            except socket.timeout:
                send_podcast(message)
            finally:
                f.close()


@bot.message_handler(commands=['urbandictionary', 'ud'])
def use_urban_dictionary(message):
    word = extract_arg(message.text)
    bot.reply_to(message, ud.find_a(word))
    
    
@bot.message_handler(commands=['at', 'audiotest', 'say'])
def send_audio(message):
    word = extract_arg(message.text)
    _file = requests.get('https://howjsay.com/mp3/%s.mp3' % word)
    if word == '' or _file.status_code != 200:
        bot.send_message(message.from_user.id, text = 'Wrong word.')
    else:
        with open('/home/a0251026/domains/cit.chrge.ru/public_html/telebot/audio.mp3', 'wb') as f:
            f.write(_file.content)
        audio = open('/home/a0251026/domains/cit.chrge.ru/public_html/telebot/audio.mp3', 'rb')
        bot.send_audio(message.from_user.id, audio, performer = 'HowJSay', title = word)


@bot.message_handler(commands=['wordreference', 'wr'])
def use_word_reference(message):
    # start = timeit.default_timer()
    word = extract_arg(message.text)
    wr = wordreference.WordReference(word, emojis = ['№', '№'])
    bot.reply_to(message, wr.get_full_info())
    # elapsed = timeit.default_timer() - start
    # bot.reply_to(message, "\nComplete in %f seconds" % elapsed)


@bot.message_handler(commands=['truncate', 't'])
def truncate_dictionary(message):
    if not os.stat('%s%s' % (PATH_TO_DICTIONARIES, message.from_user.id)).st_size == 0:
        try:
            dictionary = open('%s%s' % (PATH_TO_DICTIONARIES, str(message.from_user.id)), 'w')
        except Exception as e:
            bot.reply_to(message, str(e))
        else:
            dictionary.close()
            bot.reply_to(message, '№ Your dictionary is now empty.')
    else:
        bot.reply_to(message, '№Ё Your dictionary is empty already.')
    

@bot.message_handler(commands=['prefill', 'p'])
def prefill_user_dictionary(message):
    truncate_dictionary(message)
    list_of_words = load_dictionary(PATH_TO_DEVIL)
    random.shuffle(list_of_words)
    try:
        f = open_user_dictionary(message)
    except:
        bot.reply_to(message, '№Є Prefill is not available now')
    else:
        bot.reply_to(message, 'тяИ It\'s gonna take some time.')
        for index in range(20):
            try:
                definition = get_definition(list_of_words[index].lower())
            except:
                continue
            else:
                f.write("%s : %s \n" % (list_of_words[index], definition))
        bot.reply_to(message, 'тяИ Your dictionary has been filled.')
        f.close()


@bot.message_handler(commands=['userlist', 'ul'])
def list_all_users(message):
    users = os.listdir(PATH_TO_DICTIONARIES)
    bot.reply_to(message, "\n".join(users))

    
@bot.message_handler(commands=['mad', 'm'])
def rape_me(message):
    list_of_words = load_dictionary('/home/a0251026/domains/cit.chrge.ru/public_html/telebot/knowledgebase/devilish.dictionary')
    word = list_of_words[random.randint(0, len(list_of_words)-1)]
    bot.reply_to(message, get_info_better(word.lower()))



@bot.message_handler(commands=['crypto', 'c'])
def crypto_stats(message):
    bot.reply_to(message, crypto.check_favorites())
    

@bot.message_handler(commands=['see', 's'])
def view_dictionary(message):
    if not os.stat('%s%s' % (PATH_TO_DICTIONARIES, message.from_user.id)).st_size == 0:
        try:
            my_words = [line.split(':')[0] for line in open('%s%s' % (PATH_TO_DICTIONARIES, str(message.from_user.id)))]
        except Exception as e:
            bot.reply_to(message, str(e))
        else:
            response = "\n".join(my_words)
            bot.reply_to(message, "№ЁYou've got %d words\n\n%s" % (len(my_words), response))
    else:
        bot.reply_to(message, '№ЄЋ Your dictionary is empty.')
    

def extract_arg(arg):
    return ' '.join(arg.split()[1:])


def create_dictionary(uid):
    if not os.path.exists('/home/a0251026/domains/cit.chrge.ru/public_html/telebot/dictionaries/'+str(uid)):
        with open('/home/a0251026/domains/cit.chrge.ru/public_html/telebot/dictionaries/'+str(uid), 'w'): 
            pass


@bot.message_handler(commands = ['add', 'a'])
def add_to_dictionary(message):
    word = extract_arg(message.text)
    try:
        definition = get_definition(word)
    except:
        bot.reply_to(message, 'Nothing found № Check spelling?')
    else:
        try:
            f = open("/home/a0251026/domains/cit.chrge.ru/public_html/telebot/dictionaries/%s" % str(message.from_user.id),"a+")
        except Exception as e:
            bot.reply_to(message, str(e))
            bot.reply_to(message, '№Ё Cannot write to file.')
        else:
            f.write("%s : %s \n" % (word, definition))
            f.close()
            bot.reply_to(message, '№ Your dictionary was updated.')


def get_info():
    string = ""
    word = wod.random_word(7)
    try:
        string += "№ %s\n" % word
        string += "№ %s\n" % remdict.get_definition(word)
    except:
        raise Exception
    else:
        string += "№ %s \n" % remdict.get_example_of_use(word)
        return string


def get_info_better(word):
    string = ""
    try:
        string += "№ %s \n" % word
        string += "№ %s \n" % remdict.get_definition(word)
    except:
        raise Exception
    else:
        string += "№ %s \n" % remdict.get_example_of_use(word)
        return string


def get_definition(word):
    definition = "№ " + remdict.get_definition(word)
    return definition
    

@bot.message_handler(commands=['define', 'd'])
def define(message):
    # start = timeit.default_timer()
    word = extract_arg(message.text)
    try:
        definition = get_definition(word)
        example = remdict.get_example_of_use(word)
    except:
        bot.reply_to(message, 'Not a word. Check spelling №Є')
    else:
        bot.reply_to(message, "%s\n%s " % (definition, example))
        # elapsed = timeit.default_timer() - start
        # bot.reply_to(message, "\nComplete in %f seconds" % elapsed)
    
    
@bot.message_handler(commands=['random', 'r'])
def random_word(message):
    try:
        bot.reply_to(message, get_info())
    except:
        random_word(message)


@bot.message_handler(commands=['help', 'h'])
def help_user(message):
    commands_list = """ 
    /a word or /add word - add a word to your dictionary
    /h or /help  - list all commands
    /d word or /define word - define a word
    /r or /random - returns a random word 
    """
    bot.reply_to(message, commands_list)
    

@bot.message_handler(commands=['start'])
def greet(message):
    username = str(message.from_user.first_name) + " " + str(message.from_user.last_name)
    create_dictionary(message.from_user.id)
    f = open("/home/a0251026/domains/cit.chrge.ru/public_html/telebot/stats/userlist.log","a+")
    f.write("%d %s %s \n" % (message.from_user.id, username, datetime.datetime.now()))
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
    return "№ %s %s." % (salutations[random.randint(0, len(salutations)-1)], username)


bot.infinity_polling(True)    
bot.polling()
