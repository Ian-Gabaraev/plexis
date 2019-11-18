import requests
import random
import remdict
from bs4 import BeautifulSoup

web_address = 'https://plato.stanford.edu/cgi-bin/encyclopedia/random'


def connect_to_plato():
    try:
        response = requests.get(web_address)
    except:
        raise Exception
    else:
        source = response.content
        return BeautifulSoup(source, features='html.parser')



def random_word(size):
    try:
        soup = connect_to_plato()
    except:
        raise Exception
    else:
        preamble = soup.find('div', {'id': 'preamble'})
        child = preamble.find("p" , recursive=False).text
        list_of_words = [word.strip('\n,.():"\'') for word in child.split(
            ' ') if len(word) >= size and word.isalpha()]
        try:
            return list_of_words[random.randint(0, len(list_of_words)-1)]
        except ValueError:
            raise Exception('ERROR.Size is too big.')


# while True:
#     rm = random_word(7)
#     print rm
#     print remdict.get_definition(rm)
#     print remdict.get_example_of_use(rm)