import django_filters
from django_filters import NumberFilter

from .models import *

class CharactersFilter(django_filters.FilterSet):
    class Meta:
        model = Characters
        fields = '__all__'
        #exclude = ['entry']

class SpellsFilter(django_filters.FilterSet):
    class Meta:
        model = Spells
        fields = '__all__'
        #exclude = ['entry']

class LocationsFilter(django_filters.FilterSet):
    #start_level = NumberFilter(field_name='levels', lookup_expr='contains')
    class Meta:
        model = Locations
        fields = '__all__'
        #exclude = ['entry', 'levels']

class ItemsFilter(django_filters.FilterSet):
    class Meta:
        model = Items
        fields = '__all__'
        #exclude = ['entry']

class QuestsFilter(django_filters.FilterSet):
    class Meta:
        model = Quests
        fields = '__all__'
        #exclude = ['entry']
