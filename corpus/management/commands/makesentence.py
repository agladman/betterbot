from django.core.management.base import BaseCommand

from corpus.models import Sentence


class Command(BaseCommand):
    help = 'Generates a sentence based on the current text model.'

    def handle(self, *args, **options):
        s = Sentence.create()
        s.save()
        self.stdout.write('Sentence created: {0}'.format(s.text))
