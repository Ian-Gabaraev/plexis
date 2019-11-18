# Remote dictionary module

from bs4 import BeautifulSoup
import requests
import random


web_address = 'https://www.lexico.com/en/definition/'

# This website returns 404 code if word is unrecognized
# Thus, we can filter out non-English requests to the dictionary


def is_a_word(word):
    response = requests.get('https://www.infoplease.com/dictionary/' + word)
    return response.__getattribute__('status_code') == 200 or word.isalpha()


def connect_to_dictionary(word):
    response = requests.get(web_address + word)
    if is_a_word(word) and response.__getattribute__('status_code') == 200:
        return response.content
    else:
        raise Exception('ERROR. Not a word or website is down.')


def search_dictionary(word):
    try:
        page_source = connect_to_dictionary(word)
    except Exception as e:
        # print e.message
        raise Exception('ERROR. Could not process request.')
    else:
        try:
            return BeautifulSoup(page_source, features = 'html.parser')
        except AttributeError:
            raise Exception('ERROR.Nothing found.')

        
def get_definition(word):
    try:
        soup = search_dictionary(word)
    except:
        raise Exception
    else:
        try:
            return soup.find('span', 'ind').text
        except:
            raise Exception


def get_example_of_use(word):
    try:
        soup = search_dictionary(word)
    except Exception as e:
        raise Exception
        # print e.message
    else:
        examples = [example.text for example in soup.find_all('li', 'ex')]
        return examples[random.randint(0, len(examples)-1)]


# print get_definition('kinky')
# print get_example_of_use('nihilism')