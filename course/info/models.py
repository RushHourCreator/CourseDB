from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import IntegerRangeField

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _



class Entries(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Characters(models.Model):
    entry = models.OneToOneField(Entries, primary_key=True, on_delete=models.CASCADE)
    strength = models.PositiveSmallIntegerField()
    will = models.PositiveSmallIntegerField()
    influence = models.PositiveIntegerField()
    observation = models.PositiveIntegerField()
    lore = models.PositiveIntegerField()
    CHOICES = (
        ('Hybrid', 'Hybrid'),
        ('Human', 'Human'),
    )
    loyalty = models.CharField(max_length=300, choices = CHOICES)

    # loyalty = models.BooleanField()
    # if models.BooleanField() :
    #     is_friendly = "Human"
    # else:
    #     is_friendly = "Hybrid"


    def __str__(self):
        return self.entry.__str__()
    
    def get_absolute_url(self):
        return reverse('info:character_detail', kwargs={'slug': self.entry.slug})

class Spells(models.Model):
    entry = models.OneToOneField(Entries, primary_key=True, on_delete=models.CASCADE)
    effect = models.TextField()

    def __str__(self):
        return self.entry.__str__()

    def get_absolute_url(self):
        return reverse('info:spell_detail', kwargs={'slug': self.entry.slug})

class Locations(models.Model):
    entry = models.OneToOneField(Entries, primary_key=True, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    effect = models.TextField()

    def __str__(self):
        return self.entry.__str__()

    def get_absolute_url(self):
        return reverse('info:location_detail', kwargs={'slug': self.entry.slug})

class Items(models.Model):
    entry = models.OneToOneField(Entries, primary_key=True, on_delete=models.CASCADE)
    effect = models.TextField()

    def __str__(self):
        return self.entry.__str__()

    def get_absolute_url(self):
        return reverse('info:item_detail', kwargs={'slug': self.entry.slug})

class Quests(models.Model):
    entry = models.OneToOneField(Entries, primary_key=True, on_delete=models.CASCADE)
    crisis = models.TextField()
    target_number = models.PositiveIntegerField()
    items = models.ManyToManyField(Items, blank=True)

    def __str__(self):
        return self.entry.__str__()

    def get_absolute_url(self):
        return reverse('info:quest_detail', kwargs={'slug': self.entry.slug})




class ForumUsers(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user'), related_name='forumusers', on_delete=models.CASCADE)
    read_only = models.BooleanField(verbose_name=_('read_only'))

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_forum_user(sender, instance, created, **kwargs):
    if created:
        ForumUsers.objects.create(user=instance, read_only=False)

@receiver(post_save, sender=User)
def save_forum_user(sender, instance, **kwargs):
    instance.forumusers.save()

# class Comments(models.Model):
#     entry = models.ForeignKey(models.Entries, verbose_name=_('entry'), on_delete=models.CASCADE)
#     user = models.ForeignKey(ForumUsers, verbose_name=_('user'), on_delete=models.CASCADE)
#     publication_date = models.DateTimeField(verbose_name=_('publication_date'), auto_now_add=True)
#     content = models.TextField(verbose_name=_('content'))