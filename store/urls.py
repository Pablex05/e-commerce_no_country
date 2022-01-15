from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.UpdateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('login_user/', LoginView.as_view(template_name='store/login.html'), name="login_user"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('register/', views.register, name="register"),
]
