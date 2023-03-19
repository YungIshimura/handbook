import json
from django.db import transaction

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from users.forms import EmployeeCreateForm, CityCreateForm, AddressCreateForm, \
    LicenseCreateForm, CompanyContactPhoneForm, CompanyContactEmailForm, CompanyContactUrlForm

from geo_handbook.models import Company, Branches, Employee, License, TypeWork, CompanySpecialization, Director, \
    WorkRegion, CompanyWorkRegion


def view_profile(request):
    return render(request, 'profile.html')


def update_company(request, pk):
    company = get_object_or_404(Company.objects.select_related('legal_address__region'), pk=pk)
    employees = Employee.objects.filter(company=company).exclude(branches__isnull=False)
    type_works = TypeWork.objects.all()
    work_regions = WorkRegion.objects.all()
    branches = company.branches.select_related('address').all()
    # формы, которые передаем для модальных окон
    forms = {
        'add_employee_form': EmployeeCreateForm(),
        'edit_employee_form': EmployeeCreateForm(),
        'add_branch_city_form': CityCreateForm(),
        'add_branch_address_form': AddressCreateForm(),
        'edit_branch_city_form': CityCreateForm(),
        'edit_branch_address_form': AddressCreateForm(),
        'add_license_form': LicenseCreateForm(),
        'edit_license_form': LicenseCreateForm(),
        'add_contact_phone_form': CompanyContactPhoneForm(),
        'edit_contact_phone_form': CompanyContactPhoneForm(),
        'add_contact_email_form': CompanyContactEmailForm(),
        'edit_contact_email_form': CompanyContactEmailForm(),
        'add_contact_url_form': CompanyContactUrlForm(),
        'edit_contact_url_form': CompanyContactUrlForm(),
    }

    context = {
        **forms,
        'company': company,
        'branches': branches,
        'employees': employees,
        'type_works': type_works,
        'work_regions': work_regions
    }
    return render(request, 'enter_details_company.html', context)


# Получить данные о сотруднике компании
def get_employee_data(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    data = {
        'position': employee.position,
        'surname': employee.surname,
        'name': employee.name,
        'father_name': employee.father_name,
        'phonenumber': employee.phonenumber,
        'email': employee.email
    }
    return JsonResponse(data)


# Добавить сотрудника компании
@require_POST
def add_employee_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    add_employee_form = EmployeeCreateForm(request.POST)

    if add_employee_form.is_valid():
        employee = add_employee_form.save(commit=False)
        employee.company = company
        employee.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': add_employee_form.errors}, status=400)


# Редактировать сотрудника компании
@require_POST
def update_employee_company(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    edit_employee_form = EmployeeCreateForm(request.POST, instance=employee)
    if edit_employee_form.is_valid():
        edit_employee_form.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': edit_employee_form.errors}, status=400)


# Удалить сотрудника компании
@require_POST
def delete_employee_company(request, pk):
    try:
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        data = {'success': True}

    except Exception as e:
        data = {'error': str(e)}

    return JsonResponse(data)


# Получить данные о филиале компании
def get_branche_data(request, pk):
    branche = get_object_or_404(Branches, pk=pk)
    data = {
        'region': branche.address.region.pk,
        'postcode': branche.address.postcode,
        'city': branche.address.city.name,
        'district': branche.address.district,
        'street': branche.address.street,
        'house_number': branche.address.house_number
    }
    return JsonResponse(data)


# Добавить филиал компании
@require_POST
def add_branch_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    add_branch_city_form = CityCreateForm(request.POST)
    add_branch_address_form = AddressCreateForm(request.POST)

    if add_branch_city_form.is_valid() and add_branch_address_form.is_valid():
        city = add_branch_city_form.save()
        address = add_branch_address_form.save(commit=False)
        address.city = city
        address.save()
        if address:
            branch = Branches(address=address, company=company)
            branch.save()
            return JsonResponse({'success': True})
    errors = {}
    for form in [add_branch_city_form, add_branch_address_form]:
        for field, error_list in form.errors.items():
            errors[field] = error_list[0] if error_list else ''

    return JsonResponse({'success': False, 'errors': errors}, status=400)


# Редактировать филиал
@require_POST
def update_branch_company(request, pk):
    branch = get_object_or_404(Branches, pk=pk)
    edit_branch_city_form = CityCreateForm(request.POST, instance=branch.address.city)
    edit_branch_address_form = AddressCreateForm(request.POST, instance=branch.address)

    if edit_branch_city_form.is_valid() and edit_branch_address_form.is_valid():
        city = edit_branch_city_form.save()
        address = edit_branch_address_form.save(commit=False)
        address.city = city
        address.save()
        if address:
            branch.address = address
            branch.save()
            return JsonResponse({'success': True})
    errors = {}
    for form in [edit_branch_city_form, edit_branch_address_form]:
        for field, error_list in form.errors.items():
            errors[field] = error_list[0] if error_list else ''
    return JsonResponse({'success': False, 'errors': errors}, status=400)


# Удалить филиал
@require_POST
def delete_branch(request, pk):
    try:
        branch = get_object_or_404(Branches, pk=pk)
        # удаляем адрес и филиал
        branch.address.delete()
        branch.delete()
        data = {'success': True}

    except Exception as e:
        data = {'error': str(e)}

    return JsonResponse(data)


# Получить данные о лицензии компании
def get_license_data(request, pk):
    license = get_object_or_404(License, pk=pk)
    data = {
        'name': license.name,
        'license_date': license.license_date,
        'license_area': license.license_area,
        'license_organization': license.license_organization
    }
    return JsonResponse(data)


# Добавить лицензию компании
@require_POST
def add_license_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    add_license_form = LicenseCreateForm(request.POST)

    if add_license_form.is_valid():
        license = add_license_form.save(commit=False)
        license.company = company
        license.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': add_license_form.errors}, status=400)


# Редактировать лицензию компании
@require_POST
def update_license_company(request, pk):
    license = get_object_or_404(License, pk=pk)
    edit_license_form = LicenseCreateForm(request.POST, instance=license)
    if edit_license_form.is_valid():
        edit_license_form.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': edit_license_form.errors}, status=400)


# Удалить лицензию компании
@require_POST
def delete_license_company(request, pk):
    try:
        license = get_object_or_404(License, pk=pk)
        license.delete()
        data = {'success': True}

    except Exception as e:
        data = {'error': str(e)}

    return JsonResponse(data)


# Получить данные о номерах телефонов компании
def get_contact_phone_data(request, pk):
    company = get_object_or_404(Company, pk=pk)
    data = {
        'contact_phone': company.contact_phone,
    }
    return JsonResponse(data)


# Добавить контактные телефоны
@require_POST
def add_contact_phone_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    add_contact_phone_form = CompanyContactPhoneForm(request.POST)

    if add_contact_phone_form.is_valid():
        contact_phone = add_contact_phone_form.cleaned_data['contact_phone']
        company.contact_phone = contact_phone
        company.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': add_contact_phone_form.errors}, status=400)


# Редактировать телефонные номера компании
@require_POST
def update_contact_phone_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    edit_contact_phone_form = CompanyContactPhoneForm(request.POST)

    if edit_contact_phone_form.is_valid():
        contact_phone_numbers = edit_contact_phone_form.cleaned_data['contact_phone']
        # создаем список строк из объектов PhoneNumber
        contact_phone_list = [str(phone_number) for phone_number in contact_phone_numbers]
        company.contact_phone = contact_phone_list
        company.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': edit_contact_phone_form.errors}, status=400)


# Удалить контактные телефоны компании
@require_POST
def delete_contact_phone_company(request, pk):
    try:
        company = get_object_or_404(Company, pk=pk)
        company.contact_phone = None
        company.save()
        data = {'success': True}

    except Exception as e:
        data = {'error': str(e)}

    return JsonResponse(data)


# Получить данные о email компании
def get_contact_email_data(request, pk):
    company = get_object_or_404(Company, pk=pk)
    data = {
        'contact_email': company.contact_email,
    }
    return JsonResponse(data)


# Добавить контактные email компании
@require_POST
def add_contact_email_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    add_contact_email_form = CompanyContactEmailForm(request.POST)

    if add_contact_email_form.is_valid():
        contact_email = add_contact_email_form.cleaned_data['contact_email']
        company.contact_email = contact_email
        company.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': add_contact_email_form.errors}, status=400)


# Редактировать email компании
@require_POST
def update_contact_email_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    edit_contact_email_form = CompanyContactEmailForm(request.POST)

    if edit_contact_email_form.is_valid():
        contact_email = edit_contact_email_form.cleaned_data['contact_email']
        # создаем список строк из объектов email
        contact_email_list = [str(email) for email in contact_email]
        company.contact_email = contact_email_list
        company.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': edit_contact_email_form.errors}, status=400)


# Удалить контактный email компании
@require_POST
def delete_contact_email_company(request, pk):
    try:
        company = get_object_or_404(Company, pk=pk)
        company.contact_email = None
        company.save()
        data = {'success': True}

    except Exception as e:
        data = {'error': str(e)}

    return JsonResponse(data)


# Получить данные о url компании
def get_contact_url_data(request, pk):
    company = get_object_or_404(Company, pk=pk)
    data = {
        'contact_url': company.contact_url,
    }
    return JsonResponse(data)


# Добавить контактный url компании
@require_POST
def add_contact_url_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    add_contact_url_form = CompanyContactUrlForm(request.POST)

    if add_contact_url_form.is_valid():
        contact_url = add_contact_url_form.cleaned_data['contact_url']
        company.contact_url = contact_url
        company.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': add_contact_url_form.errors}, status=400)


# Редактировать url компании
@require_POST
def update_contact_url_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    edit_contact_url_form = CompanyContactUrlForm(request.POST)

    if edit_contact_url_form.is_valid():
        contact_url = edit_contact_url_form.cleaned_data['contact_url']
        company.contact_url = contact_url
        company.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': edit_contact_url_form.errors}, status=400)


# Удалить контактный url компании
@require_POST
def delete_contact_url_company(request, pk):
    try:
        company = get_object_or_404(Company, pk=pk)
        company.contact_url = None
        company.save()
        data = {'success': True}

    except Exception as e:
        data = {'error': str(e)}

    return JsonResponse(data)


# обновляем данные компании
@require_POST
def update_data_company(request, pk):

    # Получаем типы работ и регионы выполняемых работ, отправленные с клиента, очищаем данные
    type_works = [item.strip() for item in json.loads(request.body)['type_works']]
    region_works = [item.strip() for item in json.loads(request.body)['region_works']]

    with transaction.atomic():
        company = get_object_or_404(Company, pk=pk)

        # удаляем те работы, которых нет в списке
        company.specializations.exclude(type_work__type__in=type_works).delete()

        # Добавляем новые связи между компанией и типами работ
        for specialization in type_works:
            type_work = get_object_or_404(TypeWork, type=specialization)
            CompanySpecialization.objects.get_or_create(company=company, type_work=type_work)

        # удаляем те регионы выполняемых работ, которых нет в списке
        company.work_regions_companies.exclude(working_zone__title__in=region_works).delete()

        # Добавляем новые связи между компанией и регионами выполняемых работ
        for region in region_works:
            work_region = get_object_or_404(WorkRegion, title=region)
            CompanyWorkRegion.objects.get_or_create(company=company, working_zone=work_region)
=

    return JsonResponse({'success': True})
