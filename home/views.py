from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Inventory1, Transactions
from .forms import TransactionsForm
from decimal import *
# Create your views here.


def index(request):
    if (not request.user.is_anonymous):
        return render(request, 'home.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user = authenticate(username=username, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, 'Login failed! Wrong credentials')
            return render(request, 'index.html')
    return render(request, 'index.html')


def home(request):
    if request.user.is_anonymous:
        return redirect('/')
    return render(request, 'home.html')


def help(request):
    if request.user.is_anonymous:
        return redirect('/')
    return render(request, 'help.html')


def logoutUser(request):
    logout(request)
    return redirect('/')


def change_password(request):
    if request.user.is_anonymous:
        return redirect('/')
    if request.method == "POST":
        pwd = request.POST.get('pwd1')
        u = User.objects.get(username=request.user)
        u.set_password(pwd)
        u.save()
        messages.success(request, 'password changed')
        return redirect('/')
    return render(request, 'change_password.html')


def add_material(request, inv_id):
    if request.user.is_anonymous:
        return redirect('/')
    if request.method == "POST":
        material_code = request.POST['material_code']
        material_name = request.POST.get('material_name')
        balance = request.POST.get('balance')
        unit = request.POST.get('unit')
        remark = request.POST.get('remark')
        inv1_object = Inventory1(inv_id=inv_id, material_code=material_code,
                                 material_name=material_name, balance=balance, unit=unit, remark=remark)
        inv1_object.save()
        messages.success(request, 'material added')
        materials = Inventory1.objects.filter(inv_id=inv_id)
        context = {'materials': materials, 'inv_id': inv_id}
        return render(request, 'inventory.html', context)


def inventory(request, inv_id):
    if request.user.is_anonymous:
        return redirect('/')
    materials = Inventory1.objects.filter(inv_id=inv_id)
    context = {'materials': materials, 'inv_id': inv_id}
    return render(request, 'inventory.html', context)


def transactions(request, inv_id, mat_code):

    if request.user.is_anonymous:
        return redirect('/')
    material = Inventory1.objects.get(material_code=mat_code)
    mat_trans = Transactions.objects.filter(
        inv_id=inv_id, material_code=mat_code)
    form = TransactionsForm()
    if request.method == 'POST':
        new_balance = material.balance-Decimal(request.POST['quantity'])
        material.balance = new_balance
        material.save()
        form_data = Transactions(balance=new_balance, inv_id=inv_id,
                                 material_code=mat_code, material_name=material.material_name)
        form = TransactionsForm(request.POST, instance=form_data)
        # print(form)
        if form.is_valid():
            # save the form data to model
            form.save()
            messages.success(request, 'material issued ')
        else:
            messages.success(request, 'form is not valid ')

    context = {'form': form, 'mat_trans': mat_trans, 'inv_id': inv_id,
               'mat_code': mat_code, 'mat_name': material.material_name, 'balance': material.balance, 'unit': material.unit}
    return render(request, 'transactions.html', context)
