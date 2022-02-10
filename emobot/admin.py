from django.contrib import admin

from emobot.models import Person,SessionTable,EmotionTable

# Register your models here.
admin.site.register(Person)
admin.site.register(SessionTable)
admin.site.register(EmotionTable)


