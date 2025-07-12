from django.shortcuts import render, redirect, HttpResponse
from app.models import Product, Contact_us, Order, Size, News, SkinTonePalette, LegalDocument, Wishlist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.templatetags.custom_filters import rental_rate
from django.contrib.auth.models import User
from .cart import Cart
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.contrib.auth import authenticate, login
from app.models import UserCreateForm, Comment, SkinTone
from app.forms import CommentForm, SubscriberForm, UserImageForm
from django.db.utils import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.paginator import Paginator
import os
from app.utils import detect_skin_tone_from_image, get_closest_skin_tone
from django.http import JsonResponse
from app.dialogflow_utils import get_dialogflow_response
from app.utils import get_colors_for_skin_tone
from django.views.decorators.csrf import csrf_exempt

def Master(request):
    return render(request, 'master.html')

def Index(request):
    product = Product.objects.all()[:8]
    news_items = News.objects.all().order_by('-published_date')[:3]
    privacy = LegalDocument.objects.filter(slug='privacy').first()
    terms = LegalDocument.objects.filter(slug='terms-conditions').first()

    context = {
        'product': product,
        'news_items': news_items,
        'privacy': privacy,
        'terms': terms,
    }
    return render(request, 'index.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            # Save the new user and extra data
            new_user = form.save()
            # Authenticate and log in the user
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            if new_user is not None:
                login(request, new_user)
                messages.success(request, 'Registration successful!')
                return redirect('index')  # Ensure 'index' is a valid URL name
            else:
                messages.error(request, 'Authentication failed. Please try again.')
        else:
            # Handle form errors if the form is invalid
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreateForm()

    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)


@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)

    size_id = request.POST.get('size_id')
    rental_days = request.POST.get('rental_days')  # ✅ NEW: Get rental days if any
    quantity = int(request.POST.get('quantity', 1))

    try:
        size = Size.objects.get(id=size_id) if size_id else None
    except Size.DoesNotExist:
        size = None

    # Optional: Calculate price for rentals
    rental_price = None
    if product.category == 'rental' and rental_days:
        try:
            rental_days = int(rental_days)
            rental_price = rental_rate(product.price, rental_days)
        except ValueError:
            rental_days = None

    # ✅ Add item to cart
    cart.add(
        product=product,
        size=size,
        quantity=quantity,
        rental_days=rental_days,
        rental_price=rental_price
    )

    request.session.pop(f'temp_qty_{id}', None)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)

    size_id = request.GET.get('size_id')
    rental_days = request.GET.get('rental_days')  # ✅ Added for rental support

    try:
        size = Size.objects.get(id=size_id) if size_id else None
    except Size.DoesNotExist:
        size = None

    cart.remove(product=product, size=size, rental_days=rental_days)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)

    if product.category == 'rental':
        return redirect("cart_detail")  # Prevent increment for rental

    size_id = request.GET.get('size_id')
    try:
        size = Size.objects.get(id=size_id) if size_id else None
    except Size.DoesNotExist:
        size = None

    cart.add(product=product, size=size)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)

    if product.category == 'rental':
        return redirect("cart_detail")

    size_id = request.GET.get('size_id')  # Changed to GET from POST

    try:
        size = Size.objects.get(id=size_id) if size_id else None
    except Size.DoesNotExist:
        size = None

    cart.decrement(product=product, size=size)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_detail(request):
    cart = Cart(request)
    total_price = cart.get_total_price()  # Get total price
    context = {
        'cart': cart,
        'total_price': total_price,
    }
    return render(request, 'cart/cart-detail.html', context)

def about(request):
    return render(request, 'about.html')

def Contact_Page(request):
    if request.method == 'POST':
        contact = Contact_us(
            name=request.POST.get('name'),
            phone_number=request.POST.get('phone_number'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            message=request.POST.get('message'),
        )
        contact.save()
        return redirect('contact_page')  # Redirect to avoid resubmission

    # You forgot this part for GET requests
    return render(request, 'contact.html')


@login_required(login_url="/users/login")
def CheckOut(request):
    if request.method == "POST":
        cart = Cart(request)
        if not cart:
            return redirect("cart_detail")

        for item in cart:
            Order.objects.create(
                user=request.user,
                product=item['product'].name,
                price=Decimal(item['price']),
                quantity=int(item['quantity']),
                image=item['product'].image,
                address=request.POST.get('address'),
                phone=request.POST.get('phone'),
                pincode=request.POST.get('pincode'),
                size=item.get('size_name')
            )

        cart.clear()  # ✅ Cart is cleared here

        messages.success(request, "Your order has been placed!")
        return redirect('order')


def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)

    order = Order.objects.filter(user=user)
    context = {
        'order': order,
    }
    return render(request, 'order.html', context)


def Product_page(request):
    product_list = Product.objects.all().order_by('-id')  # You can sort as needed
    paginator = Paginator(product_list, 16)  # 6 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'product.html', {
        'page_obj': page_obj,
        'wishlist_items': wishlist_items,
    })


def Product_Detail(request, id):
    product = get_object_or_404(Product, id=id)
    sizes = product.available_sizes.all()

    temp_qty_key = f'temp_qty_{id}'
    temp_qty = request.session.get(temp_qty_key, 1)

    accordion_items = [
        {
            'title': 'Care Instructions',
            'content': product.care_instructions if product.care_instructions else 'Hand wash recommended. Do not bleach. Iron on low heat. Dry in shade.'
        },
        {
            'title': 'Disclaimer',
            'content': 'The actual color may slightly vary from the image shown due to lighting effects and screen settings.'
        },
    ]

    recommendations = Product.objects.exclude(id=product.id).order_by('?')[:4]

    # 👇 Add this to handle wishlist buttons
    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    context = {
        'product': product,
        'sizes': sizes,
        'accordion_items': accordion_items,
        'temp_qty': temp_qty,
        'recommendations': recommendations,
        'wishlist_items': wishlist_items,  # ✅ Pass to template
    }
    return render(request, 'product_detail.html', context)



def increase_temp_qty(request, product_id):
    key = f'temp_qty_{product_id}'
    qty = request.session.get(key, 1)
    request.session[key] = qty + 1
    return redirect('product_detail', id=product_id)

def decrease_temp_qty(request, product_id):
    key = f'temp_qty_{product_id}'
    qty = request.session.get(key, 1)
    if qty > 1:
        request.session[key] = qty - 1
    return redirect('product_detail', id=product_id)

@login_required
def clear_orders(request):
    if request.method == 'POST':
        # Delete all orders for the current user
        Order.objects.filter(user=request.user).delete()
        messages.success(request, "All your orders have been cleared.")
        return redirect('order')
    return redirect('order')

# news

def news_list(request):
    news_items = News.objects.all().order_by('-published_date')
    paginator = Paginator(news_items, 6)  # Show 6 items per page
    page = request.GET.get('page')
    paged_news = paginator.get_page(page)
    return render(request, 'news/news_list.html', {'news_items': paged_news})

def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug)
    comments = news_item.comments.order_by('-created_at')

    # Get 3 latest related posts excluding the current one
    related_posts = News.objects.exclude(id=news_item.id).order_by('-published_date')[:3]

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news_item
            comment.save()
            return redirect('news_detail', slug=news_item.slug)
    else:
        form = CommentForm()

    return render(request, 'news/news_detail.html', {
        'news_item': news_item,
        'form': form,
        'comments': comments,
        'related_posts': related_posts,
    })


def subscribe_view(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect(request.META.get('HTTP_REFERER', '/'))  # Refresh page
    else:
        form = SubscriberForm()

    return render(request, 'your_template.html', {'form': form})

# skin
def color_recommender(request):
    tone_id = request.GET.get('tone_id')
    color_hex = request.GET.get('color_hex')

    skin_tones = SkinTone.objects.all()
    selected_tone = SkinTone.objects.filter(id=tone_id).first() if tone_id else None

    palettes = []
    if selected_tone:
        palettes = get_colors_for_skin_tone(selected_tone.name)

    recommended_products = []
    if color_hex:
        recommended_products = Product.objects.filter(color_hex__iexact=color_hex)

    # ✅ Fix: Always define current_step
    if not selected_tone:
        current_step = 1
    elif selected_tone and not color_hex:
        current_step = 2
    elif selected_tone and color_hex:
        current_step = 3

    # ✅ Always render with skin_tones even if nothing selected
    return render(request, 'color_recommender.html', {
        'skin_tones': skin_tones,
        'selected_tone': selected_tone,
        'palettes': palettes,
        'recommended_products': recommended_products,
        'selected_hex': color_hex,
        'current_step': current_step,
    })



def show_palettes(request, skin_tone_id):
    tone = get_object_or_404(SkinTone, id=skin_tone_id)
    return render(request, 'color_recommender.html', {
        'skin_tones': SkinTone.objects.all(),
        'selected_tone': tone,
    })

#product categories'
CATEGORY_LABELS = {
    'formalwear': 'Formal Wear',
    'casualwear': 'Casual Wear',
    'festiveCollection': 'Festive Collection',
    'rental': 'Rental Wear',
}

def product_category(request, category_slug):
    products = Product.objects.filter(category__iexact=category_slug)
    category_label = CATEGORY_LABELS.get(category_slug, category_slug.title())  # Fallback to .title()

    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'product_category.html', {
        'products': products,
        'category': category_slug,
        'category_label': category_label,
        'wishlist_items': wishlist_items,
    })

# wishlist
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


def rental_products(request):
    products = Product.objects.filter(category='rental')
    return render(request, 'product/rental_list.html', {'products': products})

def Search(request):
    query = request.GET.get('query')
    products = Product.objects.none()  # Start with no products

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'products': products,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'search.html', context)


# def virtual_try_on(request):
#     tone_id = request.GET.get('tone_id')
#     color_hexes = request.GET.getlist('colors')
#
#     skin_tone = get_object_or_404(SkinTone, id=tone_id)
#
#     context = {
#         'base_avatar_url': skin_tone.base_avatar.url if skin_tone.base_avatar else '',
#         'clothing_mask_url': skin_tone.clothing_mask.url if skin_tone.clothing_mask else '',
#         'skin_mask_url': skin_tone.skin_mask.url if skin_tone.skin_mask else '',
#         'colors': color_hexes,
#         'selected_tone': skin_tone,
#     }
#     return render(request, 'virtual_try_on.html', context)

def upload_image(request):
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user

            # Analyze uploaded image
            hex_code = detect_skin_tone_from_image(request.FILES['image'])
            matched_tone = get_closest_skin_tone(hex_code, SkinTone.objects.all())

            instance.detected_tone = matched_tone
            instance.save()

            # Redirect to the color recommender with selected tone
            return redirect(f"/color-recommender/?tone_id={matched_tone.id}")
    else:
        form = UserImageForm()

    return render(request, 'upload.html', {'form': form})

# views.py

def chatbot_response(request):
    user_message = request.GET.get('message', '')
    bot_reply = get_dialogflow_response(user_message)
    return JsonResponse({'reply': bot_reply})

def chat_page(request):
    return render(request, "chat.html")

# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import json
#
# @csrf_exempt
# def dialogflow_webhook(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         intent = data.get("queryResult", {}).get("intent", {}).get("displayName")
#
#         if intent == "Browse Products":
#             response_data = {
#                 "fulfillmentMessages": [
#                     {
#                         "text": {
#                             "text": [
#                                 "You can explore our full collection here: https://2bd9-103-169-99-50.ngrok-free.app/product/"
#                             ]
#                         }
#                     },
#                     {
#                         "text": {
#                             "text": [
#                                 "Or choose a category below to narrow your search:"
#                             ]
#                         }
#                     },
#                     {
#                         "payload": {
#                             "richContent": [
#                                 [
#                                     {
#                                         "type": "chips",
#                                         "options": [
#                                             { "text": "Formal Wear" },
#                                             { "text": "Casual Wear" },
#                                             { "text": "Festive Collection" },
#                                             { "text": "Rental Wear" }
#                                         ]
#                                     }
#                                 ]
#                             ]
#                         }
#                     }
#                 ]
#             }
#             return JsonResponse(response_data)
#
#         # Optional: handle chip replies
#         elif intent == "Show Formal Wear":
#             return JsonResponse({
#                 "fulfillmentText": "Here's our Formal Wear collection: https://2bd9-103-169-99-50.ngrok-free.app/category/formalwear/"
#             })
#
#         elif intent == "Show Casual Wear":
#             return JsonResponse({
#                 "fulfillmentText": "Browse Casual Wear: https://2bd9-103-169-99-50.ngrok-free.app/category/casualwear/"
#             })
#
#         elif intent == "Show Festive Collection":
#             return JsonResponse({
#                 "fulfillmentText": "Explore Festive Collection: https://2bd9-103-169-99-50.ngrok-free.app/category/festiveCollection/"
#             })
#
#         elif intent == "Show Rental Wear":
#             return JsonResponse({
#                 "fulfillmentText": "Browse our Rental Wear here: https://2bd9-103-169-99-50.ngrok-free.app/category/rental/"
#             })
#
#         return JsonResponse({
#             "fulfillmentText": "Sorry, I didn't understand that. Can you rephrase?"
#         })
#
#     return JsonResponse({"error": "Invalid request method"}, status=405)
#

# views.py

def delivery_info(request):
    return render(request, 'delivery_info.html')


from django.contrib import messages


@csrf_exempt
@login_required
def start_payment(request):
    if request.method == 'POST':
        cart = Cart(request)

        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        pincode = request.POST.get('pincode', '')
        user = request.user

        if not cart:
            return JsonResponse({'error': 'Cart is empty'}, status=400)

        for item in cart:
            Order.objects.create(
                image=item['product'].image,  # assuming each product has one main image
                product=item['product'].name,
                user=user,
                price=item['price'],
                quantity=item['quantity'],
                total=item['total_price'],
                address=address,
                phone=phone,
                pincode=pincode,
                size=item.get('size_name', ''),
                date=timezone.now().date()
            )

        cart.clear()
        return JsonResponse({'redirect_url': '/order/'})

    return JsonResponse({'error': 'Invalid request'}, status=400)