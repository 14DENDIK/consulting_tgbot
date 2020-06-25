from django.contrib import admin

from .models import TelegramUser, Application, Country, FAQ

admin.site.register(TelegramUser)
admin.site.register(Application)
admin.site.register(Country)
admin.site.register(FAQ)
