from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Product, ConsumedProduct
from .forms import ProductForm, ConsumedProductForm, UserRegisterForm
from datetime import date
from django.shortcuts import get_object_or_404

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

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def product_list(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'nutrition/product_list.html', {'products': products})

@login_required
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

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)
    
    if request.method == 'POST':
        product.delete()
        # messages.success(request, 'Продукт успешно удален!')
        return redirect('product_list')
    
    return render(request, 'nutrition/delete_confirm.html', {'product': product})


@login_required
def add_consumed_product(request):
    if request.method == 'POST':
        form = ConsumedProductForm(request.user, request.POST)
        if form.is_valid():
            consumed_product = form.save(commit=False)
            consumed_product.user = request.user
            consumed_product.date = timezone.now().date()
            consumed_product.save()
            return redirect('daily_stats')
    else:
        form = ConsumedProductForm(request.user)
    return render(request, 'nutrition/add_consumed_product.html', {'form': form})

@login_required
def daily_stats(request):
    today = date.today()
    consumed = ConsumedProduct.objects.filter(user=request.user, date=today)
    
    total_calories = sum(item.total_calories for item in consumed)
    total_protein = sum(item.total_protein for item in consumed)
    total_fat = sum(item.total_fat for item in consumed)
    total_carbs = sum(item.total_carbs for item in consumed)
    
    return render(request, 'nutrition/daily_stats.html', {
        'consumed': consumed,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_fat': total_fat,
        'total_carbs': total_carbs,
        'today': today.strftime('%d.%m.%Y')
    })