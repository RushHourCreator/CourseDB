from django.shortcuts import get_object_or_404, render
from .filters import *
from .models import *

import io
import xlsxwriter
from django.http import HttpResponse

import sender as sender
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View



from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



def get_xlsx(request, model, columns, ws_name):
    output = io.BytesIO()

    filename = f'current-report.xlsx'
    workbook = xlsxwriter.Workbook(output, {'in_memory': True, 'default_date_format': 'dd/mm/yy',
                                            'time_format': 'hh:mm:ss'})
    worksheet = workbook.add_worksheet(ws_name)

    row_num = 0
    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num])

    print(field for field in columns)
    rows = model.objects.all().order_by(columns[0]).values_list(*columns)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, row[col_num])

    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    output.close()

    return response



def get_characters_xlsx(request):
    columns = ['entry', 'strength', 'will', 'influence', 'observation', 'lore', 'loyalty']
    return get_xlsx(request, Characters, columns, ws_name='Персонажи')

def get_items_xlsx(request):
    columns = ['entry', 'effect']
    return get_xlsx(request, Items, columns, ws_name='Карты предметов')

def get_spells_xlsx(request):
    columns = ['entry', 'effect']
    return get_xlsx(request, Spells, columns, ws_name='Карты заклинаний')

def get_quests_xlsx(request):
    columns = ['entry', 'crisis', 'target_number', 'items']
    return get_xlsx(request, Quests, columns, ws_name='Карты мифов')

def get_locations_xlsx(request):
    columns = ['entry', 'number', 'effect']
    return get_xlsx(request, Locations, columns, ws_name='Локации')




def home(request):
    return render(request, 'info/home.html')

def characters(request):
    characters = Characters.objects.all()

    myFilter = CharactersFilter(request.GET, queryset=characters)
    characters = myFilter.qs

    context = {'myFilter': myFilter, 'characters': characters, 'title': 'Персонажи - UnfathomableDB'}
    return render(request, 'info/characters.html', context)

def character_detail(request, slug):
    entry = get_object_or_404(Entries, slug=slug)
    character = get_object_or_404(Characters, entry=entry)
    context = {
        'character': character,
    }
    return render(request, 'info/character_detail.html', context)

def spells(request):
    spells = Spells.objects.all()

    myFilter = SpellsFilter(request.GET, queryset=spells)
    spells = myFilter.qs

    context = {'myFilter': myFilter, 'spells': spells, 'title': 'Карты заклинаний - UnfathomableDB'}
    return render(request, 'info/spells.html', context)

def spell_detail(request, slug):
    entry = get_object_or_404(Entries, slug=slug)
    spell = get_object_or_404(Spells, entry=entry)
    context = {
        'spell': spell,
    }
    return render(request, 'info/spell_detail.html', context)

def locations(request):
    locations = Locations.objects.all()

    myFilter = LocationsFilter(request.GET, queryset=locations)
    locations = myFilter.qs

    context = {'myFilter': myFilter, 'locations': locations, 'title': 'Локации корабля - UnfathomableDB'}
    return render(request, 'info/locations.html', context)

def location_detail(request, slug):
    entry = get_object_or_404(Entries, slug=slug)
    location = get_object_or_404(Locations, entry=entry)
    context = {
        'location': location,
    }
    return render(request, 'info/location_detail.html', context)

def items(request):
    items = Items.objects.all()

    myFilter = ItemsFilter(request.GET, queryset=items)
    items = myFilter.qs

    context = {'myFilter': myFilter, 'items': items, 'title': 'Карты предметов - UnfathomableDB'}
    return render(request, 'info/items.html', context)

def item_detail(request, slug):
    entry = get_object_or_404(Entries, slug=slug)
    item = get_object_or_404(Items, entry=entry)
    context = {
        'item': item,
    }
    return render(request, 'info/item_detail.html', context)

def quests(request):
    quests = Quests.objects.all()

    myFilter = QuestsFilter(request.GET, queryset=quests)
    quests = myFilter.qs

    context = {'myFilter': myFilter, 'quests': quests, 'title': 'Карты мифов - UnfathomableDB'}
    return render(request, 'info/quests.html', context)

def quest_detail(request, slug):
    entry = get_object_or_404(Entries, slug=slug)
    quest = get_object_or_404(Quests, entry=entry)
    context = {
        'quest': quest,
    }
    return render(request, 'info/quest_detail.html', context)


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'forum/register.html'
    success_url = reverse_lazy('forum:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация - UnfathomableDB'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('info:home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'forum/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход - UnfathomableDB'
        return context


def logout_user(request):
    logout(request)
    return redirect('forum:login')

