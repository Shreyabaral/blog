from django.contrib import admin
from .models import post, Comments
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(post)
admin.site.register(Comments)

# Register your models here.
