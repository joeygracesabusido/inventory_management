from django.shortcuts import render,redirect

# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages, auth

from .models import equipment

from django.shortcuts import HttpResponse

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def ajax_test(request):
    if is_ajax(request=request):
        message = "This is ajax"
    else:
        message = "Not ajax"
    return HttpResponse(message)



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
        mrs_no = request.POST.get('mrs')
        requested_by = request.POST.get('requested_by')
      
        # journal_save = Journal.objects.create(
        #     trans_date = trans_date,
        #     ref = ref,
        #     memo = memo
        # )
        
        data_ = dict(request.POST.lists())
        data_.pop('csrfmiddlewaretoken')
        data_.pop('inventory_date')
        data_.pop('transType')
        data_.pop('mrs')
        data_.pop('requested_by')
        
        print(data_)
        entry = len(data_['inventory_id'])
        
        # for k in data_.items():
        #     print(k)
    
        # result = []
        # for i in range(entry):
        #     d={}
        #     for j,k in enumerate(data_.items()):
        #         if j == 0:
        #             d['gl_type']= (k[1][i])
        #         elif j == 1:
        #             d['tx_type']= (k[1][i])
        #         elif j == 2:
        #             d['amount']= (k[1][i])
        #     result.append(d)


        # for r in result:
        #     Transaction.objects.create(
        #         journal = journal_save,
        #         tx_type = r['tx_type'],
        #         gl_account_id = r['gl_type'],
        #         amount = r['amount']
        #     )

            # print(type(k[0]))
            # print(k[1])
            
        #     for i, val in enumerate(k[1]):
        #         print(k[1][i])
            # print(type(k['BalanceSheetType']))
            # print(type(k['BalanceSheetType'][0]))
        # for i, val in enumerate(gl_account):
        #     print(i)
        
            
            
            # db_save = Transaction.objects.create(
            #     journal = journal_save,
            #     tx_type = trans_date,
            #     gl_account = ref,
            #     amount = memo
            # )
    
        return redirect('/')
        # return render(request,'choices.html')
    
    
    
    return render(request,'inventory.html')