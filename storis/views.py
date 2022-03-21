from django.shortcuts import render
from .packages import functionality as FY


def home(request):
    context = {

    }
    return render(request, 'storis/home.html', context)


def login(request):
    context = {

    }
    return render(request, 'storis/login.html', context)


def handler404(request, exception):
    return render(request, 'storis/404.html', {})


def singleUpdate(request):
    context = {

    }
    FY.fullWebsiteUpdate()
    return render(request, 'storis/home.html', context)
