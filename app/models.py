import sys

# Prevent loading the conflicting models package
if 'models' in sys.modules:
    del sys.modules['models']

# Now import Django models safely



from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

COLOR_HEX_MAP = {
    "Red": "#FF0000",
    "Green": "#008000",
    "Blue": "#0000FF",
    "Black": "#000000",
    "White": "#FFFFFF",
    "Navy": "#000080",
    "Pink": "#FFC0CB",
    "Yellow": "#FFFF00",
    "Purple": "#800080",
    "Maroon": "#800000",
    "Orange": "#FFA500",
    "Gray": "#808080",
    # Add more if needed
}
# Create your models here.
class Size(models.Model):
    name = models.CharField(max_length=10)


    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('formalwear', 'Formal Wear'),
        ('casualwear', 'Casual Wear'),
        ('festiveCollection', 'Festive Collection'),
        ('rental', 'Rental Wear'),
    ]
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='formalwear')
    Availability = (('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock'))
    image = models.ImageField(upload_to='ecommerce/pimg')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    Availability = models.CharField(choices=Availability, null=True, max_length=100)
    date = models.DateField(auto_now_add=True)

    # Product details
    description = models.TextField(blank=True, null=True)
    shirt_details = models.TextField(blank=True, null=True)
    trouser_details = models.TextField(blank=True, null=True)
    fabric = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    color_hex = models.CharField(max_length=7, blank=True, null=True, default='#FFFFFF')
    weight = models.CharField(max_length=50, blank=True, null=True)
    care_instructions = models.TextField(blank=True, null=True)
    disclaimer = models.TextField(blank=True, null=True)

    # Size relationship
    available_sizes = models.ManyToManyField(Size)

    def save(self, *args, **kwargs):
        if self.color and not self.color_hex:
            self.color_hex = COLOR_HEX_MAP.get(self.color.capitalize(), '#FFFFFF')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', args=[str(self.id)])

class UserExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=11)
    address = models.TextField()
    address_line_2 = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required='True',error_messages={'exists':'This Already Exists'})
    phonenumber = forms.CharField(
        required=True,
        max_length=11,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter phone number'}),
        label='Phone Number'
    )
    address = forms.CharField(
            required=True,
            widget=forms.Textarea(attrs={'placeholder': 'Enter street address'}),
            label='Address'
        )
    address_line_2 = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={'placeholder': 'Enter street address line 2'}),
            label='Address Line 2'
        )
    country = forms.ChoiceField(
            choices=[('Pakistan', 'Pakistan'), ('America', 'America'), ('India', 'India'), ('Nepal', 'Nepal')],
            required=True,
            label='Country'
        )
    city = forms.CharField(
            required=True,
            widget=forms.TextInput(attrs={'placeholder': 'Enter your city'}),
            label='City'
        )
    region = forms.CharField(
            required=True,
            widget=forms.TextInput(attrs={'placeholder': 'Enter your region'}),
            label='Region'
        )
    postal_code = forms.CharField(
            required=True,
            widget=forms.NumberInput(attrs={'placeholder': 'Enter postal code'}),
            label='Postal Code'
        )

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'abc@gmail.com'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            UserExtra.objects.create(
                user=user,
                phonenumber=self.cleaned_data['phonenumber'],
                address=self.cleaned_data['address'],
                address_line_2=self.cleaned_data['address_line_2'],
                country=self.cleaned_data['country'],
                city=self.cleaned_data['city'],
                region=self.cleaned_data['region'],
                postal_code=self.cleaned_data['postal_code']
            )
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']

class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.email

# order checkout
class Order(models.Model):
    image = models.ImageField(upload_to='ecommerce/order/image')
    product = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.CharField(max_length=5)
    total = models.CharField(max_length=1000, default='')
    address = models.TextField()
    phone = models.CharField(max_length=11)
    pincode = models.CharField(max_length=18)
    size = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return f"Order of {self.product} by {self.user.username} - Rs. {self.price}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='ecommerce/pimg/extra')

    def __str__(self):
        return f"Extra image for {self.product.name}"

# news


class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to='news_images/')
    intro = models.TextField(blank=True)
    daytime_look = models.TextField(blank=True, null=True)
    evening_look = models.TextField(blank=True, null=True)
    content = models.TextField()
    published_date = models.DateField()
    likes = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    related_products = models.ManyToManyField(Product, blank=True, related_name='news_articles')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.name}'

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# skin

class SkinTone(models.Model):
    name = models.CharField(max_length=100)
    color_hex = models.CharField(max_length=7)
    # base_avatar = models.ImageField(upload_to='avatars/base/', null=True, blank=True)  # Make nullable
    # clothing_mask = models.ImageField(upload_to='avatars/masks/', null=True, blank=True)  # Make nullable
    # skin_mask = models.ImageField(upload_to='avatars/skin_masks/', null=True, blank=True)

    def __str__(self):
        return self.name

class SkinTonePalette(models.Model):
    skin_tone = models.ForeignKey(SkinTone, on_delete=models.CASCADE, related_name='palettes')
    color = models.CharField(max_length=50, blank=True, null=True)  # <-- new
    color_hex = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.skin_tone.name} - {self.color_hex}"

    def save(self, *args, **kwargs):
        if self.color and not self.color_hex:
            from .models import COLOR_HEX_MAP
            self.color_hex = COLOR_HEX_MAP.get(self.color.capitalize(), '#ffffff')
        if self.color_hex:
            self.color_hex = self.color_hex.lower().strip()
        super().save(*args, **kwargs)

class LegalDocument(models.Model):
    DOCUMENT_CHOICES = [
        ('privacy', 'Privacy Policy'),
        ('terms', 'Terms & Conditions'),
    ]

    title = models.CharField(max_length=100)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_CHOICES, unique=True)
    slug = models.SlugField(unique=True)
    content = CKEditor5Field('Content', config_name='default')

    def __str__(self):
        return self.title

# wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Avoid duplicates

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_uploads/')
    detected_tone = models.ForeignKey('SkinTone', null=True, blank=True, on_delete=models.SET_NULL)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Color(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color_hex = models.CharField(max_length=7)  # e.g., #FF5733

    def __str__(self):
        return self.name

