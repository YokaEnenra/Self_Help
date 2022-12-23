import string
from random import choice

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


# Create your models here.


class ErrorMessages(models.Model):
    name = models.CharField(verbose_name=_('error`s short name'), max_length=100, unique=True)
    full_text = models.CharField(verbose_name=_('error`s full text'), max_length=255)


class InfoMessages(models.Model):
    name = models.CharField(verbose_name=_('message`s short name'), max_length=100, unique=True)
    full_text = models.CharField(verbose_name=_('message`s full text'), max_length=255)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_messages_active = models.BooleanField(default=False)
    notifications_interval = models.IntegerField(default=None, null=True)
    notification_time = models.DateTimeField(default=None, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.UserProfile.save()

class Project(models.Model):
    title = models.CharField(null=False, max_length=100)
    host = models.ManyToManyField(User, related_name='host_user')
    users = models.ManyToManyField(User)
    slug = models.SlugField(null=True, unique=True, max_length=70)


def rand_slug():
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(12))


def rand_title_chars(value):
    return ''.join(choice(value) for _ in range(int(len(value)/2)))


@receiver(post_save, sender=Project)
def update_project(sender, instance, created, update_fields, **kwargs):
    if created or (update_fields is not None and instance.title in update_fields):
        instance.slug = slugify(rand_slug() + rand_title_chars(instance.title))


class Note(models.Model):
    title = models.CharField(null=True, max_length=100)
    text = models.CharField(max_length=1000, null=True)
    project_id = models.ManyToManyField(Project)
    vid_id = models.CharField(null=True, max_length=50)
    is_done = models.BooleanField(default=False)
    slug = models.SlugField(null=True, unique=True, max_length=70)


@receiver(post_save, sender=Note)
def update_note(sender, instance, created, update_fields, **kwargs):
    if created and instance.title is None:
        instance.title = InfoMessages.objects.get(name='new_note').full_text + instance.id
    if created or (update_fields is not None and instance.title in update_fields):
        instance.slug = slugify(rand_slug() + rand_title_chars(instance.title))
