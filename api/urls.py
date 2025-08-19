from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import LikedMoviesListCreateView, couple_data_view, create_couple_view

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('liked-movies/', LikedMoviesListCreateView.as_view(), name='liked_movies_list_create'),
    path('couples/', couple_data_view, name='couple_data_view'),
    path('create-couple/', create_couple_view, name='create_couple_view'),
]
