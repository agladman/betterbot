import markovify
import nltk
import os
from random import randint
import re
import requests
import uuid

from betterbot.settings import STATICFILES_DIRS


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


def fetch_image():
    image_filename = 'media/{0}.jpg'.format(uuid.uuid4().hex)
    r = requests.get(f'https://source.unsplash.com/category/technology/800x600?sig={randint(1, 999)}', stream=True)
    if r.status_code == 200:
        try:
            if int(r.headers['content-length']) < 3145728:
                with open(os.path.join(STATICFILES_DIRS[0], image_filename), 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                return True
        except KeyError:
            pass
    return False
