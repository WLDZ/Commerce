from pickle import FALSE, TRUE
import re
from .models import User,Listing,Comment,Bid,Watchlist


def get_user_watchlist(id_user,lst_id):

     current_watchlist_items = Watchlist.objects.filter(user_id =id_user,listing_id= lst_id)

     if (len(current_watchlist_items) ==0):
         return None
     return True
