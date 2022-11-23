# Generated by Django 4.1.3 on 2022-11-15 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DishCountry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DishRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_dish', models.CharField(max_length=50)),
                ('ingredients', models.JSONField()),
                ('spices', models.JSONField(null=True)),
                ('from_country', models.IntegerField()),
                ('dish_type', models.CharField(choices=[('Appetizer', 'Appetizer'), ('Salad', 'Salad'), ('Soup', 'Soup'), ('Garnish', 'Garnish'), ('Main Dish', 'Main Dish'), ('Meat Dish', 'Meat Dish'), ('Poultry Dish', 'Poultry Dish'), ('Seafood Dish', 'Seafood Dish'), ('Snack', 'Snack'), ('Sauce', 'Sauce'), ('Dessert', 'Dessert'), ('Beverage', 'Beverage')], default='Appetizer', max_length=15)),
                ('method_preparation', models.CharField(choices=[('Combine', 'Combine'), ('Slicing', 'Slicing'), ('Fry', 'Fry'), ('Brew', 'Brew'), ('Steamed', 'Steamed'), ('BBQ-Grill', 'Barbecue Grill'), ('Braised', 'Braised'), ('Baked', 'Baked')], default='Combine', max_length=15)),
                ('time_preparation', models.TimeField()),
                ('difficulty_recipe', models.IntegerField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_dish', models.IntegerField()),
                ('text_review', models.TextField()),
                ('rate_recipe', models.IntegerField(max_length=1)),
            ],
        ),
    ]