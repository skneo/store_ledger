from django.contrib import admin

# Register your models here.
from . models import Inventory1, Transactions


class invAdmin(admin.ModelAdmin):
    list_display = ('material_code', 'material_name', 'balance')


admin.site.register(Inventory1, invAdmin)


class transAdmin(admin.ModelAdmin):
    list_display = ('material_code', 'material_name', 'in_out',
                    'quantity', 'balance', 'issued_to')


admin.site.register(Transactions, transAdmin)
