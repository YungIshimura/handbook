from django.contrib import admin
from .models import TypeWork, SRO, LegalAddress, Company, Branches, CompanySpecialization, Director, Employee


@admin.register(TypeWork)
class TypeWorkAdmin(admin.ModelAdmin):
    pass


@admin.register(SRO)
class SROAdmin(admin.ModelAdmin):
    pass


@admin.register(LegalAddress)
class LegalAddressAdmin(admin.ModelAdmin):
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