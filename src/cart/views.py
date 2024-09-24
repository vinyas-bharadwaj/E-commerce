from django.shortcuts import render, get_object_or_404
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

    context = {'cart_products': cart_products, 'quantities': quantities}

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

        # Return a response
        response = JsonResponse({'quantity': cart_quantity})
        return response

# Deleting an item from cart
def cart_delete(request):
    pass

# Updating an item in cart
def cart_update(request):
    pass


