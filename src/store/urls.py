from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/update', views.update_profile, name='update-profile'),
    path('profile/info', views.update_info, name='update-info'),
    path('password/update', views.update_password, name='update-password'),
    path('products/<int:pk>/', views.product_details, name='product'),
    path('products/<str:cat>', views.category_products, name='category-products'),
    path('search/<str:item>', views.search, name='search'),
    path('search_redirect', views.search_redirect, name='search-redirect'),
]