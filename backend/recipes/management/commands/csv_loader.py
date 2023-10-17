import csv
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в БД'

    def handle(self, *args, **kwargs):
        with open('static/data/ingredients.csv', encoding='utf8') as file:
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
