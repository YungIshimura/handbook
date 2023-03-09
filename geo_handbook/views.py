from django.shortcuts import render, get_object_or_404, redirect
from geo_handbook.forms import CompanyUpdateForm, BranchCreateForm, DirectorCreateForm, EmployeeCreateForm
from geo_handbook.models import Company, Branches, Employee


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
    employee = Employee.objects.filter(company=company).exclude(branches__isnull=False)
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
        'employee': employee
    }
    return render(request, 'company_update.html', context)


# Редактировать филиал
def update_branch(request, pk):
    branch = get_object_or_404(Branches, pk=pk)

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
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('geo_handbook:edit_company', pk=employee.company.pk)

    return render(request, 'employee/delete_employee.html', {'employee': employee})
