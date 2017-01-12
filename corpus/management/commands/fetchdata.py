from django.core.management.base import BaseCommand
from django.db import IntegrityError

import praw

from betterbot.settings import CONFIG
from corpus.models import BaseText


class Command(BaseCommand):
    help = 'Populates the corpus database with data from the Reddit API.'
    reddit = praw.Reddit(user_agent=CONFIG['reddit']['my_user_agent'],
                         client_id=CONFIG['reddit']['my_client_id'],
                         client_secret=CONFIG['reddit']['my_client_secret'],
                         username=CONFIG['reddit']['my_username'],
                         password=CONFIG['reddit']['my_password'])

    def handle(self, *args, **options):
        self.stdout.write('fetching data from Reddit API')
        for sub in CONFIG['reddit']['subreddits']:
            self.stdout.write('-- r/{0}'.format(sub))
            subreddit = self.reddit.subreddit(sub)
            for p in subreddit.hot(limit=CONFIG['reddit']['fetch_limit']):
                if not p.stickied:
                    try:
                        x = BaseText.create(p.id, p.title)
                        x.save()
                    except IntegrityError:
                        pass
        self.stdout.write('operation complete')
