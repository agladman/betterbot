from django.core.management.base import BaseCommand

from corpus.models import Sentence
from betterbot.settings import BASE_DIR, CONFIG, STATICFILES_DIRS

import os
from random import choice

from twython import Twython


class Command(BaseCommand):
    help = 'Tweets the most popular sentence from the corpus.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--with-photo',
            action='store_true',
            dest='photo',
            default=False,
            help='Adds a picture to the tweet.'
        )
    # TODO: add --promo option to tweet

    def handle(self, *args, **options):
        twitter = Twython(app_key=CONFIG['twitter']['app_key'],
                          app_secret=CONFIG['twitter']['app_secret'],
                          oauth_token=CONFIG['twitter']['oauth_token'],
                          oauth_token_secret=CONFIG['twitter']['oauth_token_secret'])

        sentence = Sentence.objects.most_popular_now()

        if options['photo']:
            try:
                media_dir = os.path.join(BASE_DIR, 'static/media')
                photos = [os.path.join(media_dir, fname) for fname in os.listdir(media_dir)]
                with open(choice(photos), 'rb') as p:
                    response = twitter.upload_media(media=p)
                twitter.update_status(status=sentence.text, media_ids=[response['media_id']])
                sentence.tweeted = True
                sentence.save()
                self.stdout.write('Tweet sent with picture.')
            except Exception as e:
                self.stdout.write('Exception blocked tweet.\n{0}'.format(e))
                pass
        else:
            try:
                twitter.update_status(status=sentence.text)
                sentence.tweeted = True
                sentence.save()
                self.stdout.write('Tweet sent.')
            except Exception as e:
                self.stdout.write('Exception blocked tweet.\n{0}'.format(e))
                pass
