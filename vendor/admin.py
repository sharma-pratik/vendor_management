from django.contrib import admin

# Register your models here.

from vendor.models import *


class PurchaseOrderInline(admin.ModelAdmin):
    model = PurchaseOrder
    list_display = [f.get_attname() for f in PurchaseOrder._meta.fields]


class VendorInline(admin.ModelAdmin):
    model = Vendor
    list_display = [f.get_attname() for f in Vendor._meta.fields]


class HistoricalPerformanceInline(admin.ModelAdmin):
    model = Vendor
    list_display = [f.get_attname() for f in HistoricalPerformance._meta.fields]

admin.site.register(PurchaseOrder, PurchaseOrderInline)
admin.site.register(Vendor, VendorInline)
admin.site.register(HistoricalPerformance, HistoricalPerformanceInline)
