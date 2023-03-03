from django.shortcuts import render


def view_index(request):
    return render (request, 'index.html')


def view_about(request):
    return render(request, 'about.html')