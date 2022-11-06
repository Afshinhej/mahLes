from django.contrib import admin

from .models import Category, Auction_listing, User
# Register your models here.

admin.site.register(Category)
admin.site.register(Auction_listing)
admin.site.register(User)