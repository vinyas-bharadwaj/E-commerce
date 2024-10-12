from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .forms import SignUpForm, UpdateProfileForm, UpdatePasswordForm, UpdateInfoForm
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress

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

# Redirect to the search page
def search_redirect(request):
	search_query = request.GET.get('q')

	if search_query:
		return redirect(reverse('search', kwargs={'item': search_query}))
	
	return redirect('home')

# Search for a product
def search(request, item: str):
	# Q - essentially just allows us to have multiple conditions for the same query	
	products = Product.objects.filter(Q(name__icontains=item) | Q(description__icontains=item))

	if not products:
		messages.success(request, 'There seems to be no product with that name, please try again')
		return render(request, 'store/search.html', {})
	
	return render(request, 'store/search.html', {'products': products})

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

# Update the user info
def update_info(request):
	if request.user.is_authenticated:
		# Get current user
		current_user = Profile.objects.get(user__id=request.user.id)

		# Get current user's shipping info
		shipping_info = ShippingAddress.objects.get(user__id=request.user.id)

		# User info form
		form = UpdateInfoForm(request.POST or None, instance=current_user)

		# Shipping form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_info)

		if form.is_valid() or shipping_form.is_valid():
			form.save()
			shipping_form.save()

			messages.success(request, 'User info successfully updated')
			return redirect('home')
		
		return render(request, 'store/update-info.html', {'form': form, 'shipping_form': shipping_form})

	messages.success(request, 'Must be logged in to update user info')
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

			# Check the shopping cart details
			curr_user = Profile.objects.get(user__id=request.user.id)

			# Get their saved cart from database
			saved_cart = curr_user.old_cart

			# Convert database string to python dictionary
			if saved_cart:
				# Convert to dictionary using json
				converted_cart = json.loads(saved_cart)

				# Add loaded cart dictionary to our current users session
				cart = Cart(request)

				for key, val in converted_cart.items():
					cart.db_add(product=key, quantity=val)

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

