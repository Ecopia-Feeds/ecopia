from django.urls import path
from .views import AboutView, BlogView, FAQView, ProductList, CategoryProductList, ProductDetail, PostDetail

app_name = 'products'

urlpatterns = [
    path('about-us/', AboutView, name='about'),
    path('blog/', BlogView, name='blog'),
    # path("<slug:slug>/", PostDetail, name="post_detail"),
    path('faqs/', FAQView, name='faqs'), 

    # Product listing
    path('products/', ProductList, name='products'),
    path('products/<slug:category_slug>/', CategoryProductList, name='product_list_by_category'),

    # Product detail
    path('products/<slug:category_slug>/<slug:product_slug>/', ProductDetail, name='product_detail'),
]
