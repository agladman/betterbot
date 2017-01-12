from django.core.management.base import BaseCommand

import json
import markovify

from betterbot.settings import TEXT_MODEL_JSON_FILE
from corpus.models import BaseText


class Command(BaseCommand):
    help = 'Creates a new text model for the markovify library and exports it to JSON.'

    def handle(self, *args, **options):
        """
        Creates a text model for the markovify library from all lines in the corpus
        that fall within the maximum age limit.
        """
        self.stdout.write('exporting text model')
        basetext = '\n'.join([x.text_str for x in BaseText.objects.all() if x.check_age()])

        # text_model = POSifiedText(basetext, state_size=3)
        text_model = markovify.Text(basetext, state_size=3)
        model_json = text_model.to_json()

        with open(TEXT_MODEL_JSON_FILE, 'w') as json_file:
            json_file.write(json.dumps(model_json))

        self.stdout.write('text model exported')
