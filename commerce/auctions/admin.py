from django.contrib import admin

from .models import Category, Auction, User, Seller
# Register your models here.

admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(User)
admin.site.register(Seller)