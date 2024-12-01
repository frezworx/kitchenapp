from django.contrib import admin

from core_app.models import Cook, DishType, Ingredient, Dish

admin.site.register(Cook)
admin.site.register(DishType)
admin.site.register(Ingredient)
admin.site.register(Dish)
