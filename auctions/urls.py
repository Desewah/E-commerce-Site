from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.display_listing, name="display_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist/<int:id>", views.watchlist_action, name="watchlist"),
    path("watchlist", views.watchlist, name="watch_list"),
    path("comment_section/<int:id>", views.comment_section, name="comment_section"),
    path("place_bid/<int:id>", views.place_bid, name="place_bid"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction"),
    path("closed_auctions", views.inactive_auctions, name="inactive_auctions"),
]
