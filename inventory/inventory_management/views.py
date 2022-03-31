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