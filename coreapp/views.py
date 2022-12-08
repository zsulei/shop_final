from datetime import datetime
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegistrationForm, AvatarUpdateForm, ProductImageForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Client, Product, Categories, Material, Size, Type, Manufacturer, AdminLog, Purchase
from .functions import handle_upload_avatar


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success = 'Now You can Log In'
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'user_form': user_form})


def search_by_name(request):
    name = request.GET.get('name_search')
    return render(request, 'coreapp/by_name.html', {
        'products': Product.objects.filter(title__contains=name),
        'categories': Categories.objects.all(),
    })


def cabinet(request):
    return render(request, 'coreapp/cabinet.html', {
        'categories': Categories.objects.all(),
        'admin_log': AdminLog.objects.filter(client=request.user)
                  .order_by('-purchase_date'),
    })


def admin_mode(request):
    return render(request, 'coreapp/admin_mode.html', {
        'products': Product.objects.all(),
        'categories': Categories.objects.all()
    })


def addproducts(request):
    if request.method == "POST":
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('home')
    else:
        form = ProductImageForm()
    return render(request, 'coreapp/admin_mode.html', {'form': form})


def delete_product(request, productid):
    product = Product.objects.get(id=productid)
    product.delete()
    return redirect('admin_mode')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('logout')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def update_first_name(request):
    if request.method == 'POST':
        user = Client.objects.get(id=request.user.id)
        user.first_name = request.POST.get('first_name')
        user.save()
        return redirect('cabinet')


def update_last_name(request):
    if request.method == 'POST':
        user = Client.objects.get(id=request.user.id)
        user.last_name = request.POST.get('last_name')
        user.save()
        return redirect('cabinet')


def delete_user(request):
    user = Client.objects.get(id=request.user.id)
    if not user.is_superuser:
        user.delete()
    return redirect('home')


def avatar(request):
    return render(request, 'coreapp/upload_avatar.html', {'avatar': Client.objects.get(id=request.user.id).avatar})


def update_avatar(request):
    if request.method == 'POST':
        form = AvatarUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            new_avatar = handle_upload_avatar(request.FILES['avatar'])
            user = request.user
            user.avatar = new_avatar
            user.save()
            return redirect('cabinet')
    else:
        form = AvatarUpdateForm()
    return render(request, 'coreapp/upload_avatar.html', {'form': form, })


def home(request):
    is_popular = Product.objects.filter(is_popular=True)
    order_by = request.GET.get('order_by', None)
    if order_by == 'highest':
        products = Product.objects.order_by('-price')
    else:
        products = Product.objects.order_by('price')
    return render(request, 'coreapp/home.html', {
        'is_popular': is_popular,
        'products': products,
        'categories': Categories.objects.all(),
    })


def product_detail(request, productid):
    return render(request, 'coreapp/product.html', {
        'product_detail': Product.objects.get(id=productid),
        'categories': Categories.objects.all(),
        'products': Product.objects.all(),
    })


def by_category(request, categoryid):
    return render(request, 'coreapp/category.html', {
        'products': Product.objects.filter(category=categoryid),
        'categories': Categories.objects.all(),
    })


def about_us(request):
    return render(request, 'coreapp/about.html', {
        'categories': Categories.objects.all(),
    })


def test_payment(request):
    total_price = 0
    cart = Cart(request)
    if len(cart.cart.values()) != 0:
        admin_log = AdminLog(
            client=Client.objects.get(id=request.user.id),
            purchase_date=datetime.now(tz=timezone.utc),
            total_price=total_price,
        )
        admin_log.save()
        for item in cart.cart.values():
            purchase = Purchase(
                product=Product.objects.get(id=item['product_id']),
                quantity=int(item['quantity']),
            )
            purchase.save()
            admin_log.purchase.add(purchase)
            admin_log.save()
        cart.clear()
        return redirect('home')
    else:
        success_message = 'Add some products to your cart first'
        return redirect('cart_detail')


@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')
