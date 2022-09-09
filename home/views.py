from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Inventory1

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
            messages.error(
                request, 'Login failed! Wrong credentials', extra_tags='danger')
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
        return render(request, 'change_password.html')
    return render(request, 'change_password.html')


def add_material(request, inv_id):
    if request.user.is_anonymous:
        return redirect('/')
    if request.method == "POST":
        material_code = request.POST.get('material_code')
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
