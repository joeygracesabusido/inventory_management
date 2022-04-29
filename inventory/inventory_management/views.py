from datetime import datetime,date
from django.shortcuts import render,redirect

# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages, auth

from .models import equipment, inventory_db, inventory_transaction

# from django.shortcuts import HttpResponse
from django.http import HttpResponse, JsonResponse

from django.db.models import Sum

from .serializers import (
    EquipmentSerializer, InventoryTransactions
)

import csv

# def is_ajax(request):
#     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# def ajax_test(request):
#     if is_ajax(request=request):
#         message = "This is ajax"
#     else:
#         message = "Not ajax"
#     return HttpResponse(message)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def get_equipments(request):
    if is_ajax(request=request):
        equipments = equipment.objects.all()
        print(equipments)
        return JsonResponse({
            'data': [EquipmentSerializer(e).data for e in equipments],
            })
    return redirect('/')

def get_inv_transactions(request):
    val = request.GET['val']
    if is_ajax(request=request):
        # inv = inventory_transaction.objects.all()
        inv = inventory_transaction.objects.get(inventory_id=val)
        
        print(inv)
        return JsonResponse({
            'data': InventoryTransactions(inv).data
            })
    return redirect('/')

def loginPage(request):
    #return render(request, 'accounts/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect('navbar')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request,
                  "login.html",
                  {"form": form})

def navBar_dashboard(request):
    return render(request, 'navbar.html')
def testing_html(request):
    return render(request, 'equipment_entry.html')

def insert_equipment(request):
    """
    This function is for inserting
    Equipment
    """
    
    if request.is_ajax():
        print(request.POST)
        equipment_id = request.POST.get('equipment_id')
        equipment_name = request.POST.get('equipment_name')
        purchase_value = request.POST.get('purchase_value')
        rental_rate = request.POST.get('rental_rate')
        equipment_descriptions = request.POST.get('equipment_decription')
        
        
        db_save = equipment.objects.create(
            equipment_id = equipment_id,
            equipment_name = equipment_name,
            purchase_value = purchase_value,
            rental_rate = rental_rate,
            equipment_descriptions = equipment_descriptions
        )
        # print(ChartofAccount_link)
        return redirect('/equipment_list')
    return render(request,'navbar.html')
def view_equipment(request):
    """
    This function is to 
    list of equipment
    """
    results = equipment.objects.all()
    return render(request, "equipment.html", {"show_equipment": results})

def get_equipment_list(request):
     
    context = {
        'sequenceList': equipment.objects.order_by('equipment_id')
    }
    return render(request, "equipment_list.html", context)

def delete_equipment(request,id):
    """
    This function is for
    Deleting Entry for Barcode
    """
    transactions_pk = equipment.objects.get(pk=id)
    transactions_pk.delete()
    return redirect("equipment_list")

def test_inventory(request):
    """
    This is for inventory
    html
    """
    context = {
        'sequenceList': equipment.objects.order_by('equipment_id')
    }
    return render(request,'inventory.html',context)

def test(request):
    """
    this function is for testing 
    multiplication
    """

    return render(request, "test.html")

def save_inventory_in(request):
    """
    This function is for
    saving inventory in
    """

    if request.method == 'POST':
        trans_date = request.POST.get('inventory_date')
        transtype = request.POST.get('transType')
        sales_invoice = request.POST.get('sales_invoice')
        supplier_in = request.POST.get('supplier')
        mrs_no = request.POST.get('mrs')
        requested_by = request.POST.get('requested_by')
      
        journal_save = inventory_db.objects.create(
            trans_date = trans_date,
            transaction_type = transtype,
            sales_invoice = sales_invoice,
            supplier = supplier_in,
            mrs_number = mrs_no,
            requested_by =requested_by
        )
        
        data_ = dict(request.POST.lists())
        data_.pop('csrfmiddlewaretoken')
        data_.pop('inventory_date')
        data_.pop('transType')
        data_.pop('mrs')
        data_.pop('requested_by')
        data_.pop('sales_invoice')
        data_.pop('supplier')
        
        
        entry = len(data_['inventory_id_in'])
        
        for k in data_.items():
            print(k)
    
        result = []
        for i in range(entry):
            d={}
            for j,k in enumerate(data_.items()):
                if j == 0:
                    d['inventory_id_in']= (k[1][i])
                elif j == 1:
                    d['brand']= (k[1][i])
                elif j == 2:
                    d['myCategory']= (k[1][i])
               
                elif j == 3:
                    d['itemdescriptions']= (k[1][i])
                elif j == 4:
                    d['quantity']= (k[1][i])
                elif j == 5:
                    d['unit']= (k[1][i])
                elif j == 6:
                    d['price']= (k[1][i])
                elif j == 7:
                    d['amount']= (k[1][i])
                elif j == 8:
                    d['Equipment']= (k[1][i])
            result.append(d)


        for r in result:
            inventory_transaction.objects.create(
                transactions_inventory = journal_save,
                trans_date = trans_date,
                inventory_id = r['inventory_id_in'],
                brand = r['brand'],
                category_inv = r['myCategory'],
                item_description = r['itemdescriptions'],
                quantity = r['quantity'],
                unit_measurement = r['unit'],
                inventory_price = r['price'],
                inventory_amount = r['amount'],
                equipment = r['Equipment']
            )

    
        return redirect('/inventorylist')
        # return render(request,'choices.html')
    

    return render(request,'inventory.html')

def inventory_list(request):
    """
    This function is for inventory List
    """

   
    # if request.method=="POST":
        
    equipment_search = request.GET.get('equipment_id')
    inventory_search = request.GET.get('Inventory_id')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    

    if equipment_search != '' and  inventory_search != '':
        

        # searchResult = inventory_transaction.objects.raw('SELECT id, inventory_id, quantity,\
        #                                     unit_measurement,inventory_price,inventory_amount,\
        #                                         equipment\
        #                                     from inventory_transaction where \
        #                                     equipment like "%'+ equipment_search +'%" and \
        #                                     inventory_id like "%'+ inventory_search +'%"' )

        
        
        
        
        searchResult = inventory_transaction.objects.filter(equipment = equipment_search).filter(inventory_id = inventory_search)
        total = searchResult.aggregate(Sum('inventory_amount'))
        
        return render (request,"inventoryList.html", {"inventory_list": searchResult,
                        'total': total['inventory_amount__sum'] })
        
    elif equipment_search != '' and inventory_search == '' and date_from =='' and date_to =='':
        searchResult = inventory_transaction.objects.filter(equipment =equipment_search)
        

        total = searchResult.aggregate(Sum('inventory_amount'))
        
        
        
        
        return render (request,"inventoryList.html", {"inventory_list": searchResult,
                        'total': total['inventory_amount__sum'] })

        
    
    elif equipment_search == '' and inventory_search != '':

        # searchResult = inventory_transaction.objects.raw('SELECT id, inventory_id, quantity,\
        #                                     unit_measurement,inventory_price,inventory_amount,\
        #                                         equipment\
        #                                     from inventory_transaction where \
        #                                     inventory_id like "%'+ inventory_search +'%"' )
        
        searchResult = inventory_transaction.objects.filter(inventory_id =inventory_search)
        

        total = searchResult.aggregate(Sum('inventory_amount'))
        return render (request,"inventoryList.html", {"inventory_list": searchResult,
                        'total': total['inventory_amount__sum'] })


    elif equipment_search =='' and inventory_search == '' and date_from !='' and date_to !='' :

        # searchResult = inventory_db.objects.all()
        # searchResult2 = inventory_db.objects.filter(trans_date__gte =date_to )
        # # searchResult =  inventory_transaction.objects.all()
        # # for i in searchResult:
        # #     z = i.transactions_inventory.trans_date
        # #     print(z)


        # searchResult = inventory_transaction.objects.raw('SELECT id, inventory_id, quantity,\
        #                                     unit_measurement,inventory_price,inventory_amount,\
        #                                         equipment\
        #                                     from inventory_transaction where \
        #                                         trans_date BETWEEN \
        #                                          "'+ date_from +'"  AND "'+ date_to +'"' )
        
        searchResult2 = inventory_transaction.objects.filter(trans_date__lte =date_to).filter(trans_date__gte =date_from)
        
        total = searchResult2.aggregate(Sum('inventory_amount'))
        
        return render (request,"inventoryList.html",{
            "inventory_list": searchResult2, 
            'total': total['inventory_amount__sum']
            })

        # searchResult2 = inventory_transaction.objects.filter(trans_date__lte =date_to).\
        #                 aggregate(Sum('inventory_amount'))
                        
        # searchResult2 = inventory_transaction.objects.filter(trans_date__gte=datetime.date(date_to))
    
        # return render (request,"inventoryList.html",{"inventory_list": searchResult2},
                                    
    
        
    elif equipment_search !='' and inventory_search == '' and date_from !='' and date_to !='' :
        searchResult2 = inventory_transaction.objects.filter(trans_date__lte =date_to) \
            .filter(trans_date__gte =date_from).filter(equipment=equipment_search)
        
        total = searchResult2.aggregate(Sum('inventory_amount'))
        
        return render (request,"inventoryList.html",{
            "inventory_list": searchResult2, 
            'total': total['inventory_amount__sum']
            })
        
        
    elif equipment_search == '' and inventory_search == '':
        total = inventory_transaction.objects.aggregate(Sum('inventory_amount'))
       
        print(total)
        context = {
        'inventory_list': inventory_transaction.objects.all(),
        'total': total['inventory_amount__sum']
        }

        
        return render(request,'inventoryList.html',context)
       
        


    # else:
    #     total = inventory_transaction.objects.aggregate(Sum('inventory_amount'))
    #     context = {
    #     'inventory_list': inventory_transaction.objects.all(),
    #     'total': total['inventory_amount__sum']
    #     }

        
    #     return render(request,'inventoryList.html',context)

def export_excel(request):
    """
    this function  is for exporting excel
    """
    print(request.GET)
    equipment_search = request.GET.get('equipment_id')
    inventory_search = request.GET.get('Inventory_id')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'ID', 'Inventory ID', 'Quantity','Unit','Price',
                        'Equipment'])
    
    
    
    print(date_from)
    if equipment_search and date_from !='' and date_to!='':
        # searchResult = inventory_transaction.objects.filter(equipment = equipment_search)
        searchResult = inventory_transaction.objects.filter(trans_date__lte =date_to) \
        .filter(trans_date__gte =date_from).filter(equipment=equipment_search) 
        for i in searchResult:
            
            writer.writerow([i.trans_date, i.inventory_id,
                            i.quantity, i.unit_measurement,
                            i.inventory_price, i.inventory_amount, i.equipment])
        
        

    if date_from and date_to and equipment_search =='' :
        searchResult = inventory_transaction.objects.filter(trans_date__lte =date_to).filter(trans_date__gte =date_from)
        for i in searchResult:
            writer.writerow([i.trans_date, i.inventory_id,
                            i.quantity, i.unit_measurement,
                            i.inventory_price, i.inventory_amount, i.equipment])
            
    
    if equipment_search  and inventory_search == '' and date_from =='' and date_to =='' :
        
        searchResult = inventory_transaction.objects.filter(equipment=equipment_search) 
        for i in searchResult:
            writer.writerow([i.trans_date, i.inventory_id,
                        i.quantity, i.unit_measurement,
                        i.inventory_price, i.inventory_amount, i.equipment])   
            
    if inventory_search and equipment_search == '' and date_from =='' and date_to =='':
        searchResult = inventory_transaction.objects.filter(inventory_id =inventory_search) 
        for i in searchResult:
            writer.writerow([i.trans_date, i.inventory_id,
                        i.quantity, i.unit_measurement,
                        i.inventory_price, i.inventory_amount, i.equipment]) 
         
        
    return response