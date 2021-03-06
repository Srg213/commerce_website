from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name='create'),
    path('listings/<int:listing_id>' , views.item , name = 'listing'),
    path('watchlist',views.watchlist ,name='watchlist'),
    path('comment' , views.comments , name='comment')
]
