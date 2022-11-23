from django.db import models


class DishCountry(models.Model):
    name_country = models.CharField(max_length=50, null=False)


class DishRecipe(models.Model):
    name_dish = models.CharField(max_length=50, null=False)
    ingredients = models.JSONField(null=False)
    spices = models.JSONField(null=True)
    from_country = models.IntegerField()

    class DishType(models.TextChoices):
        appetizer = 'Appetizer'
        salad = 'Salad'
        soup = 'Soup'
        garnish = 'Garnish'
        main_dish = 'Main Dish'
        meat_dish = 'Meat Dish'
        poultry_dish = 'Poultry Dish'
        seafood_dish = 'Seafood Dish'
        snack = 'Snack'
        sauce = 'Sauce'
        dessert = 'Dessert'
        beverage = 'Beverage'

    dish_type = models.CharField(
        max_length=15,
        choices=DishType.choices,
        default=DishType.appetizer)

    class MethodPreparation(models.TextChoices):
        combine = 'Combine'
        slicing = 'Slicing'
        fry = 'Fry'
        brew = 'Brew'
        steamed = 'Steamed'
        barbecue_grill = 'BBQ-Grill'
        braised = 'Braised'
        baked = 'Baked'

    method_preparation = models.CharField(
        max_length=15,
        choices=MethodPreparation.choices,
        default=MethodPreparation.combine)

    time_preparation = models.IntegerField()
    difficulty_recipe = models.IntegerField()
    sequence_operations = models.TextField()


class ReviewRecipe(models.Model):
    id_dish = models.IntegerField(null=False)
    text_review = models.TextField()
    rate_recipe = models.IntegerField()
    record_date = models.TextField(null=False)
