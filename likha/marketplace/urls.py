from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('login-signup/', views.login_signup, name="login_signup"),
    path('profile/', views.user_profile, name="user_profile"),
    
    # Shop page
    path('shop/', views.shop, name="shop"),
    
    # Add URLs for product categories
    path('category/traditional-pottery/', views.traditional_pottery, name="traditional_pottery"),
    path('category/indigenous-jewelry/', views.indigenous_jewelry, name="indigenous_jewelry"),
    path('category/home-decor/', views.home_decor, name="home_decor"),
    path('category/wearables-bags/', views.wearables_bags, name="wearables_bags"),
    path('category/<str:category_name>/', views.category, name="category"),
    
    # Add URLs for other pages
    path('artisans/', views.artisans, name="artisans"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('seller-dashboard/', views.seller_dashboard, name="seller_dashboard"),
    path('become-a-seller/', views.selling_page, name="selling_page"),
    path('home2/', views.home2, name="home2"),
    
    # Cart functionality
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]