from django.db import models
from datetime import date

from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.

class equipment(models.Model):
    equipment_id = models.CharField(max_length=100,
                                blank=True, null=True)
    equipment_name = models.CharField(max_length=100)
    purchase_value = models.DecimalField(max_digits=19,decimal_places=2,null=True, blank=True)
    rental_rate = models.DecimalField(max_digits=19,decimal_places=2,null=True, blank=True)
    equipment_descriptions = models.CharField(max_length=250)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['equipment_name']
        db_table = 'equipment_db'
    
    def __str__(self):
        return f'{self.equipment_id}'

class inventory_db(models.Model):
    TX_TYPE = (
        ('1', _('In')),
        ('2', _('Out'))
    )
    trans_date = models.DateField(default=date.today, verbose_name=_('Date'))
    sales_invoice = models.CharField(max_length=50, verbose_name=_('Inventory id'))
    supplier = models.CharField(max_length=100, verbose_name=_('Supplier'))
    transaction_type = models.CharField(max_length=10, choices=TX_TYPE, verbose_name=_('Tx Type'))
    mrs_number = models.CharField(max_length=50, verbose_name=_('MRS'))
    requested_by = models.CharField(max_length=10, verbose_name=_('Requested by'))
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering = ['-trans_date']
        verbose_name = _('inventory')
        verbose_name_plural = _('inventories')

        db_table = 'inventory'

    def __str__(self):
        return f'{self.trans_date} - {self.sales_invoice}'

class inventory_transaction(models.Model):
    CATEGORY_TYPE = (
        ('1', _('Tires')),
        ('2', _('Oil & Lubricants')),
        ('3', _('Mechanical Parts')),
        ('4', _('Office Supplies')),
        ('5', _('Tools Supplies')),
        ('6', _('Others Supplies')),
    )
    transactions_inventory = models.ForeignKey(inventory_db, on_delete=models.CASCADE, null=True, blank=True)
    inventory_id = models.CharField(max_length=20, verbose_name=_('Inventory id'))
    brand = models.CharField(max_length=100,verbose_name=_('Brand'))
    category_inv = models.CharField(max_length=25, choices=CATEGORY_TYPE, verbose_name=_('Category Type'))
    item_description = models.CharField(max_length=100, verbose_name=_('Item Description'))
    quantity = models.DecimalField(max_digits=19,decimal_places=2,null=True, blank=True)
    unit_measurement = models.CharField(max_length=50, verbose_name=_('Unit'))
    inventory_price = models.DecimalField(max_digits=19,decimal_places=2,null=True, blank=True)
    inventory_amount = models.DecimalField(max_digits=19,decimal_places=2,null=True, blank=True)
    equipment = models.CharField(max_length=20, verbose_name=_('equipment'))
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering = ['-transactions_inventory']
        verbose_name = _('inventory_transaction')
        verbose_name_plural = _('inventories_transactions')

        db_table = 'inventory_transaction'

    def __str__(self):
        return f'{self.inventory_id} - {self.item_description}'
