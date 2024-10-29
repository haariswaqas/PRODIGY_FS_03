from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_Listing, name = "create"),
    path("particular_Category", views.particular_Category, name="particular_Category"), 
    path("listing/<int:id>", views.listing, name = "listing"), 
    path("watchlistRemove/<int:id>", views.watchlistRemove, name="watchlistRemove"),
    path("watchlistAdd/<int:id>", views.watchlistAdd, name="watchlistAdd"), 
    path("add_comment/<int:id>", views.add_comment, name="add_comment"), 
    path("watchlist", views.show_watchlist, name="watchlist"), 
    path("add_bid/<int:id>", views.add_bid, name="add_bid"),
    path("close/<int:id>", views.close, name="close")
    
]
