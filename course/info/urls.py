from django.urls import path

import info.views as iv

app_name = 'info'
app_name = 'forum'
urlpatterns = [
    path('export-clients-xlsx/', iv.get_characters_xlsx, name='characters_xlsx'),
    path('export-items-xlsx/', iv.get_items_xlsx, name='items_xlsx'),
    path('export-locations-xlsx/', iv.get_locations_xlsx, name='locations_xlsx'),
    path('export-quests-xlsx/', iv.get_quests_xlsx, name='quests_xlsx'),
    path('export-spells-xlsx/', iv.get_spells_xlsx, name='spells_xlsx'),

    path('register/', iv.RegisterUser.as_view(), name='register'),
    path('login/', iv.LoginUser.as_view(), name='login'),
    path('logout/', iv.logout_user, name='logout'),
    path('', iv.home, name='home'),
    path('characters/', iv.characters, name='characters'),
    path('character/<slug:slug>', iv.character_detail, name='character_detail'),
    path('spells/', iv.spells, name='spells'),
    path('spell/<slug:slug>', iv.spell_detail, name='spell_detail'),
    path('locations/', iv.locations, name='locations'),
    path('location/<slug:slug>', iv.location_detail, name='location_detail'),
    path('items/', iv.items, name='items'),
    path('item/<slug:slug>', iv.item_detail, name='item_detail'),
    path('quests/', iv.quests, name='quests'),
    path('quest/<slug:slug>', iv.quest_detail, name='quest_detail'),
]