from django.contrib import admin
from .models import User,FoodData,ActivityData

admin.site.register(User)
admin.site.register(FoodData)
admin.site.register(ActivityData)

