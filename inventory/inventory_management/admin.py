from django.contrib import admin

# Register your models here.
from inventory_management import models
from .models import equipment,inventory_db, inventory_transaction

admin.site.register(equipment)
# admin.site.register(inventory_db)
# admin.site.register(inventory_transaction)


class Inventory_transactionInline(admin.TabularInline):
    model = models.inventory_transaction


@admin.register(models.inventory_db)
class InventorylAdmin(admin.ModelAdmin):
    inlines = [Inventory_transactionInline]