from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from django.db.models import Q



# Create your views here.

def index(request):
    product = {
        'product' :Product.objects.all()
    }
    return render(request,'index.html',product )


def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)

# product = Product.objects.all()
#     product_id = Product.objects.filter(product_id=id)



def loginn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,"invalid username or password")
            return redirect('login')
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.info(request,"username already exists")
            return redirect('register')

        elif User.objects.filter(email=email).exists():
            messages.info(request,"email already exists")
            return redirect('register')
        
        else:
            user=User.objects.create_user(username=username , email=email, password=password)
            user.save();
        return redirect('/')
    return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')



# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     
#     cart, created = Cart.objects.get_or_create(user=request.user, product=product)

#     if not created:
#         # Increment the quantity if the product is already in the cart
#         cart.quantity += 1
#         cart.save()

#     
#     return redirect('view_details', product_id=product_id)


# def cart(request):
#     
#     cart_items = Cart.objects.filter(user=request.user)

#    
#     total_price = sum(item.product.price * item.quantity for item in cart_items)

#     context = {
#         'cart_items': cart_items,
#         'total_price': total_price
#     }

#     return render(request, 'cart.html', context)

# def add_to_cart(request):
#     user=request.user
#     product_id=request.GET.get('prod_id')
#     print(product_id)
#     # product = Product.objects.get(id=product_id)
#     product = get_object_or_404(Product, id=product_id)
#     print(product_id)
#     Cart(user=user,product=product).save()
#     print(product_id)
#     return redirect("cart")

# def show_cart(request):
#     user=request.user
#     cart=Cart.objects.filter(user=user)
#     return render(request,"addtocart.html",locals(),{'cart': cart})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    # print(card_product)
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
            totalamount = amount 
        return render(request, 'addtocart.html', {'cart': cart, 'totalamount': totalamount, 'amount': amount})
    else:
        return render(request, 'emptycard.html')

@login_required
def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET.get('prod_id')
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity += 1
    c.save()

    amount = 0.0
    
    card_product = [p for p in Cart.objects.all() if p.user == request.user]
                    
    for p in card_product:
        tempamount = (p.quantity * p.product.price)
        amount += tempamount

    data = {
        'quantity': c.quantity,
        'amount': amount,
        'totalamount': amount 
    }
    return JsonResponse(data)
  
@login_required
def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET.get('prod_id')
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity -= 1
    c.save()

    amount = 0.0
    
    card_product = [p for p in Cart.objects.all() if p.user ==request.user]
    for p in card_product:
        tempamount = (p.quantity * p.product.price)
        amount += tempamount

    data = {
        'quantity': c.quantity,
        'amount': amount,
        'totalamount': amount 
    }
    return JsonResponse(data)

@login_required
def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()

    amount = 0.0
    
    card_product = [p for p in Cart.objects.all() if p.user ==
                    request.user]
    for p in card_product:
        tempamount = (p.quantity * p.product.price)
        amount += tempamount

    data = {
        'amount': amount,
        'totalamount': amount 
    }
    return JsonResponse(data)
  






def create_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        product_image = request.FILES['product_image']
        description = request.POST['description']
        quantity = request.POST['quantity']
        price = request.POST['price']
        product = Product(name=name, product_image=product_image, description=description, quntity=quantity, price=price)
        product.save()
        return redirect('home')  # Redirect to the product list page
    return render(request, 'create_product.html')

# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'product_list.html', {'products': products})

def update_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.product_image = request.FILES['product_image']
        product.description = request.POST['description']
        product.quantity = request.POST['quantity']
        product.price = request.POST['price']
        product.save()
        return redirect('home')  # Redirect to the product list page
    return render(request, 'update_product.html', {'product': product})

def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        b= Product.objects.get(pk=pk)
        b.delete()
        return redirect('home')  # Redirect to the product list page
    return render(request, 'delete_product.html', {'product': product})











