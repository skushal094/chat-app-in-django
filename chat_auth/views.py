from django.shortcuts import render


def login(request):
    return render(request, 'chat_auth/login.html', {})
