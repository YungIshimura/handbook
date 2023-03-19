from django.contrib import admin

from .models import TypeWork, SRO, CompanyAddress, Company, Branches, CompanySpecialization, Director, Employee, City, \
    Region, License, WorkRegion, CompanyWorkRegion, Area


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass


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


@admin.register(WorkRegion)
class WorkRegionAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyWorkRegion)
class CompanyWorkRegionAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass