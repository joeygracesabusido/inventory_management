from django.urls import path
from .import views


urlpatterns = [
    path('', views.loginPage, name="login"),
    path('navbar/', views.navBar_dashboard, name="navbar"),
    path('test/', views.testing_html, name="test"),
    path('insert_equipment/', views.insert_equipment, name="insert_equipment"),
    path('equipment_list/', views.get_equipment_list, name="equipment_list"),
    path('equipmentDelete/<int:id>/', views.delete_equipment, name="equipmentDelete"),
    path('inventory/', views.test_inventory, name="inventory"),
    path('test-html/', views.test, name="test-html"),
    path('insert-inventory-in/', views.save_inventory_in, name="insert-inventory-in"),
    path('inventorylist/', views.inventory_list, name="inventorylist"),


    #### for API calls ###
    path('api-equipments/', views.get_equipments, name='api-equipments'),
    path('api-inventory-trans/', views.get_inv_transactions, name='api-transactions')
   
]