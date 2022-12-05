from datetime import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegistrationForm, AvatarUpdateForm
from dateutil.tz import tzlocal
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


def cabinet(request):
    return render(request, 'coreapp/cabinet.html', {
        'user': Client.objects.get(id=request.user.id),
        'categories': Categories.objects.all(),
        'products': Product.objects.all(),
        'size': Size.objects.all(),
        'purchases': AdminLog.objects.filter(client=request.user),
    })


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            print('asd')
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
    return render(request, 'coreapp/home.html', {
        'products': Product.objects.all(),
        'categories': Categories.objects.all(),
    })


def product_detail(request, productid):
    return render(request, 'coreapp/product.html', {
        'product_detail': Product.objects.get(id=productid),
        'categories': Categories.objects.all(),
        'products': Product.objects.all(),
    })


def by_category(request, categoryid):
    query = Categories.objects.filter(category=categoryid)
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
            purchase_date=datetime.now(tzlocal()).strftime("%Y-%m-%d %H:%M:%S"),
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
