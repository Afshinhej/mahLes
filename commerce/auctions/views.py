from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction_listing

# To derive a list of specefic feature (column) from a table (query set) 
def derive(Queryset, requested_field): # requestd_firld has to be 'str'.
    result = []
    for _ in Queryset.objects.values(requested_field):
        result.append(_[requested_field])
    return result


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction_listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def auction(request, auction_title):
    existing_titles = list(map(str.upper, derive(Auction_listing, 'title')))
    if auction_title.upper() in existing_titles:
        auction_index = existing_titles.index(auction_title.upper())
        return render(request, "auctions/auction.html",{
            "auction_listing": Auction_listing.objects.get(pk=1+auction_index)
        })

    return render(request, "auctions/auction.html",{
            "auction_listing": Auction_listing.objects.get(pk=1+auction_index)
        })
