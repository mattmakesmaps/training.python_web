__author__ = 'matt'
from django.contrib import admin
from models import *

class EntryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Entries, EntryAdmin)
