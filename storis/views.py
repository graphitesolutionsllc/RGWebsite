from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    context = {

    }
    return render(request, 'storis/home.html', context)

def login(request):
    context = {

    }
    return render(request, 'storis/login.html', context)
