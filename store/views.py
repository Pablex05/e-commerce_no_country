from email import message
from pyexpat.errors import messages
from typing import ItemsView
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from verify_email.email_handler import send_verification_email
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# Create your views here.

def store(request):
    order, items, cartItems = list_product(request)
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        order, items, cartItems = list_product(request)
        context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
        return render(request, 'store/cart.html', context)
    else:
        messages.success(request, "Tiene que INICIAR SESION")  # corregir y aplicar decorator de autenticacion
        return redirect('/')

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
        return render(request, 'store/checkout.html', context)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
        messages.success(request, "Tiene que INICIAR SESION")  # corregir y aplicar decorator de autenticacion
        return redirect('/')

def login_user(request):
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
                messages.success(request, 'El nombre de usuario no existe')
                return render(request, 'store/login.html', {"message": message})
            if not user.is_active:
                messages.success(request, 'Ingrese a su cuenta de correo electronico para completar la activacion de la cuenta')
            if user.password == password:
                request.session['id'] = user.id  # Registrar que el usuario ha iniciado sesión
                return redirect('store/store.html')
            else:
                messages.success(request, 'contraseña incorrecta')
                return render(request, 'store/login.html')

    return render(request, 'store/login.html')

def list_product(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    return order, items, cartItems

def logout_user(request):
    if request.user.is_authenticated:
        if request.session.get('id') != None:  # Puede iniciar sesión solo cuando no haya iniciado sesión
            return redirect('/')
        try:
            request.session.flush()
        except:
            messages.success(request, 'Deslogueo no Exitoso, intentelo mas tarde')
            return redirect('/')
        return redirect('/')
    else:
        messages.success(request, "Tiene que INICIAR SESION")  # corregir y aplicar decorator de autenticacion
        return redirect('/')

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            #inactive_user = send_verification_email(request, form)
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            Customer.objects.create(user=user)
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('store/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, f"Ingrese a su cuenta de correo electronico para completar la activacion de la cuenta")
            return redirect('/')
        messages.success(request, "Error en registrar el Usuario - complete correctamente los campos.")
    return render(request, 'store/register.html')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user
    return render(request, 'social/profile.html', {'user': user, 'posts': posts})

@login_required
def UpdateItem(request):
    if request.user.is_authenticated:
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
    else:
        messages.success(request, "Tiene que INICIAR SESION")  # corregir y aplicar decorator de autenticacion
        return redirect('/')

@login_required
def processOrder(request):
    if request.user.is_authenticated:
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
    else:
        messages.success(request, "Tiene que INICIAR SESION")  # corregir y aplicar decorator de autenticacion
        return redirect('/')