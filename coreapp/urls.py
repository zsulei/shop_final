from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    path('upload_avatar/', views.update_avatar, name='upload_avatar'),
    path('avatar/', views.update_avatar, name='avatar'),
    path('update_first_name/', views.update_first_name, name='update_first_name'),
    path('update_last_name/', views.update_last_name, name='update_last_name'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('change_password/', views.change_password, name='change_password'),
    path('registration/', views.register, name='registration'),
    path('detail/<int:productid>/', views.product_detail, name='product'),
    path('category/<int:categoryid>/', views.by_category, name='category'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
    path('test', views.test_payment, name='test'),
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about'),
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
