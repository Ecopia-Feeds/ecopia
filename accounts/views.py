from django.shortcuts import render, redirect, get_object_or_404
from store.models import Category, Product, Post, NewsletterSubscriber
from store.forms import NewsletterForm

# Create your views here.
def HomeView(request, category_slug=None):
    """
    A general home page with options to login and info.
    """ 
    category = None
    products = Product.objects.filter(available=True)
    posts = Post.objects.all()[:3]
    form = NewsletterForm()

    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, "You have subscribed to our newsletter!")
            return

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, "home.html", {
        "category": category,
        "products": products,
        "posts": posts,
        "form": form
    })


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages

from .models import AuditLog, CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class RegisterView(View):
    """Handles user registration."""

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Log action
            AuditLog.objects.create(user=user, action="login", description="New account created and logged in.")

            messages.success(request, "Your account has been created successfully!")
            return redirect("/")  # 👈 redirect to your dashboard/home
        return render(request, "register.html", {"form": form})


class LoginView(View):
    """Handles user login."""

    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Log action
            AuditLog.objects.create(user=user, action="login", description="User logged in.")

            return redirect("/")
        messages.error(request, "Invalid email or password.")
        return render(request, "login.html", {"form": form})


class LogoutView(View):
    """Handles user logout."""

    @method_decorator(login_required)
    def get(self, request):
        AuditLog.objects.create(user=request.user, action="logout", description="User logged out.")
        logout(request)
        return redirect("login")


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    """User profile page."""

    def get(self, request):
        return render(request, "profile.html", {"user": request.user})

class CartView(View):
    """Handles Cart page"""
    def get(self, request):
        return render(request, 'cart.html', {"user": request.user})