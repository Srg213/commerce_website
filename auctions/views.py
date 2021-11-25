from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User , Listing, Bid ,Comments
from django import forms
from django.db.models import Max


def index(request):
    if request.method == 'POST':
        id = request.POST['listing.id']
        item = Listing.objects.get(id = id)
        item.state = False
        item.save()
        print(item.state)  
    return render(request, "auctions/index.html",{ 'listings' : Listing.objects.all()})


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
        #Attempt to create new user
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


@login_required(login_url = '/login')
def create_listing(request):
    if request.method == "POST":
        title= request.POST['title']
        description = request.POST['description']
        starting_bid = request.POST['first_bid']
        image = request.POST['image']
        category = request.POST['category']
        f=Listing(title=title, description =description,starting_bid=starting_bid,image= image,category=category ,creator = request.user)
        f.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request,"auctions/create.html" )


@login_required(login_url = '/login')
def item(request , listing_id):
    l = Listing.objects.get(id = listing_id)
    if  l.state:
        m = l.new_bids.all()
        try:
            max= l.new_bids.first().price
            max_bidder = l.new_bids.first().user
            for i in m:
                if i.price > max:
                    max = i.price
                    max_bidder = i.user
            number_bid = len(m)
            if str(max_bidder) == User.objects.get(id = request.user.id).username :
                max_bidder = 'you'
        except: 
            max = l.starting_bid
            max_bidder = ''
            number_bid = 0

        a = Listing.objects.get(id = listing_id) 
        b = User.objects.get(id = request.user.id)
        if request.method == "POST":
            bid = request.POST['Bid']                
            if int(bid) > int(a.starting_bid)  :     
                k = Bid(user = b, item =a ,price=bid)
                k.save()
                return HttpResponseRedirect(f'/listings/{listing_id}')
            else:
                return render(request ,"auctions/listing.html", {'listing' : l ,'max' : max , 'max_bidder': max_bidder ,'number_bid':number_bid ,'message' :'Place a bid greater than starting bid'})
        else:
            pass

        if str(a.creator) == str(b.username):
            return render(request, "auctions/listing.html" , {'listing': l , 'max': max, 'max_bidder': max_bidder ,'number_bid':number_bid , 'Close':True})
      
        return render(request ,"auctions/listing.html", {'listing' : l ,'max' : max , 'max_bidder': max_bidder ,'number_bid':number_bid })

    else:
        m = Bid.objects.filter(item = l).aggregate(Max('price'))['price__max']
        max_bidder = Bid.objects.filter(price = m)[0]
        return render(request ,"auctions/listing.html", {'listing' : l ,"max": max_bidder.price,"max_bidder": max_bidder.user, "message" : 'Bid closed.' })

@login_required(login_url = '/login')
def watchlist(request): 
    z = request.user.id
    try:
        listing_id = request.POST['listing.id']
        l = Listing.objects.get(id = listing_id)
        l.customer.add(z)
    except:
        pass
    a = User.objects.get(id = z)
    p = a.watchlist.all()
    return render(request , "auctions/watchlist.html" , {'listing' : p } )


def comments(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        item = request.POST['listing.id']
        user = User.objects.get(user= request.user.id)
        listing = Listing.objects.get(id = item)
        a = Comment(user = user, comments = listing, text = comment)
        return render(reverse('listing' , item))