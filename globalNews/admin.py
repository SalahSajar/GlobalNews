from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User, SavedArticle, Topic

admin.site.register(User, UserAdmin)
admin.site.register(SavedArticle)
admin.site.register(Topic)
