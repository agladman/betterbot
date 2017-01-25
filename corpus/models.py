from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.db import IntegrityError as IntegError1
from psycopg2 import IntegrityError as IntegError2

from betterbot.settings import CONFIG, LOGCONFIG, TEXT_MODEL_JSON_FILE
from corpus import querysets
from corpus.utils import POSifiedText

import json
import logging.config


logging.config.dictConfig(LOGCONFIG)
logger = logging.getLogger(__name__)


class BaseText(models.Model):
    """
    trying to add duplicate api_ref should raise django.db.IntegrityError
    possibly django.core.ValidationError
    """
    api_ref = models.CharField(max_length=20, unique=True)
    text_str = models.CharField(max_length=400)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    @classmethod
    def create(cls, api_ref, text_str):
        t = cls(api_ref=api_ref, text_str=text_str)
        t.save()
        return t

    def check_age(self):
        """
        :returns True if the line is under the max age limit and False if it is over:
        """
        if self.timestamp > timezone.now() - timedelta(days=CONFIG['limits']['corpus_max_age']):
            return True
        else:
            return False


class Sentence(models.Model):
    text = models.CharField(max_length=140, unique=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    appearances = models.IntegerField(default=0)
    last_appearance = models.DateTimeField(auto_now_add=False, auto_now=True)
    tweeted = models.NullBooleanField(null=True)

    objects = querysets.SentenceQuerySet.as_manager()

    @classmethod
    def create(cls):
        if CONFIG['markov-from-json']:
            with open(TEXT_MODEL_JSON_FILE, 'r') as json_file:
                model_data = json.loads(json_file.read())
            text_model = POSifiedText.from_json(model_data)
        else:
            basetext = '\n'.join([x.text_str for x in BaseText.objects.all() if x.check_age()])
            text_model = POSifiedText(basetext)     # removed state_size=2
        s = None
        while not s:
            try:
                s = cls(text=text_model.make_short_sentence(CONFIG['limits']['tweet_max_length']))
                s.save()
                logger.debug(f'sentence created: {s.text}')
                break
            except (IntegError1, IntegError2) as e:
                logger.exception(f'exception while creating sentence: {e}')
                s = None
                continue
        return s

    def set_score(self):
        self.score = self.ups - self.downs

    def win(self):
        self.ups += 1
        self.set_score()
        self.save()

    def lose(self):
        self.downs += 1
        self.set_score()
        self.save()
