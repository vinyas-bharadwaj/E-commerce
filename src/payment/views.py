from django.shortcuts import render
from cart.cart import Cart

# Create your views here.
def payment_success(request):
	return render(request, 'payment/payment-success.html', {})

def checkout(request):
	cart = Cart(request)
	cart_products = cart.get_products()
	quantities = cart.get_quantity()
	total = cart.total()

	context = {'cart_products': cart_products, 'quantities': quantities, 'total': total}

	return render(request, 'payment/checkout.html', context=context)