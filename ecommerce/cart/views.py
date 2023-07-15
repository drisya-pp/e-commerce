from django.shortcuts import render,redirect
from cart.models import Cart,Account,Order
from shop.models import Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def cart_view(request):
    total=0
    try:
        user=request.user
        cartitems=Cart.objects.filter(user=user)
        for i in cartitems:
            total+=i.quantity*i.products.price
    except Cart.DoesNotExist:
        pass
    return render(request,'cart.html',{'cart':cartitems,'total':total})

@login_required
def add_cart(request, x):
    products=Product.objects.get(id=x)
    user=request.user
    try:
        cart=Cart.objects.get(products=products,user=user)
        if cart.quantity<cart.products.stock:
            cart.quantity+=1
            cart.save()
    except Cart.DoesNotExist:

        cartitems=Cart.objects.create(products=products,user=user,quantity=1)
        cartitems.save()

    return redirect('cart:cart_view') # render means it returns the html page,redirect means it return function
@login_required
def cart_remove(request, x):
    user=request.user
    products=Product.objects.get(id=x)
    try:
        cart=Cart.objects.get(user=user,products=products)
        if cart.quantity>1:
            cart.quantity-=1
            cart.save()

        else:
            cart.delete()

    except:
        pass
    return redirect('cart:cart_view')

@login_required
def full_remove(request,x):
    user=request.user
    products=Product.objects.get(id=x)
    try:
        cart=Cart.objects.get(user=user,products=products)
        cart.delete()
    except:
        pass
    return redirect('cart:cart_view')

@login_required
def order(request):#p-p means it pass the total amount from cart.html
    total=0
    items=0
    msg=0
    if (request.method=="POST"):
        a=request.POST['a']
        p=request.POST['p']
        ac=request.POST['ac']
        user=request.user
        cart=Cart.objects.filter(user=user)
        for i in cart:
            total+=i.quantity*i.products.price
            items +=i.quantity
        c=Account.objects.get(acctnumber=ac)
        if float(c.amount)>=total:
            c.amount=c.amount-total
            c.save()
            for i in cart:
                o=Order.objects.create(user=user,products=i.products,address=a,phone=p,order_status="paid",noofitems=i.quantity)
                o.save()
            cart.delete()
            msg="Order Placed Successfully"
            return render(request,'orderdetail.html',{'msg':msg,'total':total,'items':items})
        else:
            msg="Order Cannot Be Placed"
            return render(request,'orderdetail.html',{'msg':msg})
    return render(request,'orderform.html')


def orderview(request):
    user=request.user
    o=Order.objects.filter(user=user,order_status="paid")
    return render(request,'orderview.html',{'o':o,'name':user.username})




