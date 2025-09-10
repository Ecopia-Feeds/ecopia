from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        ordering = ('name',)

class Product(models.Model):
    category = models.ForeignKey(Category, related_name = 'products', on_delete = models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    specification = models.TextField()
    weight = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField()
    available = models.BooleanField(default=True)


    def get_absolute_url(self):
        return reverse(
            'products:product_detail',
            args=[self.category.slug, self.slug]
        )

    class Meta:
        ordering = ('name',)

class Banner(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="banners/")
    discount_text = models.CharField(max_length=50, blank=True, null=True)  # e.g. "20% OFF"
    button_text = models.CharField(max_length=50, blank=True, null=True)    # e.g. "Shop Now"
    button_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
from django.db import models
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, help_text="e.g., Recent Blog Posts, Our")
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="posts/")
    excerpt = models.TextField(max_length=300, help_text="Short preview text")
    content = models.TextField(help_text="Full article content")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("post_detail", args=[self.slug])


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
