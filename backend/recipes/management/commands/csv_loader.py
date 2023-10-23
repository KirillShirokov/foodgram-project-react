import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в БД'

    def handle(self, *args, **kwargs):
        file_path = (
            settings.BASE_DIR / 'static_data' / 'data' / 'ingredients.csv')
        with open(file_path, encoding='utf8') as file:
            reader = csv.reader(file, delimiter=',')
            Ingredient.objects.all().delete()
            ingredients = []
            for row in reader:
                name, meashurement_unit = row
                ingredients.append(Ingredient(
                    name=name,
                    meashurement_unit=meashurement_unit))
            Ingredient.objects.bulk_create(ingredients)

        print('Загрузка в БД прошла успешно')
