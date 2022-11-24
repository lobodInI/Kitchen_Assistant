from django.urls import path
from . import views


app_name = 'cookery'

urlpatterns = [
    path('', views.main_page),
    path('find_dish', views.dish_filter, name='dish_filter'),
    path('find_dish_by_ingredient', views.find_by_ingredient, name='recipe_by_ingredient'),
    path('add_dish', views.add_dish_recipe, name='add_dish_recipe'),
    path('dish_info/<dish_name>', views.dish_info, name='dish_info'),
    path('dish_info/correcting/<dish_name>', views.correcting_recipe, name='correcting_recipe'),
    path('dish_info/review/<dish_name>', views.dish_review, name='dish_review'),
    path('dish_info/review_add/<dish_name>', views.add_dish_review, name='add_dish_review')
]
