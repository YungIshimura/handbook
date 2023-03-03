from django.shortcuts import render


def view_index(request):
    return render(request, 'index.html')


def view_sign_up_user(request):
    return render(request, 'sign_up_user.html')
