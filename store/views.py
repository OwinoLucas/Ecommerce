from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ecommerce.settings import MESSAGE_TAGS
from .forms import *

from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from .mpesa import MpesaGateWay
import pdb
from django.contrib.sessions.models import Session

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created. You can now proceed to login.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}!')
            return redirect('store')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})


@login_required
def customer_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = CustomerUpdateForm(request.POST, request.FILES, instance=request.user.customer)

        if u_form.is_valid() and p_form.is_valid():
            print("Forms are valid")
            u_form.save()
            print("User form saved")
            p_form.save()
            print("Customer form saved")
            messages.success(request, f'Your account has been updated!')
            return redirect('customer-profile')
        else:
            print("Forms are not valid")
            print(u_form.errors)
            print(p_form.errors)

            messages.error(request, 'There was an error updating your profile. Please check the form.')
    context = {
        'u_form': UserUpdateForm(instance=request.user),
        'p_form': CustomerUpdateForm(instance=request.user.customer),
    }
    return render(request, 'auth/customer.html', context)
        

def logout_view(request):
    logout(request)
    return redirect('login')

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def mpesa(request):
    data = cartData(request)
    order = data['order']

    # pdb.set_trace()
    phonenumber = str(request.user.customer.mobile).lstrip('+')
    print(phonenumber)
    amount = int(order.get_cart_total)
    callback_url = 'https://mydomain.com/path'
    lipaNaMpesa = MpesaGateWay()

    try:
        stk = lipaNaMpesa.stk_push(phonenumber, amount, callback_url)
        return render(request, 'store/checkout.html', {'stk': stk})
    except Exception as e:
        return render(request, 'store/checkout.html', {'error_message': str(e)})
      

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    context = {'orderItem':orderItem}
    return render(request, 'store/cart.html', context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if 'Cart' in request.session:
        del request.session['cart']
        request.session.modified = True

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

    return render(request, 'store/checkout.html')