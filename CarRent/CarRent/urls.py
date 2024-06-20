from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from cars import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cars/', include('cars.urls')),
    path('', include('cars.urls')),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('star/<int:car_id>/', views.star_car, name='star_car'),
    path('unstar/<int:car_id>/', views.unstar_car, name='unstar_car'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)