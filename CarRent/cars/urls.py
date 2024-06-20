from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('add/', views.add_car, name='add_car'),
    path('delete/<int:pk>/', views.delete_car, name='delete_car'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('star/<int:car_id>/', views.star_car, name='star_car'),
    path('unstar/<int:car_id>/', views.unstar_car, name='unstar_car'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'), 
    path('rent/<int:car_id>/', views.rent_car, name='rent_car'), 
    path('rent_confirmation/<int:rented_car_id>/', views.rent_confirmation, name='rent_confirmation'),
    path('unrent/<int:car_id>/', views.unrent_car, name='unrent_car'), 
    path('filter/', views.car_filter, name='car_filter'),  

]


