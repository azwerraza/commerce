"""
URL configuration for commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import clear_orders
    # virtual_try_on
from django.conf.urls.static import static
from . import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('master/', views.Master, name='master'),
                  path('', views.Index, name='index'),
                  path('about/', views.about, name='about'),

                  path('signup/',views.signup, name='signup'),
                  path('accounts/', include('django.contrib.auth.urls')),

              # add to cart
                  path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
                  path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
                  path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
                  path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
                  path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
                  path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
              # contact us
                  path('contact_us/', views.Contact_Page, name='contact_page'),
              # product page
                  path('product/', views.Product_page, name='product'),
              # product detail
                  path('product_detail/<str:id>/', views.Product_Detail, name='product_detail'),
              # checkout
                  path('checkout/', views.CheckOut, name='checkout'),

              # order page
                 path('order/', views.Your_Order, name='order'),
              # clear order
                 path('orders/clear/', clear_orders, name='clear_orders'),
                 path('product/<int:product_id>/qty/increase/', views.increase_temp_qty, name='increase_temp_qty'),
                 path('product/<int:product_id>/qty/decrease/', views.decrease_temp_qty, name='decrease_temp_qty'),
              # news section
                 path('news/', views.news_list, name='news_list'),
                 path('news/<slug:slug>/', views.news_detail, name='news_detail'),
                 path('subscribe/', views.subscribe_view, name='subscribe'),
              # feature
                 path('recommender/', views.color_recommender, name='color_recommender'),
                 path('recommender/<int:skin_tone_id>/', views.show_palettes, name='show_palettes'),
                 path('color-recommender/', views.color_recommender, name='color_recommender'),
                 # path('skin-tone/<int:tone_id>/', views.skin_tone_detail, name='skin_tone_detail'),


               # product category
                 path('category/<str:category_slug>/', views.product_category, name='product_category'),
                 path('ckeditor5/', include('django_ckeditor_5.urls')),
                 path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='wishlist_add'),
                 path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='wishlist_remove'),
                 path('wishlist/', views.view_wishlist, name='wishlist'),
                 path('rental/', views.rental_products, name='rental_products'),
               # search
                 path('search/', views.Search, name='search'),

    # path('virtual-try-on/', views.virtual_try_on, name='virtual_try_on'),
                path('upload-image/', views.upload_image, name='upload_image'),
                path('chatbot/', views.chatbot_response, name='chatbot_response'),
                path('chat/', views.chat_page, name='chat_page'),

                path('delivery-information/', views.delivery_info, name='delivery_info'),
                path('start-payment/', views.start_payment, name='start-payment'),
# cancel order
                path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),


# path('dialogflow-webhook/', views.dialogflow_webhook, name='dialogflow_webhook'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

