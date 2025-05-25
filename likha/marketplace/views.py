from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login  # Rename login to auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.db.utils import OperationalError

def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'marketplace/home.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'marketplace/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'marketplace/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
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
        
    return JsonResponse('Item was added', safe=False)

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
    
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
        
    return JsonResponse('Payment complete!', safe=False)

# Update category views to handle the case where the category field doesn't exist yet
def traditional_pottery(request):
    data = cartData(request)
    cartItems = data['cartItems']
    try:
        products = Product.objects.filter(category='traditional_pottery')
    except OperationalError:
        # If the category field doesn't exist yet, return all products
        products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'category': 'Traditional Pottery'}
    return render(request, 'marketplace/category.html', context)

def indigenous_jewelry(request):
    data = cartData(request)
    cartItems = data['cartItems']
    try:
        products = Product.objects.filter(category='indigenous_jewelry')
    except OperationalError:
        # If the category field doesn't exist yet, return all products
        products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'category': 'Indigenous Jewelry'}
    return render(request, 'marketplace/category.html', context)

def home_decor(request):
    data = cartData(request)
    cartItems = data['cartItems']
    try:
        products = Product.objects.filter(category='home_decor')
    except OperationalError:
        # If the category field doesn't exist yet, return all products
        products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'category': 'Home Decor'}
    return render(request, 'marketplace/category.html', context)

def wearables_bags(request):
    data = cartData(request)
    cartItems = data['cartItems']
    try:
        products = Product.objects.filter(category='wearables_bags')
    except OperationalError:
        # If the category field doesn't exist yet, return all products
        products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'category': 'Wearables & Bags'}
    return render(request, 'marketplace/category.html', context)

def category(request, category_name):
    data = cartData(request)
    cartItems = data['cartItems']
    try:
        products = Product.objects.filter(category=category_name.replace('-', '_'))
    except OperationalError:
        # If the category field doesn't exist yet, return all products
        products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'category': category_name.replace('-', ' ').title()}
    return render(request, 'marketplace/category.html', context)

# Add other missing views
def shop(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'marketplace/shop.html', context)

def artisans(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}
    return render(request, 'marketplace/artisans.html', context)

def about(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}
    return render(request, 'marketplace/about.html', context)

def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}
    return render(request, 'marketplace/contact.html', context)

def login(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}
    return render(request, 'marketplace/login.html', context)

def login_signup(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user = authenticate(request, username=email, password=password)  # Change email to username
            
            if user is not None:
                auth_login(request, user)  # Use auth_login instead of login
                messages.success(request, 'Successfully logged in!')
                return redirect('home2')
            else:
                messages.error(request, 'Invalid email or password.')
                
        elif form_type == 'signup':
            try:
                email = request.POST.get('email-signup')
                password = request.POST.get('password-signup')
                first_name = request.POST.get('first-name')
                last_name = request.POST.get('last-name')
                
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already registered')
                    return redirect('login_signup')
                
                user = User.objects.create(
                    username=email,
                    email=email,
                    password=make_password(password),
                    first_name=first_name,
                    last_name=last_name
                )
                
                Customer.objects.create(
                    user=user,
                    name=f"{first_name} {last_name}",
                    email=email
                )
                
                auth_login(request, user)  # Use auth_login instead of login
                messages.success(request, 'Account created successfully!')
                return redirect('home2')
                
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
                return redirect('login_signup')
    
    return render(request, 'marketplace/login_signup.html')

def seller_dashboard(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}
    return render(request, 'marketplace/sellerdashboard.html', context)

def selling_page(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}
    return render(request, 'marketplace/sellerform.html', context)

def home2(request):
    if not request.user.is_authenticated:
        return redirect('login_signup')
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'marketplace/home2.html', context)

def logout_view(request):
    print("Logout view called")  # Debug log
    logout(request)
    return redirect('home')

def user_profile(request):
    print("User profile view called")  # Debug log
    if not request.user.is_authenticated:
        return redirect('login_signup')
        
    data = cartData(request)
    cartItems = data['cartItems']
    
    context = {
        'cartItems': cartItems,
        'user': request.user
    }
    return render(request, 'marketplace/userprofile.html', context)
