from django.shortcuts import render


def view_index(request):
    return render(request, 'index.html')


def view_sign_up_user(request):
    return render(request, 'sign_up_user.html')


def view_sign_up_company(request):
    return render(request, 'sign_up_company.html')


def view_select_city(request):
    return render(request, 'select_city.html')


def view_search(request):
    return render(request, 'search.html')


def view_card_layer(request):
    return render(request, 'card_layer.html')


def view_card(request):
    return render(request, 'card.html')
