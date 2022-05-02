from rest_framework import serializers
from .models import (
    equipment,
    inventory_db,
    inventory_transaction
)


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = equipment
        read_only_fields = ('id',)
        fields = (
            'id',
            'equipment_id',
            'equipment_name',
            'purchase_value',
            'rental_rate'
        )

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = inventory_db
        read_only_fields = ('id',)
        fields = '__all__'

class InventoryTransactions(serializers.ModelSerializer):
    transactions_inventory = serializers.SerializerMethodField()
    class Meta:
        model = inventory_transaction
        read_only_fields = ('id',)
        fields = (
            'id',
            'inventory_id',
            'transactions_inventory',
            'brand',
            'category_inv',
            'item_description',
            'unit_measurement',
            'inventory_price'
        )
    def get_transactions_inventory(self, obj):
        return InventorySerializer(obj.transactions_inventory).data
