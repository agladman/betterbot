from django.core.management.base import BaseCommand

from requests import HTTPError

from corpus.utils import fetch_image


class Command(BaseCommand):
    help = 'Fetches one or more images from unsplash.com.'

    def add_arguments(self, parser):
        parser.add_argument('num_arg', type=int)

    def handle(self, *args, **options):
            num = options['num_arg'] or 1
            self.stdout.write('fetching images')
            fetched = 0
            for i in range(num):
                try:
                    if fetch_image() is True:
                        fetched += 1
                except HTTPError as e:
                    self.stdout.write(f'error fetching image: {e.response.status_code}')
            self.stdout.write(f'images fetched: {fetched}')
