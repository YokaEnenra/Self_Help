from modeltranslation.translator import register, TranslationOptions
from Self_Help.models import ErrorMessages, InfoMessages


@register(ErrorMessages)
class ErrorTranslationOptions(TranslationOptions):
    fields = ('full_text', )


@register(InfoMessages)
class InfoMessagesTranslationOptions(TranslationOptions):
    fields = ('full_text', )
