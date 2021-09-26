from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path ("new_listing",views.new_lisitng,name = "new_listing"),
    path ("user_listing",views.user_listing,name = "user_listing"),
    path ("listing_details",views.listing_deatils,name = "listing_details"),
    path ("add_to_watchlist",views.add_to_watchlist,name = "add_to_watchlist"),
    path ("my_watchlist",views.my_watchlist,name = "my_watchlist"),
    path ("posted",views.place_bid,name = "posted"),
    path ("remove_from_watchlist",views.remove_from_watchlist,name = "remove_from_watchlist"),
    path ("close_listing",views.close_listing,name = "close_listing"),
    path ("bid_history",views.bid_win_history,name = "bid_history"),
    path ("bid_history_all",views.bid_history,name = "bid_history_all"),
    path ("search",views.search,name = "search"),
    path ("results",views.search_results,name = "results"),
    path ("comment",views.post_comment,name = "comment")


   

]
