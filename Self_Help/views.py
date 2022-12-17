from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView

from Self_Help.email import send
from Self_Help.models import TestModel, ErrorMessages, InfoMessages

USER_MODEL = get_user_model()


# Create your views here.
class TestModelView(ListView):
    model = TestModel
    template_name = "test.html"


class StandardPage(View):
    def get(self, request):
        return redirect(reverse_lazy('home'))


class HomePage(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            return render(request, 'signin_home.html', context={
                'username': username,
            })
        return render(request, 'homepage.html')


class SignUp(View):
    def get(self, request, short_error_message=None):
        return render(request, "signup.html", context={
            'error_message': request.session.get('error_message'),
            'short_error_message': short_error_message})

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if USER_MODEL.objects.filter(username=username).exists():
            request.session['error_message'] = ErrorMessages.objects.get(name='wrong_username').full_text
            return redirect(reverse_lazy(
                'sign_up_with_error',
                kwargs={'short_error_message': ErrorMessages.objects.get(name='wrong_username').name}))
        if USER_MODEL.objects.filter(email=email).exists():
            request.session['error_message'] = ErrorMessages.objects.get(name='wrong_email').full_text
            return redirect(reverse_lazy(
                'sign_up_with_error',
                kwargs={'short_error_message': ErrorMessages.objects.get(name='wrong_email').name}))
        user = USER_MODEL.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False)
        send(subject=InfoMessages.objects.get(name='vrfy').full_text,
             to_email=user.email,
             template_name='verification_email.html',
             context={'subject': f"{InfoMessages.objects.get(name='hi').full_text} {user.username}.",
                      'link': reverse_lazy('verify_account', kwargs={
                          'uid': urlsafe_base64_encode(force_bytes(user.id)),
                          'token': default_token_generator.make_token(user)}),
                      'request': request})
        return HttpResponse(f"{InfoMessages.objects.get(name='hi').full_text} {user.username}.\n"
                            f"{InfoMessages.objects.get(name='acc_created').full_text} ")


def verify_account(request, uid, token):
    try:
        user = USER_MODEL.objects.get(id=urlsafe_base64_decode(uid))
    except (TypeError, ValueError, OverflowError, USER_MODEL.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse(f"{InfoMessages.objects.get(name='hi').full_text} {user.username}!\n"
                            f"{InfoMessages.objects.get(name='acc_activated').full_text}")
    return HttpResponse(ErrorMessages.objects.get(name='inv_token').full_text)


class SignIn(View):
    def get(self, request, short_error_message=None):
        return render(request, "signin.html", context={
            'error_message': request.session.get('error_message'),
            'short_error_message': short_error_message})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(reverse_lazy('home'))
        elif not user.is_active:
            request.session['error_message'] = ErrorMessages.objects.get(name='acc_not_activ').full_text
            return redirect(reverse_lazy(
                'sign_in_with_error',
                kwargs={'short_error_message': ErrorMessages.objects.get(name='acc_not_activ').name}))
        else:
            request.session['error_message'] = ErrorMessages.objects.get(name='wrong_signin').full_text
            return redirect(reverse_lazy(
                'sign_in_with_error',
                kwargs={'short_error_message': ErrorMessages.objects.get(name='wrong_signin').name}))


class SignOut(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('home'))
