from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def listing(request, id):
    listing_data = Listing.objects.get(pk=id)
    listing_in_watchlist = request.user in listing_data.watchlist.all()
    is_owner = request.user.username == listing_data.owner.username
    all_comments = Comment.objects.filter(listing=listing_data)

    return render(request, 'auctions/listing.html', {
        "listing":listing_data,
        "listing_in_watchlist":listing_in_watchlist,
        "all_comments":all_comments, 
        "is_owner":is_owner
    })




def close(request, id):
    listing_data = Listing.objects.get(pk=id)
    listing_data.active = False
    listing_data.save()

    is_owner = request.user.username == listing_data.owner.username
    listing_in_watchlist = request.user in listing_data.watchlist.all()
    return render(request, "auctions/listing.html", {
            "listing":listing_data, 
            "message":"Auction Closed",
            "is_owner":is_owner,
            "new":True
           
            })

 


def add_comment(request, id):
    current_user = request.user
    listing_data = Listing.objects.get(pk=id)
    message = request.POST['new_comment']
    new_comment = Comment(
        writer = current_user,
        listing = listing_data,
        message = message
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def watchlistRemove(request, id):
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    listing_data.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def watchlistAdd(request, id):
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    listing_data.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def show_watchlist(request):
    current_user = request.user
    listings = current_user.relatedwatchlist.all()
    return render(request, "auctions/watchlist.html",{
        "listings":listings
    }
    )



def index(request):
    active_listings = Listing.objects.filter(active=True)
    Categories = Category.objects.all()
    return render(request, "auctions/index.html",
    {
        "listings":active_listings,
        "categories": Categories
    })

def particular_Category(request):
    if request.method == 'POST':
        form_Category = request.POST['category']
        category = Category.objects.get(category_name = form_Category)

        active_listings = Listing.objects.filter(active=True, category=category)
        Categories = Category.objects.all()
        return render(request, "auctions/index.html",
        {
            "listings":active_listings,
            "categories": Categories
        })

def create_Listing(request):
    if request.method == 'GET':
        Categories = Category.objects.all()
        return render(request, 'auctions/create.html',{
            "categories": Categories
        })
    else:
        title = request.POST['title']
        description = request.POST['description']
        image_url = request.POST['image_url']
        price = request.POST['price']
        category = request.POST['category']

        current_user = request.user
        category_Data = Category.objects.get(category_name = category)
        bid = Bid(bid=int(price), user=current_user)
        bid.save()
        new_Listing = Listing(
            title=title,
            description = description, 
            image_url = image_url,
            price = bid, 
            category = category_Data, 
            owner = current_user
        )
        new_Listing.save()
        return HttpResponseRedirect(reverse(index))

def add_bid(request, id):
    listing_data = Listing.objects.get(pk=id)
    # if 'higherbid' in request.POST:
    higherbid = request.POST.get('higherbid', False)
    all_comments = Comment.objects.filter(listing=listing_data)

    listing_in_watchlist = request.user in listing_data.watchlist.all()
    is_owner = request.user.username == listing_data.owner.username
        
    if int(higherbid) > int(listing_data.price.bid):
        renew_bid = Bid(user=request.user, bid=int(higherbid))
        renew_bid.save()
        listing_data.price = renew_bid
        listing_data.save()
        return render(request, "auctions/listing.html", {
            "listing":listing_data, 
            "message":"New Bid Added!", 
            "listing_in_watchlist":listing_in_watchlist,
            "new":True,
            "all_comments":all_comments,
            "is_owner":is_owner
            
        })
    
    
    else:
        return render(request, "auctions/listing.html", {
            "listing":listing_data, 
            "message":"Bid Not Added!",
            "new":False 
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
