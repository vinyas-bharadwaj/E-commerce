from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.

# Cart summary
def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_products()
	quantities = cart.get_quantity()
	total = cart.total()

	context = {'cart_products': cart_products, 'quantities': quantities, 'total': total}

	return render(request, 'cart/cart-summary.html', context=context)


# Adding an item to cart
def cart_add(request):
	# Get the cart
	cart = Cart(request)

	# Test for POST
	if request.POST.get('action') == 'post':
		# Get data
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		# Lookup product in the database
		product = get_object_or_404(Product, id=product_id)

		# Save to session
		cart.add(product=product, quantity=product_qty)

		# Get cart quantity
		cart_quantity = cart.__len__()

		# Flash a message stating that the operation was successful
		messages.success(request, f'Added {product.name} to cart successfully')

		# Return a response
		response = JsonResponse({'quantity': cart_quantity})
		return response

# Deleting an item from cart
def cart_delete(request):
	cart = Cart(request)

	if request.POST.get('action') == 'post':
		product_id = int(request.POST.get('product_id'))

		cart.delete(product=product_id)

		messages.success(request, f'Item removed successfully')

		response = JsonResponse({'id': product_id})

		return response

# Updating an item in cart
def cart_update(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		cart.update(product=product_id, quantity=product_qty)
		messages.success(request, 'Item updated successfully')

		response = JsonResponse({'qty':product_qty})
		return response


