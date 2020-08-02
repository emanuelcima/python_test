from django.contrib import admin
from .models import Field, Rain


class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'hectares', 'latitude', 'longitude')
    search_fields = ('name',)

class RainAdmin(admin.ModelAdmin):
    list_display = ('field', 'date', 'millimeters')
    search_fields = ('field__name', 'date')


admin.site.register(Field, FieldAdmin)
admin.site.register(Rain, RainAdmin)
