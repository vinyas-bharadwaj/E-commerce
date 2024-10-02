from store.models import Product

class Cart():
	def __init__(self, request) -> None:
		self.session = request.session  

		# Get the current session key if it exists
		cart = self.session.get('session_key') # Returns none if session key is not found


		# If the user is new, we need to create a session key
		if 'session_key' not in request.session:
			cart = self.session['session_key'] = {}

		# Make sure the cart is available on all pages of the website
		self.cart = cart

	def add(self, product, quantity):
		product_id = str(product.id)
		product_qty = str(quantity)

		if product_id not in self.cart:
			self.cart[product_id] = int(product_qty)

		self.session.modified = True


	def update(self, product, quantity):
		product_id = str(product)
		product_qty = int(quantity)

		# Get cart
		ourcart = self.cart
		# Update Dictionary/cart
		ourcart[product_id] = product_qty

		self.session.modified = True
	
	def delete(self, product):
		product_id = str(product)

		if product_id in self.cart:
			del self.cart[product_id]

		self.session.modified = True

	def __len__(self):
		return len(self.cart)
	

	def get_products(self):
		# Get ID's from cart
		product_ids = self.cart.keys()

		# Use the ID's to lookup products in the database
		products = Product.objects.filter(id__in=product_ids)

		return products

	def get_quantity(self):
		quantities = self.cart
		return quantities
	
	def total(self):
		# Get product IDs
		product_ids = self.cart.keys()

		# Lookup those IDs in our products model
		products = Product.objects.filter(id__in=product_ids) 

		# Get quantities
		quantities = self.cart

		res = 0
		for key, val in quantities.items():
			# Key is the ID of the product (string)
			# Val is the quantity of the product (int)
			for product in products:
				if str(product.id) == key:
					if product.is_sale:
						res += product.sale_price * val
					else:
						res += product.price * val

		return res