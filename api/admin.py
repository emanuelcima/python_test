from django.contrib import admin
from .models import Field, Rain

admin.site.register((Field, Rain))
