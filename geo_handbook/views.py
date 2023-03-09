from django.shortcuts import render, get_object_or_404, redirect
from geo_handbook.forms import CompanyUpdateForm, BranchesUpdateForm, BranchCreateForm
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
    branches = get_object_or_404(Branches, pk=pk)
    if request.method == 'POST':
        form = BranchesUpdateForm(request.POST, instance=branches)
        if form.is_valid():
            form.save()
            return redirect('geo_handbook:edit_company', pk=branches.company.pk)
    else:
        form = BranchesUpdateForm(instance=branches)
    return render(request, 'branches/update_branch.html', {'form': form, 'branches': branches})


# Удаление филиала и связанного с ним директора
def delete_branch(request, pk):
    branch = get_object_or_404(Branches, pk=pk)
    if request.method == 'POST':
        # Удалить директоров филиала
        branch.director.all().delete()
        # Удалить филиал
        branch.delete()
        return redirect('geo_handbook:edit_company', pk=branch.company.pk)
    context = {'branch': branch}
    return render(request, 'branches/delete_branch.html', context)


# Добавление филиала компании
def add_branch(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = BranchCreateForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.company = company
            branch.save()
            return redirect('geo_handbook:edit_company', pk=pk)
    else:
        form = BranchCreateForm(initial={'company': pk})
    return render(request, 'branches/add_branch.html', {'form': form, 'company': company})
