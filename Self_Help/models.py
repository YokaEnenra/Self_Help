from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


# Create your models here.
class TestModel(models.Model):
    tast = models.CharField(verbose_name=_('tast'), max_length=120)
    test = models.IntegerField(verbose_name=_('test'))
    tust = models.CharField(verbose_name=_('tust'), max_length=120)

    def __str__(self):
        return self.tast


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
    user_id = models.ManyToManyField(User)


class Note(models.Model):
    title = models.CharField(null=True, max_length=100)
    text = models.CharField(max_length=1000)
    project_id = models.ManyToManyField(Project)


@receiver(post_save, sender=Note)
def create_note(sender, instance, created, **kwargs):
    if created and sender.title is None:
        sender.title = InfoMessages.objects.get(name='new_note').full_text + sender.id
