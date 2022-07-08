import imp
from site import USER_BASE
from unicodedata import category, name
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from matplotlib.pyplot import title
from .models import Contact, Customer, Product, Cart, OrderPlaced
from .forms import ContactUsForm, CustomerRegistrationForm, CustomerProfileForm, MySellForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#def home(request):
# return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        totalitem = 0
        oldbooks = Product.objects.filter(type='O')
        newbooks = Product.objects.filter(type='N')
        horror = Product.objects.filter(category='H')
        classic = Product.objects.filter(category='C')
        adventure = Product.objects.filter(category='A')
        novel = Product.objects.filter(category='N')
        fiction = Product.objects.filter(category='F')
        educational = Product.objects.filter(category='E')
        kids = Product.objects.filter(category='K')
        mystery = Product.objects.filter(category='M')
        thriller = Product.objects.filter(category='T')
        realistic = Product.objects.filter(category='R')
        sports = Product.objects.filter(category='S')
        inspirational = Product.objects.filter(category='I')

        if request.user.is_authenticated: 
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'oldbooks':oldbooks, 'newbooks':newbooks,'horror': horror,'classic': classic,'adventure': adventure,'novel': novel,'fiction': fiction,'educational': educational,'kids': kids,'mystery': mystery,'thriller': thriller,'realistic': realistic,'sports': sports,'inspirational': inspirational, 'totalitem': totalitem})

@method_decorator(login_required, name='dispatch')
class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        if request.user.is_authenticated: 
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})


def oldbook(request, data=None):
    totalitem=0
    if data == None:
        oldbooks = Product.objects.filter(type='O')
    elif data == 'Educational':
        oldbooks = Product.objects.filter(type='O').filter(category='E')
    elif data == 'Adventure':
        oldbooks = Product.objects.filter(type='O').filter(category='A')
    elif data == 'Novel':
        oldbooks = Product.objects.filter(type='O').filter(category='N')
    elif data == 'Classic':
        oldbooks = Product.objects.filter(type='O').filter(category='C')
    elif data == 'Realistic':
        oldbooks = Product.objects.filter(type='O').filter(category='R')
    elif data == 'Kids':
        oldbooks = Product.objects.filter(type='O').filter(category='K')
    elif data == 'Inspirational':
        oldbooks = Product.objects.filter(type='O').filter(category='I')
    elif data == 'Mystery':
        oldbooks = Product.objects.filter(type='O').filter(category='M')
    elif data == 'Thriller':
        oldbooks = Product.objects.filter(type='O').filter(category='T')
    elif data == 'Sports':
        oldbooks = Product.objects.filter(type='O').filter(category='S')
    elif data == 'Fiction':
        oldbooks = Product.objects.filter(type='O').filter(category='F')
    elif data == 'Horror':
        oldbooks = Product.objects.filter(type='O').filter(category='H')
    elif data == 'below':
        oldbooks = Product.objects.filter(type='O').filter(discounted_price__lt=200)
    elif data == 'above':
        oldbooks = Product.objects.filter(type='O').filter(discounted_price__gt=400)
    if request.user.is_authenticated: 
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/oldbook.html', {'oldbooks':oldbooks, 'totalitem':totalitem})

def newbook(request, data=None):
    totalitem = 0
    if data == None:
        newbooks = Product.objects.filter(type='N')
    elif data == 'Educational':
        newbooks = Product.objects.filter(type='N').filter(category='E')
    elif data == 'Adventure':
        newbooks = Product.objects.filter(type='N').filter(category='A')
    elif data == 'Novel':
        newbooks = Product.objects.filter(type='N').filter(category='N')
    elif data == 'Classic':
        newbooks = Product.objects.filter(type='N').filter(category='C')
    elif data == 'Realistic':
        newbooks = Product.objects.filter(type='N').filter(category='R')
    elif data == 'Kids':
        newbooks = Product.objects.filter(type='N').filter(category='K')
    elif data == 'Inspirational':
        newbooks = Product.objects.filter(type='N').filter(category='I')
    elif data == 'Mystery':
        newbooks = Product.objects.filter(type='N').filter(category='M')
    elif data == 'Thriller':
        newbooks = Product.objects.filter(type='N').filter(category='T')
    elif data == 'Sports':
        newbooks = Product.objects.filter(type='N').filter(category='S')
    elif data == 'Fiction':
        newbooks = Product.objects.filter(type='N').filter(category='F')
    elif data == 'Horror':
        newbooks = Product.objects.filter(type='N').filter(category='H')
    elif data == 'below':
        newbooks = Product.objects.filter(type='N').filter(discounted_price__lt=200)
    elif data == 'above':
        newbooks = Product.objects.filter(type='N').filter(discounted_price__gt=400)
    if request.user.is_authenticated: 
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/newbook.html', {'newbooks':newbooks, 'totalitem':totalitem})
 
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:

        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
   #     print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount, 'totalitem': totalitem})
        else:
            return render(request, 'app/emptycart.html', {'totalitem': totalitem})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data={
            'quantity': c.quantity,
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data={
            'quantity': c.quantity,
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }
        return JsonResponse(data)



def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity -= 1
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data={
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }
        return JsonResponse(data)




def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')



@login_required
def address(request):
    totalitem=0
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated: 
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', {'add': add, 'active':'btn-primary', 'totalitem': totalitem})

@login_required
def orders(request):
    totalitem = 0
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated: 
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html', {'order_placed':op, 'totalitem': totalitem})






class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form}) 

@login_required
def checkout(request):
    totalitem = 0
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount= 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount+shipping_amount
    if request.user.is_authenticated: 
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 'totalitem': totalitem})

@login_required
def payment_done(request):
    totalitem = 0
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer= customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    if request.user.is_authenticated: 
            totalitem = len(Cart.objects.filter(user=request.user))
    return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        form = CustomerProfileForm()
        if request.user.is_authenticated: 
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active':'btn-primary', 'totalitem': totalitem})
    def post(self, request):
        totalitem=0
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr= request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
        if request.user.is_authenticated: 
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
                    

@method_decorator(login_required, name='dispatch')
class SellView(View):
    def get(self, request):
        form = MySellForm()
        
        return render(request, 'app/sell.html', {'form': form, 'active':'btn-primary'})
    def post(self, request):
        form = MySellForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            selling_price = form.cleaned_data['selling_price']
            discounted_price = form.cleaned_data['discounted_price']
            description = form.cleaned_data['description']
            author = form.cleaned_data['author']
            category = form.cleaned_data['category']
            type = form.cleaned_data['type']
            product_image = form.cleaned_data['product_image']
            reg = Product(title=title, selling_price=selling_price, discounted_price=discounted_price, description=description, author=author, category=category, type=type, product_image=product_image)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
        
        return render(request, 'app/sell.html', {'form':form, 'active':'btn-primary'})


@method_decorator(login_required, name='dispatch')
class ContactView(View):
    def get(self, request):
        form = ContactUsForm()
        
        return render(request, 'app/contact.html', {'form': form, 'active':'btn-primary'})
    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            mobileno = form.cleaned_data['mobileno']
            message = form.cleaned_data['message']
            
            reg = Contact(name=name, email=email, mobileno=mobileno, message=message)
            reg.save()
            messages.success(request, 'Thanks for sending your message! We will get back to you shortly..')
        
        return render(request, 'app/contact.html', {'form':form, 'active':'btn-primary'})

class SearchView(View):
    def get(self, request):
        q= request.GET['q']
        totalitem = 0
        oldbooks = Product.objects.filter(title__icontains=q).order_by('-id')
        newbooks = Product.objects.filter(title__icontains=q).order_by('-id')
        horror = Product.objects.filter(title__icontains=q).order_by('-id')
        classic = Product.objects.filter(title__icontains=q).order_by('-id')
        adventure = Product.objects.filter(title__icontains=q).order_by('-id')
        novel = Product.objects.filter(title__icontains=q).order_by('-id')
        fiction = Product.objects.filter(title__icontains=q).order_by('-id')
        educational = Product.objects.filter(title__icontains=q).order_by('-id')
        kids = Product.objects.filter(title__icontains=q).order_by('-id')
        mystery = Product.objects.filter(title__icontains=q).order_by('-id')
        thriller = Product.objects.filter(title__icontains=q).order_by('-id')
        realistic = Product.objects.filter(title__icontains=q).order_by('-id')
        sports = Product.objects.filter(title__icontains=q).order_by('-id')
        inspirational = Product.objects.filter(title__icontains=q).order_by('-id')

        if request.user.is_authenticated: 
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/search.html', {'oldbooks':oldbooks, 'newbooks':newbooks,'horror': horror,'classic': classic,'adventure': adventure,'novel': novel,'fiction': fiction,'educational': educational,'kids': kids,'mystery': mystery,'thriller': thriller,'realistic': realistic,'sports': sports,'inspirational': inspirational, 'totalitem': totalitem})



