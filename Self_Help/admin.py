from django.contrib import admin
from Self_Help.models import TestModel, ErrorMessages, InfoMessages
from modeltranslation.admin import TranslationAdmin


# Register your models here.
@admin.register(TestModel)
class TestModelAdmin(TranslationAdmin):
    prepopulated_fields = {'tast': ('tust',)}


@admin.register(ErrorMessages)
class ErrorMessageAdmin(TranslationAdmin):
    prepopulated_fields = {'name': ('full_text',)}
    list_display = ('name', )


@admin.register(InfoMessages)
class InfoMessagesAdmin(TranslationAdmin):
    list_display = ('name', )
