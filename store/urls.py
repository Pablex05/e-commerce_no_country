from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.UpdateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('login/', LoginView.as_view(template_name='store/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='store/main.html'), name="logout"),
    path('register/', views.register, name="register"),
]
