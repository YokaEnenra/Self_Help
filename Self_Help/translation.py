from modeltranslation.translator import register, TranslationOptions
from Self_Help.models import TestModel, ErrorMessages, InfoMessages


@register(TestModel)
class TestModelTranslationOptions(TranslationOptions):
    fields = ('tast', 'tust')


@register(ErrorMessages)
class ErrorTranslationOptions(TranslationOptions):
    fields = ('full_text', )


@register(InfoMessages)
class InfoMessagesTranslationOptions(TranslationOptions):
    fields = ('full_text', )
