from django.contrib import admin
from .models import CarMake, CarModel


# Inline admin for CarModel
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of empty forms to display


# Admin class for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'year', 'make')
    list_filter = ('make', 'type')
    search_fields = ('name', 'make__name')


# Admin class for CarMake
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    inlines = [CarModelInline]  # Include CarModel inline admin


# Register models with their respective admins
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
