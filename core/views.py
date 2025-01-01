from django.contrib.auth.models import User, auth
from django.shortcuts import render , redirect
from django.contrib import messages

from user_profile.models import Profile

def home(request):
    return render(request,'core/home.html',{
        'title': 'Home'

    })

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            #A backend authenticated the credentials.
            auth.login(request, user)
            messages.success(request, 'Login Successfully. Welcome back!')
            print('Login Successfully. Welcome back!')
            return redirect('core:home')
        else:
            #No backend authenticated credentials.
            messages.error(request, 'Invalid Username or Password!')
            print("Invalid Username or Password!")
            return redirect('core:signin')
        
    return render(request, 'core/signin.html',{
        'title': 'signin'
    })

def signup (request):
    if request.method =='POST':
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']
        username =  request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.error(request,'this email already exists.')
                print("this email already exists.")
                return redirect('core:signup')
            
            elif User.objects.filter(username=username).exists():
                messages.error(request,'this username already exists')
                print("this username already exists")
                return redirect('core:signup')
            else:
                #Create user
                new_user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                new_user.save()
                # Log the user using the credentials.
                user_credentials = auth.authenticate(username=username, password=password)
                auth.login(request, user_credentials)
                # Create Profile for the user
                get_new_user = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=get_new_user)
                new_profile.save()
                #Redirect the user
                messages.success(request, 'Account created successfully! Welcome to our Website.')
                print("Account created successfully! Welcome to our Website.")
                return redirect('core:home')
        else:
            messages.error(request, "password don't match")
            print("password don't match.")
            return redirect('core:signup')
    return render(request, 'core/signup.html',{
        'title': 'signup'
    })

def signout(request):
    auth.logout(request)
    messages.success(request, 'Logout Successfull!')
    print('Logout Successfull!.')
    return redirect('core:signin')