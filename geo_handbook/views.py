from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from geo_handbook.models import Company, City
from django.contrib.postgres.search import SearchVector
from django.contrib import messages
from django.http import JsonResponse


def view_index(request):
    search_vector = SearchVector('short_name', 'inn', 'ogrn', 'director')
    if request.POST.get('search'):
        company = Company.objects.annotate(search=search_vector).filter(search=request.POST.get('search'))
        if company:
            return HttpResponseRedirect(reverse('geo_handbook:card', args=[company[0].id]))
        else:
            messages.error(request, 'По данному запросу ничего не найдено')

    if 'term' in request.GET:
        qs = City.objects.filter(name__icontains=request.GET.get('term'))
        citys = []
        for company in qs:
            citys.append(company.name)
        return JsonResponse(citys, safe=False)

    if 'region' in request.POST:
        region = request.POST.get('region')
        city_id = City.objects.get(name=region).id
        return HttpResponseRedirect(reverse('geo_handbook:region', args=[city_id]))

    if 'city_search' in request.GET:
        city = request.GET.get('city_search')
        city_id = City.objects.get(name=city).id
        return HttpResponseRedirect(reverse('geo_handbook:region', args=[city_id]))

    return render(request, 'index.html')


def view_sign_up_user(request):
    return render(request, 'sign_up_user.html')


def view_card(request, company_id):
    company = Company.objects.get(id=company_id)
    type_works = [work_type.type_work for work_type in company.specializations.all()]
    companys = []
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
        'sro_license_date': [company for company in company.licenses.all()],
        'street': company.legal_address.street,
        'index': company.legal_address.postcode,
        'house_number': company.legal_address.house_number,
        'directors': [director for director in company.director.all()]
    }
    for type_work in type_works:
        region_company = Company.objects.filter(specializations=type_work.id,legal_address__city_id=company.legal_address.city)
        if region_company:
            companys.append(region_company)
        
    context['type_works'] = type_works
    context['companys'] = companys

    return render(request, 'card.html', context=context)


def view_sign_up_company(request):
    return render(request, 'sign_up_company.html')



def view_card_layer(request):
    return render(request, 'card_layer.html')


def view_about(request):
    return render(request, 'about.html')


def view_rates(request):
    return render(request, 'rates.html')


def view_selected_region(request, city_id):
    companys = Company.objects.filter(legal_address__city=city_id)
    context = {
        'companys': [
            {
                'id': company.id,
                'name': company.short_name,
                'work_types': [work_type.type_work for work_type in company.specializations.all()],
                'legal_address': company.legal_address
            }
            for company in companys
        ],
        'region': City.objects.get(id=city_id)
    }

    return render(request, 'selected_region.html', context=context)


def view_application(request):
    return render(request, 'application.html')


def view_profile(request):
    return render(request, 'profile.html')


def view_enter_details_company(request):
    return render(request, 'enter_details_company.html')


def view_settings_profile(request):
    return render(request, 'settings_profile.html')
