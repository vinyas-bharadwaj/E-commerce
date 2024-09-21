from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.

# Home page
def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/home.html', context=context)

# About page
def about(request):
    context = {}
    return render(request, 'store/about.html', context=context)


# Login page
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('home')
        else:
            messages.success(request, "There was an error, please try again")
            return redirect('login')

    else:
        return render(request, 'store/login.html', {})

# Logout page
def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')