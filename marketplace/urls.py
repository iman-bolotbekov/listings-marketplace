from django.urls import path

from . import views

urlpatterns = [
    path('', views.getListings, name='listing-list'),
    path('user/', views.getUserListings, name='listing-user'),
    path('<int:pk>/', views.getListing, name='listing-detail'),
    path('create/', views.createListing, name='listing-add'),
    path('<int:pk>/update/', views.updateListing, name='listing-update'),
    path('<int:pk>/delete/', views.deleteListing, name='listing-delete'),
]