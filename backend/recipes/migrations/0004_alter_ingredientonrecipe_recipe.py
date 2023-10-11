# Generated by Django 4.1.5 on 2023-10-10 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_ingredientonrecipe_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientonrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_amount', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
