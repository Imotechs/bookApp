from django.shortcuts import render,redirect
from . forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

# Create your views here.

def register(request):
    if request.method == 'POST':
        if User.objects.filter(email = request.POST['email']):
            context = {
                'msg': 'Email already registered!',
            }
            return render(request,'register.html',context)
        else:
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username','email')
                messages.success(request, f'{username}, Your account was created!  Login Now')
                return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {"form":form,"title":"User Registration"})

def login(request):
    form = UserRegisterForm()
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                messages.info(request,'Welcome!')
                return redirect('profile')
            else:
                msg = {'msg':'Your Account is not active!'}
                return render(request,'login.html', {'msg':msg,'form':form})
        elif user is None:
            context = {
                'msg':'No User with this Credentials!',
                'form':form
            }
                
            return render(request,'login.html', context)

    context = {
                'form':form
            }   
    return render(request,'login.html',context)


def home(request):
    return render(request,'book/index.html')