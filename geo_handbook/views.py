from django.shortcuts import HttpResponseRedirect, redirect, render, get_object_or_404
from django.urls import reverse
from geo_handbook.forms import CompanyUpdateForm, BranchCreateForm, DirectorCreateForm, EmployeeCreateForm
from geo_handbook.models import Company, Branches, Employee
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
        'work_types':[work_type.type_work for work_type in company.specializations.all()],
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


def company_update(request, pk):
    company = get_object_or_404(Company, pk=pk)
    employees = Employee.objects.filter(company=company).exclude(branches__isnull=False)
    if request.method == 'POST':
        form = CompanyUpdateForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('geo_handbook:edit_company', pk=company.pk)
    else:
        form = CompanyUpdateForm(instance=company)
    context = {
        'form': form,
        'company': company,
        'employees': employees
    }
    return render(request, 'enter_details_company.html', context)


# Редактировать филиал
def update_branch(request, pk):
    branch = get_object_or_404(Branches, pk=pk)
    employees = Employee.objects.filter(branches=branch)

    branch_form = BranchCreateForm(request.POST or None, instance=branch)
    director_form = DirectorCreateForm(request.POST or None, instance=branch.director.first())

    if request.method == 'POST':

        if branch_form.is_valid() and director_form.is_valid():
            branch_form.save()
            director_form.save()
            return redirect('geo_handbook:edit_company', pk=branch.company.pk)

    context = {
        'branch_form': branch_form,
        'director_form': director_form,
        'branch': branch,
        'employees': employees
    }

    return render(request, 'branches/update_branch.html', context)


# Удалить филиал и связанного с ним директора
def delete_branch(request, pk):
    branch = get_object_or_404(Branches, pk=pk)

    if request.method == 'POST':
        branch.director.all().delete()  # Удалить директоров филиала
        branch.delete()  # Удалить филиал
        return redirect('geo_handbook:edit_company', pk=branch.company.pk)

    return render(request, 'branches/delete_branch.html', {'branch': branch})


# Добавить филиал компании и директора филиала
def add_branch(request, pk):
    company = get_object_or_404(Company, pk=pk)

    branch_form = BranchCreateForm(request.POST or None)
    director_form = DirectorCreateForm(request.POST or None)

    if request.method == 'POST':

        if branch_form.is_valid() and director_form.is_valid():
            branch = branch_form.save(commit=False)
            branch.company = company
            branch.save()

            director = director_form.save(commit=False)
            director.company = company
            director.branches = branch
            director.save()

            return redirect('geo_handbook:edit_company', pk=pk)

    context = {
        'branch_form': branch_form,
        'director_form': director_form,
        'company': company
    }

    return render(request, 'branches/add_branch.html', context)


# Добавить сотрудника компании
def add_employee_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    form = EmployeeCreateForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            employee = form.save(commit=False)
            employee.company = company
            employee.save()

            return redirect('geo_handbook:edit_company', pk=pk)

    context = {
        'form': form,
        'company': company
    }

    return render(request, 'employee/add_employee.html', context)


# Редактировать сотрудника компании
def update_employee_company(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeCreateForm(request.POST or None, instance=employee)

    if request.method == 'POST':

        if form.is_valid():
            form.save()

            return redirect('geo_handbook:edit_company', pk=employee.company.pk)

    context = {
        'form': form,
        'employee': employee,
    }

    return render(request, 'employee/update_employee.html', context)


# Удалить сотрудника компании
def delete_employee_company(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('geo_handbook:edit_company', pk=employee.company.pk)

    return render(request, 'employee/delete_employee.html', {'employee': employee})


# Удалить сотрудника филиала
def delete_employee_branch(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('geo_handbook:edit_branches', pk=employee.branches.pk)

    return render(request, 'employee/delete_employee.html', {'employee': employee})


# Редактировать сотрудника филиала
def update_employee_branch(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeCreateForm(request.POST or None, instance=employee)

    if request.method == 'POST':

        if form.is_valid():
            form.save()

            return redirect('geo_handbook:edit_branches', pk=employee.branches.pk)

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

            return redirect('geo_handbook:edit_branches', pk=pk)

    return render(request, 'employee/add_employee.html', {'form': form})
