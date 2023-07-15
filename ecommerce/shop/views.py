from django.shortcuts import render
from  shop.models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from  cart.models import Cart

def allprodCat(request):
    c=Category.objects.all()
    return render(request,'category.html',{'c':c})

def allproducts(request,cslug):
    c=Category.objects.get(slug=cslug)
    p=Product.objects.filter(category__slug=cslug)
    return render(request,'products.html',{'p':p,'c':c})

def productdetails(request,yslug):
    x=Product.objects.get(slug=yslug)
    return render(request,'detail.html',{'x':x})

def register(request):
    if (request.method=="POST"):
        u=request.POST['u']
        f=request.POST['f']
        l=request.POST['l']
        e=request.POST['e']
        p=request.POST['p']
        cp=request.POST['cp']
        if p==cp:
            user=User.objects.create_user(username=u,first_name=f,last_name=l,email=e,password=p)
            user.save()
            return allprodCat(request)
    return render(request,'register.html')

def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return allprodCat(request)
        else:
            messages.error(request,"Invalid credentials")
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return allprodCat(request)



