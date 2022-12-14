from django.contrib import admin
from django.contrib import admin
from Self_Help.models import TestModel
from modeltranslation.admin import TranslationAdmin

# Register your models here.
@admin.register(TestModel)
class TestModelAdmin(TranslationAdmin):
    prepopulated_fields = {'tast': ('tust',)}
