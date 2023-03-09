from django.shortcuts import render, get_object_or_404, redirect
from geo_handbook.forms import CompanyUpdateForm, BranchCreateForm, DirectorCreateForm
from geo_handbook.models import Company, Branches


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
    if request.method == 'POST':
        form = CompanyUpdateForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('geo_handbook:edit_company', pk=company.pk)
    else:
        form = CompanyUpdateForm(instance=company)
    return render(request, 'company_update.html', {'form': form, 'company': company})


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


# Удаление филиала и связанного с ним директора
def delete_branch(request, pk):
    branch = get_object_or_404(Branches, pk=pk)

    if request.method == 'POST':
        branch.director.all().delete()  # Удалить директоров филиала
        branch.delete()  # Удалить филиал
        return redirect('geo_handbook:edit_company', pk=branch.company.pk)

    return render(request, 'branches/delete_branch.html', {'branch': branch})


# Добавление филиала компании и директора филиала
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
