from django.contrib import admin

# Register your models here.
from .models import Inventory1, Transactions

admin.site.register(Inventory1)
admin.site.register(Transactions)
