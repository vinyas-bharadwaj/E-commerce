from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Product, Category
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignUpForm, UpdateProfileForm, UpdatePasswordForm

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
			messages.success(request, 'There seems to be some problem, please try again')
			return redirect('register')

	return render(request, 'store/register.html', {'form': form})

# Update user profile
def update_profile(request):
	if request.user.is_authenticated:
		current_user = request.user
		form = UpdateProfileForm(request.POST or None, instance=current_user)

		if form.is_valid():
			form.save()

			login(request, current_user)
			messages.success(request, 'Profile successfully updated')
			return redirect('home')
		
		return render(request, 'store/update-user.html', {'form': form})

	messages.success(request, 'Must be logged in to update profile')
	return redirect('home')

# Update user password
def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user

		if request.method == 'POST':
			form = UpdatePasswordForm(current_user, request.POST)

			if form.is_valid():
				form.save()
				messages.success(request, 'Password updated successfully, please login again')
				return redirect('login')
			
			else:
				for err in list(form.errors.values()):
					messages.error(request, err)
				return redirect('update-password')
		
		else:
			form = UpdatePasswordForm(current_user)
			return render(request, 'store/update-password.html', {'form': form})
		
	messages.success(request, 'Must be logged in to reset password')
	return redirect('home')
	
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

