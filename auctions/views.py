from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User
from .models import Listing, Bid, WatchList, Comment
from .forms import CreateListingForm



def index(request):
    return render(request, "auctions/index.html", {
        "items": Listing.objects.all(),
        "bids" : Bid.objects.all(),
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

@login_required
def watchlist(request):
    # choose all items watched by the user
    watch = WatchList.objects.filter(watcher=request.user)
    return render(request, "auctions/watchlist.html", {
        "watch" : watch
    })

@login_required
def categories(request):
    category_list = []
    listings = Listing.objects.all()
    for listing in listings:
        if listing.category:
            if listing.category not in category_list:
                category_list.append(listing.category)

    return render(request, "auctions/categories.html",{
        'listings' : listings,
        'category_list' : category_list,
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            starting_bid = form.cleaned_data['starting_bid']
            image_url = form.cleaned_data['image_url']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            user = request.user
            item = Listing(item=name, owner=user, starting_bid=starting_bid, current_bid=starting_bid, image_url=image_url, description=description, category=category.capitalize())
            item.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            form = CreateListingForm()
    return render(request, "auctions/create_listing.html", {
        'form': CreateListingForm(),
    })

@login_required(login_url='login')
def view_listing(request, item_id):
    user = request.user
    listing = Listing.objects.get(pk=item_id)
    u_watchlist = WatchList.objects.filter(watcher=user)
    # determine if item is in the watchlist of user
    watch_found = False
    for w in u_watchlist:
        if w.items.item == listing.item:
            watch_found = True
    # get the comments for this item
    comments = Comment.objects.filter(item=listing)
    return render (request, "auctions/view_listing.html", {
        "listing": listing,
        "watch_found" : watch_found,
        "listings": Listing.objects.all(),
        "bids" : Bid.objects.all(),
        "u_watchlist": u_watchlist,
        "watchlist" : WatchList.objects.all(),
        "comments" : comments,
    })

@login_required
def close_listing(request, item_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=item_id)
        listing.active = False
        listing.winner = listing.current_bidder
        listing.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def make_bid(request, item_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=item_id)
        user = request.user
        bid_amount = float(request.POST['bid_amount'])
        if bid_amount > listing.current_bid:
            listing.current_bid = bid_amount
            listing.current_bidder = user
            listing.save()
            bid = Bid(item=listing, bidder=user, amount=bid_amount)
            bid.save()
            return HttpResponseRedirect(reverse("view_listing", args=(item_id,)))
        else:
            return HttpResponseRedirect(reverse("bid_message"))
    return render(request, "auctions/view_listing.html", {
        #'listing' : listing,
        #'bid' : bid,
    })

@login_required
def watch_add(request, item_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=item_id)
        user = request.user
        watch = WatchList(watcher=user, items=listing,)
        watch.save()
    return HttpResponseRedirect(reverse("view_listing", args=(item_id,)))

@login_required
def watch_remove(request, item_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=item_id)
        user = request.user
        watch_r = WatchList.objects.filter(watcher=user).filter(items=listing)
        watch_r.delete()
    return HttpResponseRedirect(reverse("view_listing", args=(item_id,)))

@login_required
def add_comment(request, item_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=item_id)
        user = request.user
        u_comment = request.POST['comment_box']
        comment_input = Comment(item=listing, user=user, comment=u_comment)
        comment_input.save()
        return HttpResponseRedirect(reverse("view_listing", args=(item_id,)))  
    return HttpResponseRedirect(reverse("view_listing", args=(item_id,)))

@login_required
def closed_auctions(request):
    listings = Listing.objects.all()
    user = request.user
    return render(request, "auctions/closed_auctions.html", {
        "listings" : listings,
        "user" : user
    })

@login_required
def my_auctions(request):
    user = request.user
    listings = Listing.objects.filter(winner=user)
    return render(request, "auctions/my_auctions.html", {
        "listings" : listings,
    })
        

@login_required
def category_list_page(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/category_list_page.html", {
        "category": category,
        "listings": listings,
    })

@login_required
def bid_message(request):
    return render(request, "auctions/bid_message.html")