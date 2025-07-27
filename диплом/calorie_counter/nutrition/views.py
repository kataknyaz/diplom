from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.base import RedirectView
from .models import Product, ConsumedProduct
from .forms import ProductForm, ConsumedProductForm, UserRegisterForm
from datetime import date

def home(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('product_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            return render(request, 'registration/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'registration/login.html')

def product_list(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'nutrition/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'nutrition/add_product.html', {'form': form})

def daily_stats(request):
    today = date.today()
    consumed = ConsumedProduct.objects.filter(user=request.user, date=today)
    total_calories = sum(item.total_calories for item in consumed)
    return render(request, 'nutrition/daily_stats.html', {
        'consumed': consumed,
        'total_calories': total_calories,
        'today': today
    })
