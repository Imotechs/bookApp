from django.contrib import admin
from .models import Profile,Books,CheckedBook
# Register your models here.
admin.site.register(Profile)
admin.site.register(Books)
admin.site.register(CheckedBook)