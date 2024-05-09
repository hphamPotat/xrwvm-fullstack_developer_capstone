from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.
# Register models here
admin.site.register(CarModel)
admin.site.register(CarMake)
