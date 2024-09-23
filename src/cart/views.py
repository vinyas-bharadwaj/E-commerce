from django.shortcuts import render

# Create your views here.

# Cart summary
def cart_summary(request):
    return render(request, 'cart/cart-summary.html', {})


# Adding an item to cart
def cart_add(request):
    pass

# Deleting an item from cart
def cart_delete(request):
    pass

# Updating an item in cart
def cart_update(request):
    pass


