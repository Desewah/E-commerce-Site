from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import datetime
from .forms import *
from .models import *

def index(request):
    """
    The default route of your web application should let 
    users view all of the currently active auction listings.
    """
    active_listings = AuctionListing.objects.filter(active_user=True)
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "index": "index"
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

def create_listing(request):
    """
    Users should be able to visit a page 
    to create a new listing
    """
    if request.method == "POST":
        current_price = request.POST.get("current_price", False)
        listing_form = ListingForm(request.POST)
        bid = Bid(bid=float(current_price), bidder=request.user)
        bid.save()
        if listing_form.is_valid():
            title = listing_form.cleaned_data["title"]
            description = listing_form.cleaned_data["description"]
            category = listing_form.cleaned_data["category"]
            
            image_url = listing_form.cleaned_data["image_url"]
            auction = AuctionListing(
                user = User.objects.get(pk=request.user.id), 
                title = title, 
                description = description, 
                category=category, 
                current_price = bid,
                image_url =image_url)
            auction.save()
            return HttpResponseRedirect(reverse(index))
        else:
            return render(request, "auctions/create_listing.html", {
                "listing_form": listing_form
            })
    """
    if request.method == GET,
    display a new entry form
    """

    return render(request, "auctions/create_listing.html", {
        "listing_form": ListingForm()
    })


def categories(request):
    """
    Users should be able to visit a page that displays a list of all listing categories.
    """
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def display_listing(request, category_id):
    """
     Clicking on the name of any category should 
     take the user to a page that displays all 
     of the active listings in that category.
    """
    categories = Category.objects.get(pk=category_id)
    active_listings = AuctionListing.objects.filter(active_user=True, category=categories)
    return render(request, "auctions/index.html", {
        "categories": categories,
        "index": "categories",
        "active_listings": active_listings,
        "non_categories": Category.objects.exclude(category=categories).all()
    })

def listing(request, listing_id):
    """
    Clicking on a listing should take users 
    to a page specific to that listing.
    """
    
    listing_details = get_object_or_404(AuctionListing, pk=listing_id)
    seller = request.user.username == listing_details.user.username
    watchlist = request.user in listing_details.watchlist.all()
    comments = CommentSection.objects.filter(post=listing_details)
    author = CommentSection.author
    return render(request, "auctions/listing.html", {
        "listing_details": listing_details,
        "watchlist": watchlist,
        "comment_form" : CommentForm(),
        "comments": comments,
        "bid_form": BidForm,
        "seller": seller,
        "author": author,
    })

def watchlist_action(request, id):
    """
    If the user is signed in, the user should be able to add the 
    item to their “Watchlist.” If the item is already on the 
    watchlist, the user should be able to remove it.
    """
    listing_details = AuctionListing.objects.get(pk=id)
    current_user= request.user
    if request.POST.get("add", False):
        listing_details.watchlist.add(current_user)
    else:
        listing_details.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse(listing, args={id, }))

def watchlist(request):
    current_user = request.user
    watchlist = current_user.watchlist.all()
    if len(watchlist) >= 1:
        no = len(watchlist)
    else:
        no = 0
    return render(request, "auctions/index.html", {
        "active_listings": watchlist,
        "index": "list",
        "no" : no
    })



def comment_section(request, id):
    """
    Users who are signed in should be able to add comments to 
    the listing page. The listing page should display all 
    comments that have been made on the listing.
    """
    listing_details = AuctionListing.objects.get(pk=id)
    comments = CommentSection.objects.filter(post=listing_details)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.time_created = datetime.date.today()
            new_comment.post = listing_details
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    return render(request, "auctions/listing.html", {
        "listing_details": listing_details,
        "watchlist": watchlist,
        "comment_form" : CommentForm(),
        "comments": comments,
        "bid_form": BidForm,
    })

def place_bid(request, id):

    if request.method == "POST":
        bid_details = BidForm(request.POST)
        if bid_details.is_valid():
            updated_bid = bid_details.cleaned_data["bid"]

        else:
            return render(request, "auctions/listing.html", {
                "bid_details": bid_details
            })
    listing_details = get_object_or_404(AuctionListing, pk=id)
    if int(updated_bid) > int(listing_details.current_price.bid):
        new_bid = Bid(bid=updated_bid, bidder=request.user)
        new_bid.save()
        listing_details.current_price = new_bid

        listing_details.save()
        return render(request, "auctions/listing.html", {
            "listing_details": listing_details,
            "message": "Bid updated successfully",
            "update": True,

            "bid_form": BidForm(),
            "comment_form": CommentForm(),
            
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing_details": listing_details,
            "message": "Bid update wasn't successful, bid with a price higher than the current bid",
            "update": False,
            "bid_form": BidForm(),
            "comment_form": CommentForm(),
        })
    

def close_auction(request, id):
    listing_details = get_object_or_404(AuctionListing, pk=id)
    comments = CommentSection.objects.filter(post=listing_details)
    author = CommentSection.author
    
    seller = request.user.username == listing_details.user.username
    listing_details.active_user = False
    listing_details.save()
    return render(request, "auctions/listing.html", {
            "listing_details": listing_details,
            "message": "Auction successfully closed",
            "update": True,
            "bid_form": BidForm(),
            "comments": comments,
            "seller": seller,
            "comment_form": CommentForm(),
        })

def inactive_auctions(request):
    inactive_listings  = AuctionListing.objects.filter(active_user=False)
    return render(request, "auctions/index.html", {
        "active_listings": inactive_listings,
        "index": "inactive",
        "count": len(inactive_listings),
    })

    