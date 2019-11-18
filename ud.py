import requests
from bs4 import BeautifulSoup

ud_logo = """
    <!--
        _|_  _  _    _|. __|_. _  _  _  _
    |_|| |_)(_|| |  (_||(_ | |(_)| |(_||\/
                                        /
-->
    """

def find_a(word):
    link = 'https://www.urbandictionary.com/define.php?term=%s' %word

    response = requests.get(link)
    source = response.text.encode('utf-8').decode('ascii', 'ignore')
    soup = BeautifulSoup(source, features='html.parser')

    if not response.status_code == 404:
        definitions = soup.find_all("div", {"class": "meaning"})
        examples = soup.find_all("div", {"class": "example"})
        if len(definitions) >= 3:
            result = "%s\n🔎Definitions:\n🔵%s\n🔈Examples:\n💬%s" % (
            ud_logo,
            "\n🔵".join([definition.text for definition in definitions[:3]]),
            "\n💬".join([example.text for example in examples[:3]])
            )
        return result.replace("&apos", "'")
    else:
        return "😒 Nothing found. Check spelling?"
