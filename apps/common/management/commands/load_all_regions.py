import json
from pathlib import Path
from django.core.management.base import BaseCommand
from core.settings import BASE_DIR
from apps.common.models import Region, Country


class Command(BaseCommand):
    help = 'Load all regions'

    def handle(self, *args, **kwargs):
        regions_file = Path(BASE_DIR / 'data/regions.json')

        if not regions_file.is_file():
            return self.stderr.write(self.style.ERROR('File regions not found'))
        
        regions_text = regions_file.read_text(encoding='utf-8-sig')
        regions = json.loads(regions_text)
        country = Country.objects.get(name='Uzbekistan', code='UZ')

        for region in regions:
            Region.objects.get_or_create(name=region['name_uz'], country=country)
        
        return self.stdout.write(self.style.SUCCESS('All regions are loaded succesfully'))