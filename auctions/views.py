from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Comment, User,Listing,Bid, Watchlist
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .util import *
from django.db.models import Q




class NewTaskForm(forms.Form):
    title= forms.CharField(label = "",widget=forms.TextInput(attrs={ "class": "search", "placeholder": "Title of the listing"}))


class NewTextForm(forms.Form):
    description= forms.CharField(label="", widget=forms.Textarea(attrs={ "class": "form-control mb-4", "placeholder": "Please enter the discription about the listing","rows":"4", "cols":"10"} ))


class NewValueForm(forms.Form):
    value = forms.FloatField(required=False, min_value=0, widget=forms.NumberInput(attrs={'step': "0.01","placeholder":"0.00"}))



'''
def new_lisitng(request): 
    if not request.user.is_authenticated: 
         return HttpResponse("Please Sign in")  
    
    
    return render(request, "auctions/create_listing.html", {
                    "discription" : NewTextForm(auto_id="id_%s"), # loads the create page with just textarea in it. 
                    "title": NewTaskForm(auto_id="id_%s_2"),
                    "price":NewValueForm(auto_id="pid_%s_1")
        })'''

@login_required(login_url='/login')
def new_lisitng(request):

    if request.method == "POST": # If the form has been submitted...

        current_user = request.user
        id_user = current_user.id 

        
        title = NewTaskForm(request.POST)
        price = NewValueForm(request.POST)
        image_url =  request.POST.get("images")
        description = NewTextForm(request.POST)

        cataogryx =  request.POST['catagory']

      
        if title.is_valid() and price.is_valid() and description.is_valid() :
            input_title =  title.cleaned_data["title"]
            input_price = price.cleaned_data["value"]
            input_description = description.cleaned_data["description"]

            save_listing = Listing.objects.create(title= input_title,description= input_description,user_id = id_user,price = input_price, url =  image_url,catagory= cataogryx)
            save_listing.save
            return render(request,"auctions/posted.html",{

                "discription" :input_description, # loads the create page with just textarea in it. 
                "title":input_title,
                "price":input_price,
                "url": image_url,
                "catagory":cataogryx
                
            })
            
        else: 
            return render(request, "auctions/create_listing.html",{
                    "discription" : title, # loads the create page with just textarea in it. 
                    "title":title ,
                    "price":price
        })

    if not request.user.is_authenticated:
         return HttpResponse("Please Sign in to post a listing") 
         

    return render(request, "auctions/create_listing.html", {
                    "discription" : NewTextForm(auto_id="id_%s"), # loads the create page with just textarea in it. 
                    "title": NewTaskForm(auto_id="id_%s_2"),
                    "price":NewValueForm(auto_id="pid_%s_1")
        })

def index(request):
        return render(request, "auctions/index.html",{
            "listings":Listing.objects.filter(status = "AT")
            })


@login_required(login_url='/login')
def user_listing(request):
    if request.user.is_authenticated:

       # usr = request.user.username
        usr = request.user
        user_listings  = Listing.objects.filter(user=usr.id,status = "AT")

        return render(request, "auctions/my_listings.html",{
           "listings":user_listings
       })

@login_required(login_url='/login')
def close_listing(request):
    if request.user.is_authenticated:
        current_user = request.user
        id_user = current_user.id 
   
        if request.method == "POST":
            lst_id =  request.POST['close_listing']
            item_id = Listing.objects.get(id=lst_id)
            item_owner = item_id.user_id

            if (id_user ==item_owner ):
                listing_bids = Bid.objects.filter(listing_id=lst_id)
                bid_count = Bid.objects.filter(listing_id=lst_id).count()   
                if (bid_count >0):
                    max_bid  = listing_bids.order_by('-bid_value')[0]
                    max_bid_user_id = max_bid.user_id  
                    Bid.objects.filter(~Q(user=max_bid_user_id),listing_id=lst_id,win_status= "PD").update(win_status = "LS")
                    Bid.objects.filter(listing_id=lst_id,user_id=max_bid_user_id,win_status= "PD").update(win_status = "WN")
                    Listing.objects.filter(id=lst_id,user=id_user).update(status = "CL")
                    messages.success(request, 'This Listing has been closed successully and winner has been notified')
                    return render(request, "auctions/success.html")
                else:
                    Listing.objects.filter(id=lst_id,user=id_user).update(status = "CL")
                    messages.success(request, '"Your listing is now closed. Please go back to main page."')
                    return render(request, "auctions/success.html")


@login_required(login_url='/login')
def bid_win_history(request):
    if request.user.is_authenticated:
        current_user = request.user
        id_user = current_user.id

        hist_ind = False

        biddings_won = Bid.objects.filter(user=id_user,win_status= "WN")
        if (len(biddings_won)>0):
            hist_ind = True
            
        return render(request, "auctions/bidding_history.html",{
            "biddings_won": biddings_won,
            "hist_ind": hist_ind
            })   


@login_required(login_url='/login')
def bid_history(request):
    if request.user.is_authenticated:
        current_user = request.user
        id_user = current_user.id

        hist_ind = False

        biddings_won = Bid.objects.filter(user=id_user,win_status= "PD")
        if (len(biddings_won)>0):
            hist_ind = True
        return render(request, "auctions/history_bid.html",{
            "biddings_won": biddings_won,
            "hist_ind": hist_ind
            })   



def listing_deatils(request):
    current_user = request.user
    id_user = current_user.id 

    if request.method == "POST":
        lst_id =  request.POST['view_details'] 

        item_id = Listing.objects.get(id=lst_id)
        item_owner_id = item_id.user_id
        item_onwer = False

        if (id_user == item_owner_id):
             item_onwer = True
        
        lst_detail = Listing.objects.get(id=lst_id)

        usr_comments = Comment.objects.filter(listing_id=lst_id)

        bid_count = Bid.objects.filter(listing_id=lst_id).count()

        watch_ind = False
        bid_won_price = None
        if (get_user_watchlist(id_user,lst_id) == None):
            watch_ind = True

        closed_ind = False
        if (lst_detail.status == "CL"):
            closed_ind = True
            bid_won_price = Bid.objects.filter(listing_id=lst_id,user=id_user,win_status= "WN")
            bid_won_price = bid_won_price[0].bid_value

        return render(request, "auctions/user_listings.html",{
        "msg": lst_id,
        "title":lst_detail.title,
        "description" : lst_detail.description,
        "url": lst_detail.url,
        "price": lst_detail.price,
        "comments": usr_comments,
        "totalbids":bid_count,
        "watch_ind":watch_ind,
        "owner_ind":item_onwer,
        "closed_ind":closed_ind,
        "bid_won_price":bid_won_price

  
        })

    else:
        return render(request, "auctions/user_listings.html")


@login_required(login_url='/login')
def place_bid(request):

    if request.method == "POST":

        current_user = request.user
        id_user = current_user.id

        bid =  request.POST.get("bid")

        lsting_id = request.POST.get("lstId")

        item_id = Listing.objects.get(id=lsting_id)
        item_owner_id = item_id.user_id
        item_onwer = False

        if (current_user.id == item_owner_id):
             item_onwer = True

        watch_ind = False
        bid_won_price = None
        if (get_user_watchlist(id_user,lsting_id) == None):
            watch_ind = True   


        lst_detail = Listing.objects.get(id=lsting_id)
        closed_ind = False
        if (lst_detail.status == "CL"):
            closed_ind = True
            bid_won_price = Bid.objects.filter(listing_id=lsting_id,user=id_user,win_status= "WN")
            bid_won_price = bid_won_price[0].bid_value   

        listing = Listing.objects.filter(id=lsting_id)
        listing_price = listing[0].price


        bid_price = Bid.objects.filter(listing_id=lsting_id)
        
        if (len(bid_price) == 0):
            max_bid = 0
        else:
            max_bid = bid_price.order_by('-bid_value')[0].bid_value

        if (float(bid) < float(listing_price)):


            usr_comments = Comment.objects.filter(listing_id=lsting_id)

            bid_count = Bid.objects.filter(listing_id=lsting_id).count()

            messages.error(request, 'Bid should be greater than the price of listing')

            return render(request, "auctions/user_listings.html",{
            "msg": lsting_id,
            "title":listing[0].title,
            "description" : listing[0].description,
            "url": listing[0].url,
            "price": listing_price,
            "comments": usr_comments,
            "totalbids":bid_count,         
            "watch_ind":watch_ind,
            "owner_ind":item_onwer,
            "closed_ind":closed_ind,
            "bid_won_price":bid_won_price

        })
        
        elif (float(bid) < float(max_bid)):

            usr_comments = Comment.objects.filter(listing_id=lsting_id)

            bid_count = Bid.objects.filter(listing_id=lsting_id).count()

            messages.error(request, 'Bid should be greater than the existing bid placed')

            return render(request, "auctions/user_listings.html",{
            "msg": lsting_id,
            "title":listing[0].title,
            "description": listing[0].description,
            "url": listing[0].url,
            "price": listing_price,
            "comments": usr_comments,
            "totalbids":bid_count,         
            "watch_ind":watch_ind,
            "owner_ind":item_onwer,
            "closed_ind":closed_ind,
            "bid_won_price":bid_won_price
        })

        else:

            save_bid = Bid.objects.create(bid_value = bid,user_id = current_user.id,listing_id= lsting_id)
            save_bid.save
      
      
            return render(request, "auctions/posted.html",{
            "title":listing[0].title,
            "description" : listing[0].description,
            "url": listing[0].url,
            "price": bid
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



def add_to_watchlist(request):
    if request.user.is_authenticated:
        current_user = request.user
        id_user = current_user.id 

        if request.method == "POST":
            lst_id =  request.POST['lst_id']

            if (get_user_watchlist(id_user,lst_id) == None):

                save_watchlist = Watchlist.objects.create(user_id =id_user,listing_id= lst_id)
                save_watchlist.save
                messages.success(request, 'Added to Wishlist')
                return render(request, "auctions/success.html")
            else:  
                return  HttpResponse("Already in your Wishlist")

    return HttpResponse("Please Sign in")  



def remove_from_watchlist(request):
    if request.user.is_authenticated:
        current_user = request.user
        id_user = current_user.id 

        if request.method == "POST":
            lst_id =  request.POST['id_lst']

            print(lst_id)

        if (request.POST['watchlist_remove'] =="Remove"):
              xx=   Watchlist.objects.filter(user_id =id_user,listing_id= lst_id)
              xx.delete()

              #message needs to be displayed
              return HttpResponseRedirect(reverse("index"))


def my_watchlist(request):
    if request.user.is_authenticated:
        usr = request.user

    return render(request, "auctions/watchlist.html",{
            "listings":Watchlist.objects.filter(user=usr.id)
            })



def search(request):

    return render(request, "auctions/search.html")


def search_results(request):
    if request.method == "POST":
            cataogry =  request.POST['catagory']

            search_result = Listing.objects.filter(catagory=cataogry)

            no_results = False
            if(len(search_result)==0):
                no_results = True


    return render(request, "auctions/my_listings.html",{
            "listings":search_result,
            "result_ind": True,
            "no_results":no_results
            })


def post_comment(request):
    if request.user.is_authenticated:
        usr = request.user
        lst_id =  request.POST['id_lst']
        comment = request.POST['comments']

        Comment.objects.create(comment =comment,user_id =usr.id,listing_id= lst_id)
        messages.success(request, 'Your comment has been posted!')
      
    return render(request, "auctions/success.html")
