from email import message
from pyexpat.errors import messages
from typing import ItemsView
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.

def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/checkout.html', context)


def login(request):
    """
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return render(request, 'store/login.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'store/login.html',
                          {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'store/login.html')
"""

    if request.session.get('id') != None:  # Puede iniciar sesión solo cuando no haya iniciado sesión
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            username = username.strip()  # Eliminar espacios y líneas nuevas
            password = password.strip()
            try:
                user = models.User.objects.get(username=username)
            except:
                message = 'El nombre de usuario no existe'
                return render(request, 'store/login.html', {"message": message})
            if user.password == password:
                request.session['id'] = user.id  # Registrar que el usuario ha iniciado sesión
                return redirect('store/store.html')
            else:
                message = 'contraseña incorrecta'
                return render(request, 'store/login.html', {"message": message})
    return render(request, 'store/login.html')


def logout(request):
    request.session.flush()
    return render('store/login.html')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('store/store.html')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="store/register.html", context={"register_form": form})

"""
    # if request.session.get('id') != None:  # Regístrese solo cuando no haya iniciado sesión
    #   return redirect('store/store.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # email = request.POST.get('email')
        username = username.strip()  # Eliminar espacios y líneas nuevas
        password = password.strip()
        # email = email.strip()
        if models.User.objects.filter(username=username).exists():
            message = 'este usuario ha sido registrado'
            return render(request, 'store/register.html', {"message": message})
        user = models.User()
        user.username = username
        user.password = password
        # user.email = email
        user.save()
        request.session['id'] = user.id  # Registrar que el usuario ha iniciado sesión
        return redirect('store/store.html')
    return render(request, 'store/register.html')
"""

def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user
    return render(request, 'social/profile.html', {'user': user, 'posts': posts})


"""
def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'sigues a {username}')
    return redirect('feed')


def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
    rel.delete()
    messages.success(request, f'Ya no sigues a {username}')
    return redirect('feed')
"""


def UpdateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # agregar o remover del Cart. Chequear JavaScript
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
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

    else:
        print('User is not logged in..')

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
