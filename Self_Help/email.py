from django.conf import settings
from django.core.mail import send_mail
from django.template import loader


def send(subject, to_email, template_name, context=None, message=None,):
    template = loader.get_template(template_name)
    html_message = template.render(context)
    send_mail(subject=subject,
              message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[to_email],
              html_message=html_message)
