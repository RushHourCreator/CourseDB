from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

@admin.register(Entries)
class EntriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

@admin.register(Characters)
class CharactersAdmin(admin.ModelAdmin):
    pass

@admin.register(Spells)
class SpellsAdmin(admin.ModelAdmin):
    pass

@admin.register(Locations)
class LocationsAdmin(admin.ModelAdmin):
    pass

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    pass

@admin.register(Quests)
class QuestsAdmin(admin.ModelAdmin):
    pass

@admin.register(ForumUsers)
class ForumUsersAdmin(admin.ModelAdmin):
    pass


