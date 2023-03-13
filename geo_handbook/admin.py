from django.contrib import admin
from .models import TypeWork, SRO, CompanyAddress, Company, Branches, CompanySpecialization, Director, Employee


@admin.register(TypeWork)
class TypeWorkAdmin(admin.ModelAdmin):
    pass


@admin.register(SRO)
class SROAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyAddress)
class CompanyAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Branches)
class BranchesAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanySpecialization)
class CompanySpecializationAdmin(admin.ModelAdmin):
    pass


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass