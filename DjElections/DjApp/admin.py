from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.DJ)
admin.site.register(models.Song)
admin.site.register(models.Elections)
admin.site.register(models.SongsInElections)