from django.core.management.base import BaseCommand
from corpus.models import BaseText
from betterbot.settings import BASE_DIR

import os


class Command(BaseCommand):
    help = 'Gets active lines from the corpus database and exports them to a text file.'

    def handle(self, *args, **options):
        """
        Creates a text model for the markovify library from all lines in the corpus
        that fall within the maximum age limit.
        """
        self.stdout.write('exporting corpus to text file')
        basetext = '\n'.join([x.text_str for x in BaseText.objects.all() if x.check_age()])
        with open(os.path.join(BASE_DIR, 'corpus.txt'), 'w') as f:
            f.write(basetext)
