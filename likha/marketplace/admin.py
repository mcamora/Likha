from django.contrib import admin

# Register your models here.
from .models import *

# Unregister models first to avoid AlreadyRegistered error
if admin.site.is_registered(OrderItem):
    admin.site.unregister(OrderItem)

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

