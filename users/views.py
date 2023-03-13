from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from users.forms import CompanyUpdateForm, BranchCreateForm, DirectorCreateForm, EmployeeCreateForm
from geo_handbook.models import Company, Branches, Employee


def view_profile(request):
    return render(request, 'profile.html')


def update_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    employees = Employee.objects.filter(company=company).exclude(branches__isnull=False)
    form = CompanyUpdateForm(request.POST or None, instance=company)
    add_employee_form = EmployeeCreateForm()
    edit_employee_form = EmployeeCreateForm()

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('users:edit_company', pk=company.pk)

    context = {
        'form': form,
        'add_employee_form': add_employee_form,
        'edit_employee_form': edit_employee_form,
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
            return redirect('users:edit_company', pk=branch.company.pk)

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
        return redirect('users:edit_company', pk=branch.company.pk)

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

            return redirect('users:edit_company', pk=pk)

    context = {
        'branch_form': branch_form,
        'director_form': director_form,
        'company': company
    }

    return render(request, 'branches/add_branch.html', context)


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


# Получить данные о сотруднике компании
def get_employee_data(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    data = {
        'position': employee.position,
        'surname': employee.surname,
        'name': employee.name,
        'father_name': employee.father_name,
    }
    return JsonResponse(data)


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
    employee = get_object_or_404(Employee, pk=pk)

    employee.delete()

    if request.is_ajax():
        data = {'success': True}
        return JsonResponse(data)
    else:
        return redirect('users:edit_company', pk=employee.company.pk)


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
