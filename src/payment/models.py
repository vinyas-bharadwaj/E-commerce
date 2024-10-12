from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_name = models.CharField(max_length=255)
    shipping_email = models.EmailField(null=True, blank=True)
    shipping_phone = models.CharField(max_length=255, null=True, blank=True)
    shipping_address = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255)
    shipping_country = models.CharField(max_length=255)

    def __str__(self):
        return f"Shipping Address - {self.shipping_name}"

    class Meta:
        # Essentially changes the display name in django-admin panel
        verbose_name_plural = "Shipping Address"
