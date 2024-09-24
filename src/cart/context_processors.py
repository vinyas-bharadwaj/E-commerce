from .cart import Cart

# Create a context processor so our cart is available on all pages of the site
def cart(request):
    # Reurn the default data from our cart
    return {'cart': Cart(request)}