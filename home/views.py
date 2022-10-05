from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Inventory1, Transactions
from .forms import TransactionsForm
from decimal import *
import datetime
from django.db import IntegrityError
from django.db.models import Q

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
        try:
            inv1_object = Inventory1(inv_id=inv_id, material_code=material_code,
                                     material_name=material_name, balance=balance, unit=unit, remark=remark)
            inv1_object.save()
            trans = Transactions(inv_id=inv_id, material_code=material_code, material_name=material_name, unit=unit,
                                 in_out='IN', quantity=balance, balance=balance, issued_to='Stock added first time', remark=remark)
            trans.save()
            messages.success(request, 'material added')
        except IntegrityError:
            messages.error(
                request, 'Error! material not added because material code already exists')
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
    form = TransactionsForm()
    if request.method == 'POST':
        if (request.POST['in_out']) == 'IN':
            new_balance = material.balance + \
                abs(Decimal(request.POST['quantity']))
        else:
            new_balance = material.balance - \
                abs(Decimal(request.POST['quantity']))
        material.balance = new_balance
        material.save()
        newTrans = Transactions(inv_id=inv_id, material_code=mat_code, material_name=material.material_name, unit=material.unit,
                                in_out=request.POST['in_out'], quantity=abs(Decimal(request.POST['quantity'])), balance=new_balance, issued_to=request.POST['issued_to'], remark=request.POST['remark'])
        newTrans.save()
        messages.success(request, 'material issued ')
    mat_trans = Transactions.objects.filter(
        inv_id=inv_id, material_code=mat_code)
    context = {'form': form, 'mat_trans': mat_trans, 'inv_id': inv_id,
               'mat_code': mat_code, 'mat_name': material.material_name, 'balance': material.balance, 'unit': material.unit}
    return render(request, 'transactions.html', context)


def alltransactions(request):
    endDate = datetime.datetime.now()
    currentDate = datetime.date.today()
    startDate = datetime.datetime(currentDate.year, currentDate.month, 1)
    if request.method == 'POST':
        startDate = request.POST['from']
        endDate = request.POST['to']
        format = '%Y-%m-%d'
        startDate = datetime.datetime.strptime(startDate, format)
        endDate = datetime.datetime.strptime(endDate, format)
    alltrans = Transactions.objects.filter(
        dateTime__date__range=(startDate, endDate))
    return render(request, 'all_transactions.html', {'alltrans': alltrans, 'from': startDate, 'to': endDate})


def search(request):
    if request.user.is_anonymous:
        return redirect('/')
    if request.method == 'GET':
        q = request.GET['q']
        q_results = Inventory1.objects.filter(
            Q(material_code__icontains=q) | Q(material_name__icontains=q))
        context = {
            'q_results': q_results,
            'q': q
        }
        return render(request, 'search.html', context)
