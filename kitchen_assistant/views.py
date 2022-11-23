import json
import string
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from kitchen_assistant import models
from django.db import connection



def dish_filter(request):
    if request.method == "GET":
        dish_country = []
        dish_country_objs = models.DishCountry.objects.all()
        for itm in range(len(dish_country_objs)):
            dish_country.append(dish_country_objs[itm].name_country)
        return render(request, 'dish_filter.html', context={'dish_country': dish_country})

    if request.method == 'POST':
        cursor = connection.cursor()
        search_list = []

        if request.POST.get('country') != 'ALL':
            search_list.append(f"name_country='{request.POST.get('country')}'")
        if request.POST.get('dish_type') != 'ALL':
            search_list.append(f"dish_type='{request.POST.get('dish_type')}'")
        if request.POST.get('method') != 'ALL':
            search_list.append(f"method_preparation='{request.POST.get('method')}'")
        if request.POST.get('difficulty') != 'Any complexity':
            search_list.append(f"difficulty_recipe={request.POST.get('difficulty')}")
        if request.POST.get('time_prep') != 'Anytime':
            search_list.append(f"time_preparation<={request.POST.get('time_prep')}")

        if search_list:
            database_filter_str = f" WHERE {' and '.join(search_list)}"
        else:
            database_filter_str = ""

        database_query = """SELECT name_dish, 
                                   dish_type, 
                                   method_preparation,
                                   time_preparation, 
                                   difficulty_recipe, 
                                   name_country
                            FROM kitchen_assistant_dishrecipe AS recipe 
                                JOIN kitchen_assistant_dishcountry AS dish_country
                                    ON recipe.from_country == dish_country.id"""

        cursor.execute(database_query + database_filter_str)

        result_query = cursor.fetchall()

        if result_query:
            found_recipe_list = [{'<br>Dish name': f"<a href='dish_info/{itm[0]}' >{itm[0]}</a>",
                                  'Dish type': itm[1],
                                  'Method Dish preparation': itm[2],
                                  'Time preparation dish': itm[3],
                                  'Difficulty recipe': itm[4],
                                  'Country dish': itm[5]} for itm in result_query]

            return HttpResponse(found_recipe_list)
        else:
            return HttpResponse('Recipes not found')


def find_by_ingredient(request):
    if request.method == 'GET':
        return render(request, 'find_dish_by_ingredient.html')

    if request.method == 'POST':
        cursor = connection.cursor()
        list_ingredients_query = []
        list_for_answer = []

        list_user_ingredient = [request.POST.get('ingredient_1'),
                                request.POST.get('ingredient_2'),
                                request.POST.get('ingredient_3')]

        for ingredient in list_user_ingredient:
            for symbol in ingredient:
                if symbol in string.digits or symbol in string.punctuation:
                    break
            else:
                continue
            return HttpResponse(f'{ingredient} - Punctuation marks and/or numbers in the ingredient are found')

        for ingredient in list_user_ingredient:
            if ingredient != '':
                list_ingredients_query.append(f"instr(ingredients, '{ingredient.lower()}')")
                list_for_answer.append(ingredient)

        if list_ingredients_query:
            database_filter_str = f" WHERE {' and '.join(list_ingredients_query)}"
        else:
            return HttpResponse("Empty fields. Enter at least one ingredient."
                                "Try again:  <a href='find_dish_by_ingredient'>SEARCH BY INGREDIENT</a>"
                                "<br>Find a recipe by filter"
                                "<br><a href='find_dish'>SEARCH FOR A DISH BY FILTER</a>")

        database_query = """SELECT name_dish,
                                   ingredients,
                                   spices
                            FROM kitchen_assistant_dishrecipe"""

        cursor.execute(database_query + database_filter_str)

        result_query = cursor.fetchall()

        if result_query:
            found_recipe_list = [{'<br>Dish name': f"<a href='dish_info/{itm[0]}' >{itm[0]}</a>",
                                  'Ingredients': itm[1],
                                  'Spices': itm[2]} for itm in result_query]

            return HttpResponse([f'Find a list of recipes with these ingredients:{[x for x in list_for_answer]}',
                                 found_recipe_list])
        else:
            return HttpResponse("Enter at least one ingredient."
                                "Or it's spelled wrong."
                                "Try again: , <a href='find_dish_by_ingredient'>SEARCH BY INGREDIENT</a>"
                                "<br>Find a recipe by filter"
                                "<br><a href='find_dish'>SEARCH FOR A DISH BY FILTER</a>")


def dish_info(request, dish_name):
    cursor = connection.cursor()

    database_query = f"""SELECT name_dish, 
                                dish_type, 
                                method_preparation,
                                ingredients, 
                                spices,
                                sequence_operations, 
                                time_preparation, 
                                difficulty_recipe
                         FROM kitchen_assistant_dishrecipe as recipe
                                     WHERE name_dish='{dish_name}'"""

    cursor.execute(database_query)
    result_query_dish = cursor.fetchall()

    if result_query_dish:
        select_dish = [{'Dish name': itm[0],
                        '<br>Dish type': itm[1],
                        '<br>Method dish preparation': itm[2],
                        '<br>Ingredients dish': itm[3],
                        '<br>Spices dish': itm[4],
                        '<br>Instructions': itm[5].replace('\n', ' '),
                        '<br>Time dish preparation': itm[6],
                        '<br>Difficulty recipe': itm[7]} for itm in result_query_dish]

        return HttpResponse([select_dish, f"<br>REad all review for this recipe - "
                             f"<a href='review/{select_dish[0]['Dish name']}'>Show review</a>",
                             f"<br>Write review for this recipe - "
                             f"<a href='review_add/{select_dish[0]['Dish name']}'>Write review</a>"
                             f"<br><br>Edit Recipe(only for admin)"
                             f"<a href='correcting/{select_dish[0]['Dish name']}'>Edit recipe</a>"])
    else:
        return HttpResponse('Dish with that name was not found. Try to spell the name correctly')


def add_dish_recipe(request):
    if request.user.has_perm('add_dish_recipe'):
        if request.method == "GET":
            dish_country = []
            dish_country_objs = models.DishCountry.objects.all()
            for itm in range(len(dish_country_objs)):
                dish_country.append(dish_country_objs[itm].name_country)
            dish_country.remove('ALL')
            return render(request, 'add_recipe_dish.html', context={'dish_country': dish_country,
                                                                    'range_difficulty': range(1, 11)})

        if request.method == "POST":
            dish_name = request.POST.get('dish_name')

            dish_ingredient = dict()
            for i in range(1, 16):
                select_ingredient = request.POST.get(f"ingredient_{i}")
                select_ingredient_quantity = request.POST.get(f"quantity_{i}")
                if select_ingredient != '':
                    dish_ingredient[select_ingredient.lower()] = select_ingredient_quantity

            dish_spices = dict()
            for i in range(1, 11):
                select_spice = request.POST.get(f"spice_{i}")
                select_spice_quantity = request.POST.get(f"quantity_spice_{i}")
                if select_spice != '':
                    dish_spices[select_spice.lower()] = select_spice_quantity

            id_country_from_dish = models.DishCountry.objects.get(name_country=request.POST.get('country')).id
            dish_type = request.POST.get('dish_type')
            method_preparation = request.POST.get('method')
            difficulty_recipe = request.POST.get('difficulty_cooking')
            sequence_operations = request.POST.get('instruction_cooking')
            time_preparation = request.POST.get('cooking_time')

            new_dish_record = models.DishRecipe(name_dish=dish_name,
                                                ingredients=dish_ingredient,
                                                spices=dish_spices,
                                                from_country=id_country_from_dish,
                                                dish_type=dish_type,
                                                method_preparation=method_preparation,
                                                difficulty_recipe=difficulty_recipe,
                                                sequence_operations=sequence_operations,
                                                time_preparation=time_preparation)
            new_dish_record.save()

            return HttpResponse('Great, a new recipe has been added')
    else:
        return HttpResponse('You do not have access to add recipes. Contact customer service')


def correcting_recipe(request, dish_name):
    if request.method == 'GET':
        if request.user.is_superuser:
            cursor = connection.cursor()

            database_query = f"""SELECT id,
                                        name_dish, 
                                        ingredients, 
                                        spices,
                                        from_country,
                                        dish_type, 
                                        method_preparation,
                                        difficulty_recipe,
                                        sequence_operations, 
                                        time_preparation
                                 FROM kitchen_assistant_dishrecipe as recipe
                                         WHERE name_dish='{dish_name}'"""

            cursor.execute(database_query)
            result_query = cursor.fetchall()

            recipe_data = {'id': result_query[0][0],
                           'name_dish': result_query[0][1],
                           'ingredients': result_query[0][2],
                           'spices': result_query[0][3],
                           'from_country': result_query[0][4],
                           'dish_type': result_query[0][5],
                           'method_preparation': result_query[0][6],
                           'difficulty_recipe': result_query[0][7],
                           'sequence_operations': result_query[0][8],
                           'time_preparation': result_query[0][9]}


            return render(request, 'correcting_recipe.html', context={'recipe_data': recipe_data})
        else:
            return HttpResponse('You are not admin :)')

    if request.method == 'POST':
        ingredients = json.loads(request.POST.get('ingredients'))
        spices = json.loads(request.POST.get('spices'))

        change_recipe = models.DishRecipe.objects.get(name_dish=dish_name)

        change_recipe.id = request.POST.get('id')
        change_recipe.name_dish = request.POST.get('name_dish')
        change_recipe.ingredients = ingredients
        change_recipe.spices = spices
        change_recipe.from_country = request.POST.get('from_country')
        change_recipe.dish_type = request.POST.get('dish_type')
        change_recipe.method_preparation = request.POST.get('method_preparation')
        change_recipe.difficulty_recipe = request.POST.get('difficulty_recipe')
        change_recipe.sequence_operations = request.POST.get('sequence_operations')
        change_recipe.time_preparation = request.POST.get('time_preparation')

        change_recipe.save()
    return HttpResponse('Successfully. the recipe has been changed.')


def dish_review(request, dish_name):
    cursor = connection.cursor()

    database_query = f"""SELECT name_dish,
                                text_review,
                                rate_recipe,
                                record_date
                             FROM kitchen_assistant_dishrecipe as recipe
                             JOIN kitchen_assistant_reviewrecipe as review
                                ON recipe.id == review.id_dish
                                     WHERE name_dish='{dish_name}'"""

    cursor.execute(database_query)
    result_query_review = cursor.fetchall()

    if result_query_review:
        list_review = [{'Dish name': itm[0],
                        'Review text': itm[1],
                        'Recipe rate': itm[2],
                        'Date created review': itm[3]} for itm in result_query_review]

        return HttpResponse(list_review)

    else:
        return HttpResponse('Not found review about this recipe')


def add_dish_review(request, dish_name):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'add_review.html', context={'range_rate': range(1, 11)})

        if request.method == 'POST':
            actual_date = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
            id_dish = models.DishRecipe.objects.get(name_dish=dish_name).id
            new_review = models.ReviewRecipe(text_review=request.POST.get('user_review'),
                                             rate_recipe=request.POST.get('user_rate'),
                                             id_dish=id_dish,
                                             record_date=actual_date)
            new_review.save()

            return HttpResponse('Great. Your review has been added')

    return HttpResponse('You must log in')


def user_authorization(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'user_login.html')

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('User is login')
            else:
                return HttpResponse('User not found / Wrong password or username. '
                                    '<br><a href="login" > Try again </a>'
                                    '<br><a href="registration" > Register new user </a>')
    else:
        return HttpResponse('<a href="logout" > Logout</a>', )


def user_registration(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'user_registration.html')

        if request.method == 'POST':
            user = User.objects.create_user(username=request.POST.get('username'),
                                            password=request.POST.get('password'),
                                            email=request.POST.get('email'),
                                            first_name=request.POST.get('first_name'),
                                            last_name=request.POST.get('last_name'))
            user.save()
            return HttpResponse('User is registered')
    else:
        return HttpResponse('<a href="logout" > Logout</a>')


def logout_user(request):
    logout(request)
    return redirect('/login')
