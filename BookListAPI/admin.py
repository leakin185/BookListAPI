from django.contrib import admin
from .models import Bookitem, Category

# Register your models here.
admin.site.register(Bookitem)
admin.site.register(Category)
