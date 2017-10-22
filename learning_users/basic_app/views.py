from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# Imports required for login functionality
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

# Logout functionality only works when someone is logged in
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# Special function to show that login successful
@login_required
def special(request):
    return HttpResponse("You are logged in !!!")

def register(request):
    # Set a variable registered as false
    registered = False

    # If the form is submitted through POST
    if request.method == 'POST':
        # Creating the form objects using the submitted data and storing the reference of the objects
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Checking the validations of both the forms
        if user_form.is_valid() and profile_form.is_valid():
            # Saving the user info to the database and holding its reference
            user = user_form.save()
            # using the same form object fetching the password attribute of the user object and hashing the password using predefined method set_password
            user.set_password(user.password)
            # Saving the changes to the database
            user.save()

            # Saving the profile_form but not commiting because we need to link it with the above user_form using onetoone relationship
            profile = profile_form.save(commit=False)
            # linking the profile object's user attribute with the user object
            profile.user = user

            # Checking if profile pic exists in the submitted files
            if 'profile_pic' in request.FILES:
                # setting up the profile_pic attribute in the profile_form to with the uploaded profile pic image
                profile.profile_pic = request.FILES['profile_pic']

            # Finally saving it to the database
            profile.save()
            # Set the registered variable as true because the registration was successful
            registered = True
        else: # If forms are invalid
            print(user_form.errors, profile_form.errors)
    else: # If the request was not POST and the form is not submitted
        # Setup the form
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})

# Login method view // Never name a method same as the imports
def user_login(request):
    # Checking if someone is logging in using POST method
    if request.method == "POST":
        # fetching the username and password submitted by the user
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate the username and password using authenticate method provided by django
        user = authenticate(username=username,password=password)

        # After authentication if user exists
        if user:
            # Checking if the user is active
            if user.is_active:
                # Now login the user using the django function login
                login(request,user)
                # after logging in redirect the user where ever we want
                return HttpResponseRedirect(reverse('index'))
            else: # If account is not active
                return HttpResonse("ACCOUNT NOT ACTIVE")
        else: # If user authentication fails
            print("Someone tried to login")
            print("Username: {} Password: {}".format(username,password))
            return HttpResonse("Invalid Login Details")
    else: # If login was not submitted
        return render(request, 'basic_app/login.html', {})
