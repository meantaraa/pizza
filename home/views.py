from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from .models import Cart, CartItem, Pizza, User
from django.contrib.auth import logout


def home(request):
    pizzas = Pizza.objects.all()
    cart_count = 0

    if request.user.is_authenticated:
        cart_count = request.user.get_cart_count()
    
    context = {
        'pizzas': pizzas,
        'cart_count': cart_count,
    }
    return render(request, 'home.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken.')
                return redirect('/register/')

            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()

            messages.success(request, 'Account created.')
            return redirect('/login')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('/register/')

    return render(request, 'register.html') 

def add_cart(request, pizza_uid):
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    user = request.user
    pizza_obj = Pizza.objects.get(uid=pizza_uid)
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item = CartItem.objects.create(cart=cart, pizza=pizza_obj)

    return redirect('/')

def cart(request):
    cart = Cart.objects.get(is_paid = False, user = request.user)
    context = {'carts': cart}
    return render(request, 'cart.html', context )



def remove_cart_items(request, cart_item_uid):
    try:
        CartItem.objects.get(uid = cart_item_uid).delete()


        return redirect('/cart/')
    except Exception as e:
        print(e)


def handleLogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Successfully Logged Out")
    return redirect('home')