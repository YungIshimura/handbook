from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from geo_handbook.models import Company, City, CompanySpecialization
from django.contrib.postgres.search import SearchVector
from django.contrib import messages
from django.http import JsonResponse
from .forms import OrderForm


def get_city(req):
    qs = City.objects.filter(name__icontains=req.GET.get('term'))
    citys = []
    for company in qs:
        citys.append(company.name)

    return citys


def get_company(req):
    search_vector = SearchVector('short_name', 'inn', 'ogrn', 'director')
    company = Company.objects.annotate(search=search_vector).filter(
        search=req.POST.get('search'))

    return company


def view_index(request):
    if request.POST.get('search'):
        company = get_company(request)
        if company:
            return HttpResponseRedirect(reverse('geo_handbook:card', args=[company[0].id]))
        else:
            messages.error(request, 'По данному запросу ничего не найдено')

    if 'term' in request.GET:
        cities = get_city(request)
        return JsonResponse(cities, safe=False)

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
    company = Company.objects.select_related(
        'legal_address').get(id=company_id)
    type_works = [type_work.type_work for type_work in company.specializations.select_related(
        'type_work').all()]
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
    region_companys = CompanySpecialization.objects.filter(
        company__legal_address__city_id=company.legal_address.city.id, type_work__in=type_works).distinct(
        'company_id').select_related(
        'type_work', 'company').order_by('-company')

    context['type_works'] = type_works
    context['companys'] = region_companys

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
    if 'term' in request.GET:
        cities = get_city(request)
        return JsonResponse(cities, safe=False)

    if request.POST.get('search'):
        company = get_company(request)
        return HttpResponseRedirect(reverse('geo_handbook:card', args=[company[0].id]))

    companys = Company.objects.filter(legal_address__city=city_id).order_by(
        '-rating').select_related('legal_address__city')
    context = {
        'companys': [
            {
                'id': company.id,
                'name': company.short_name,
                'work_types': [type_work.type_work for type_work in
                               company.specializations.select_related('type_work').all()],
                'legal_address': company.legal_address,
                'rating': company.rating
            }
            for company in companys
        ],
        'region': City.objects.get(id=city_id)
    }

    return render(request, 'selected_region.html', context=context)


def view_application(request):
    context = {}
    if request.method == 'POST':
        form = OrderForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('geo_handbook:index'))
        else:
            print(form.errors)
    else:
        form = OrderForm()

    context['form'] = form
    return render(request, 'application.html', context=context)


def view_profile(request):
    return render(request, 'profile.html')


def view_enter_details_company(request):
    return render(request, 'enter_details_company.html')


def view_settings_profile(request):
    return render(request, 'settings_profile.html')
