from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from geo_handbook.models import Company
from django.contrib.postgres.search import SearchVector
from django.contrib import messages


def view_index(request):
    search_vector = SearchVector('short_name', 'inn', 'ogrn', 'director')
    if request.method == 'POST':
        company = Company.objects.annotate(search=search_vector).filter(search=request.POST.get('search'))
        if company:
            return HttpResponseRedirect(reverse('geo_handbook:card', args=[company[0].id]))
        else:
            messages.error(request, 'По данному запросу ничего не найдено')

    return render(request, 'index.html')


def view_sign_up_user(request):
    return render(request, 'sign_up_user.html')


def view_card(request, company_id):
    company = Company.objects.get(id=company_id)
    context = {
        'short_name': company.short_name,
        'full_name': company.full_name,
        'inn': company.inn,
        'ogrn': company.ogrn,
        'city': company.legal_address.city,
        'rating': company.rating,
        'sro': company.sro,
        'sro_date': company.sro_date,
        'sro_number': company.sro_number,
        'sro_license_date': company.license_date,
        'street': company.legal_address.street,
        'index': company.legal_address.postcode,
        'house_number': company.legal_address.house_number,
        'work_types': [work_type.type_work for work_type in company.specializations.all()],
        'directors': [director for director in company.director.all()]
    }

    return render(request, 'card.html', context=context)


def view_sign_up_company(request):
    return render(request, 'sign_up_company.html')


def view_select_city(request):
    return render(request, 'select_city.html')


def view_search(request):
    return render(request, 'search.html')


def view_card_layer(request):
    return render(request, 'card_layer.html')


def view_about(request):
    return render(request, 'about.html')


def view_select(request):
    return render(request, 'select_city.html')


def view_selected_region(request):
    return render(request, 'selected_region.html')


def view_application(request):
    return render(request, 'application.html')


def view_profile(request):
    return render(request, 'profile.html')


def view_enter_details_company(request):
    return render(request, 'enter_details_company.html')


def view_settings_profile(request):
    return render(request, 'settings_profile.html')