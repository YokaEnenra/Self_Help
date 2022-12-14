from modeltranslation.translator import register, TranslationOptions
from Self_Help.models import TestModel


@register(TestModel)
class TestModelTranslationOptions(TranslationOptions):
    fields = ('tast', 'tust')
