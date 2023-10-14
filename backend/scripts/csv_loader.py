import csv

from recipes.models import Ingredient


def run():
    with open('static/data/ingredients.csv', encoding='utf8') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        Ingredient.objects.all().delete()
        for row in reader:
            print(row)
            ingredients = Ingredient(
                name=row[0],
                meashurement_unit=row[1]
            )
            ingredients.save()

    print('Загрузка в БД прошла успешно')
