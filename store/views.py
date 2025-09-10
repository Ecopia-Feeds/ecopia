from django.shortcuts import render


# Create your views here.
def AboutView(request):
    """Handles About Us page"""
    return render(request, 'about.html')


def FAQView(request):
    """Handles FAQ page"""
    return render(request, 'faqs.html')


from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def ProductList(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, "products.html", {
        "category": category,
        "categories": categories,
        "products": products
    })

def CategoryProductList(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, "category.html", {
        "category": category,
        "categories": categories,
        "products": products
    })

def ProductDetail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    categories = Category.objects.all()
    product = get_object_or_404(
        Product,
        category_id = category.id,
        slug=product_slug
    )
    return render(request,'detail.html',{
        'product': product,
        "category": category,
        "categories": categories,
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post, NewsletterSubscriber
from .forms import NewsletterForm



def BlogView(request):
    posts = Post.objects.all()[:5]  # limit to 5 for homepage
    form = NewsletterForm()
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, "You have subscribed to our newsletter!")
            return redirect("post_list")
    return render(request, "blog.html", {"posts": posts, "form": form})


def PostDetail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post_detail.html", {"post": post})
