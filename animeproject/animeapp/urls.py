from django.urls import path
from .views import home,signup_view,login_view,logout_view,watchlist_view,add_to_watchlist,anime_detail

urlpatterns = [
    path('', home, name='home'),
    path('anime/<int:anime_id>/', anime_detail, name='anime_details'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('watchlist/', watchlist_view, name='watchlist'),
    path('add-to-watchlist/<int:anime_id>/', add_to_watchlist, name='add_to_watchlist'),
]
