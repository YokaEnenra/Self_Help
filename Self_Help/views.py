from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from Self_Help.models import TestModel


# Create your views here.
class TestModelView(ListView):
    model = TestModel
    template_name = "test.html"
