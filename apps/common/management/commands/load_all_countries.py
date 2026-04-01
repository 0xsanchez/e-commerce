import json
from pathlib import Path
from django.core.management.base import BaseCommand
from core.settings import BASE_DIR
from apps.common.models import Country


class Command(BaseCommand):
    help = 'Load all countries'

    def handle(self, *args, **kwargs):
        countries_file = Path(BASE_DIR / 'data/countries.json')

        if not countries_file.is_file():
            return self.stderr.write(self.style.ERROR('File countries.json not found'))
        
        countries_text = countries_file.read_text(encoding='utf-8-sig')
        countries = json.loads(countries_text)

        for country in countries:
            Country.objects.get_or_create(name=country['name_uz'], code=country['code'])
        
        return self.stdout.write(self.style.SUCCESS('All countries are loaded succesfully'))