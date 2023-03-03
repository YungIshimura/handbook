from django.shortcuts import render


def view_index(request):
    return render (request, 'index.html')


def view_about(request):
    return render(request, 'about.html')


def view_select(request):
    return render(request, 'select_city.html')


def view_selected_region(request):
    return render(request, 'selected_region.html')


def view_card(request):
    return render(request, 'card.html')