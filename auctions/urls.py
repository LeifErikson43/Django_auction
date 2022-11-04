from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:item_id>/view_listing", views.view_listing, name="view_listing"),
    path("<int:item_id>/close_listing", views.close_listing, name="close_listing"),
    path("<int:item_id>/make_bid", views.make_bid, name="make_bid"),
    path("<int:item_id>/watch_add", views.watch_add, name="watch_add"),
    path("<int:item_id>/watch_remove", views.watch_remove, name="watch_remove",),
    path("<int:item_id>/add_comment", views.add_comment, name="add_comment"),
    path("closed_auctions", views.closed_auctions, name="closed_auctions"),
    path("my_auctions", views.my_auctions, name="my_auctions"),
    path("<str:category>/category_list_page", views.category_list_page, name="category_list_page"),
    path("bid_message", views.bid_message, name="bid_message")
]
