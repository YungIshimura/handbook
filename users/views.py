from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from users.forms import CompanyUpdateForm, DirectorCreateForm, EmployeeCreateForm, CityCreateForm, AddressCreateForm, \
    LicenseCreateForm
from geo_handbook.models import Company, Branches, Employee, CompanyAddress, License


def view_profile(request):
    return render(request, 'profile.html')


def update_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    employees = Employee.objects.filter(company=company).exclude(branches__isnull=False)
    form = CompanyUpdateForm(request.POST or None, instance=company)
    # формы, которые передаем для модальных окон
    add_employee_form = EmployeeCreateForm()
    edit_employee_form = EmployeeCreateForm()
    add_branch_city_form = CityCreateForm()
    add_branch_address_form = AddressCreateForm()
    edit_branch_city_form = CityCreateForm()
    edit_branch_address_form = AddressCreateForm()
    add_license_form = LicenseCreateForm()
    edit_license_form = LicenseCreateForm()
    # add_branch_form = BranchCreateForm()

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('users:edit_company', pk=company.pk)

    context = {
        'form': form,
        'add_employee_form': add_employee_form,
        'edit_employee_form': edit_employee_form,
        'add_branch_city_form': add_branch_city_form,
        'add_branch_address_form': add_branch_address_form,
        'edit_branch_city_form': add_branch_city_form,
        'edit_branch_address_form': add_branch_address_form,
        'add_license_form': add_license_form,
        'edit_license_form': edit_license_form,
        # 'add_branch_form': add_branch_form,
        'company': company,
        'employees': employees
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
def edit_branch_company(request, pk):
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


# Удалить сотрудника филиала
def delete_employee_branch(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('users:edit_branches', pk=employee.branches.pk)

    return render(request, 'employee/delete_employee.html', {'employee': employee})


# Редактировать сотрудника филиала
def update_employee_branch(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeCreateForm(request.POST or None, instance=employee)

    if request.method == 'POST':

        if form.is_valid():
            form.save()

            return redirect('users:edit_branches', pk=employee.branches.pk)

    context = {
        'form': form,
        'employee': employee,
    }

    return render(request, 'employee/update_employee.html', context)


# Добавить сотрудника филиала
def add_employee_branch(request, pk):
    branch = get_object_or_404(Branches, pk=pk)
    form = EmployeeCreateForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            employee = form.save(commit=False)
            employee.company = branch.company
            employee.branches = branch
            employee.save()

            return redirect('users:edit_branches', pk=pk)

    return render(request, 'employee/add_employee.html', {'form': form})
