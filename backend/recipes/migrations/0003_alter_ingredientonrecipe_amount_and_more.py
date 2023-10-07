# Generated by Django 4.2.5 on 2023-10-01 12:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_rename_quantity_ingredientonrecipe_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientonrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'Количество должно быть не меньше 1')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='ingredientonrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_amount', to='recipes.ingredient', verbose_name='Ингриденты'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d', verbose_name='Ссылка на картинку на сайте'),
        ),
    ]
