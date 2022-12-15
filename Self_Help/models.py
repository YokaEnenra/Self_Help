from django.db import models
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
