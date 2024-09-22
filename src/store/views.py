from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.

# Home page
def home(request):
	products = Product.objects.all()
	categories = Category.objects.all()
	context = {'products': products, 'categories': categories}
	return render(request, 'store/home.html', context=context)

# About page
def about(request):
	return render(request, 'store/about.html', {})

# Product details page
def product_details(request, pk):
	product = Product.objects.get(id=pk)
	context = {'product': product}
	return render(request, 'store/product.html', context=context)

# Products filtered by category
def category_products(request, cat):
	cat = cat.replace('-', ' ')
	try:
		category = Category.objects.get(name=cat)
		products = Product.objects.filter(category=category)
	except:
		messages.success(request, 'Products with that category do not exist')
		return redirect('home')

	categories = Category.objects.all()
	context = {'products': products, 'categories': categories, 'category': cat}
	return render(request, 'store/category-products.html', context=context)

# Register page
def register_user(request):
	form = SignUpForm()
	  
	if request.method == "POST":
		form = SignUpForm(request.POST)
			
		if form.is_valid():
			form.save()
			messages.success(request, ("Successfully registered user"))
			return redirect('login')
		
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')

	return render(request, 'store/register.html', {'form': form})
	
# Login page
def login_user(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
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

