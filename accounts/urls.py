from django.urls import path

from .views import HomeView, RegisterView, LoginView, LogoutView, ProfileView, CartView


urlpatterns = [
    path('', HomeView, name='home'),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("accounts/cart/", CartView.as_view(), name="cart"),   
]
