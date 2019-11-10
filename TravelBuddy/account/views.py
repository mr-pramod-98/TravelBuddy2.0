from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
import re


# Create your views here.
# "register" METHOD IS CALLED WHET THE USER REQUEST FOR "register" PAGE
def register(request):

    # IF THE REQUEST METHOD IS POST EXECUTE if BLOCK
    if request.method == 'POST':

        # READING THE SENT DATA FROM THE REGISTRATION FORM
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password_conf']

        # FORM VALIDATION --> START

        # CHECKING WEATHER ALL THE FIELDS ARE FILLED
        if len(first_name) != 0 and len(last_name) != 0 and len(username) != 0 and len(password1) != 0 and len(email) != 0:

            # CHECKING WEATHER "username" STARTS WITH ALPHABETS
            if re.match(r'^[a-z,A-Z]+', username) is not None:

                # CHECKING FOR THE FORMAT CORRECT USERNAME-FORMAT
                username_format = re.match(r'[a-z,A-Z]+[a-z,A-Z,0-9]*[_]*[a-z,A-Z,0-9]*', username)
                if username_format is not None and username_format.span()[1] == len(username):

                    # ALL TEST-CASES ARE PASSED
                    pass

                else:

                    # IF THE USERNAME CONTAINS ANY SPECIAL CHARACTER OTHER THEN UNDERSCORE
                    # THEN REDIRECTING THE USER BACK TO THE "register" PAGE
                    messages.info(request, "no special character other then underscore(_) is allowed")
                    return redirect('register')
            else:

                # IF THE USERNAME DOES NOT START WITH A ALPHABET THEN REDIRECTING THE USER BACK TO THE "register" PAGE
                messages.info(request, "username should start with alphabet")
                return redirect('register')
        else:

            # IF ALL THE DETAILS ARE NOT FILLED THEN REDIRECTING THE USER BACK TO THE "register" PAGE
            messages.info(request, "fill all details")
            return redirect('register')

        # CHECKING WEATHER BOTH "Password" AND "Confirm Password" FIELDS CONTAIN SAME STRING
        if password1 == password2:

            if User.objects.filter(username=username).exists():

                # IF THE USERNAME IS TAKEN THEN REDIRECTING THE USER BACK TO THE "register" PAGE
                messages.info(request, "username taken")
                return redirect('register')

            else:

                # CREATING A USER RECORD IN THE "User" TABLE
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password2)

                # SAVING THE CHANGES
                user.save()

                # REDIRECTING TO "login" PAGE AFTER USER VERIFICATION AND REGISTRATION
                return redirect('login')

        else:

            # IF THE PASSWORD DOES NOT MATCH THEN REDIRECTING THE USER BACK TO THE "register" PAGE
            messages.info(request, "password not matching")
            return redirect('register')

        # FORM VALIDATION --> END

    # IF THE REQUEST METHOD IS GET EXECUTE else BLOCK
    else:
        return render(request, 'register.html')


# "login" METHOD IS CALLED WHET THE USER REQUEST FOR "login" PAGE
def login(request):

    # IF THE REQUEST METHOD IS POST EXECUTE if BLOCK
    if request.method == "POST":

        # FETCHING "username" AND "password" FROM THE LOGIN PAGE
        username = request.POST['username']
        password = request.POST['password']

        # AUTHENTICATING THE USER
        # "user" EQUALS "None" IF THE "username" DOES NOT MATCH WITH IT'S THE CORRESPONDING "password"
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            # REDIRECTING TO "cook_guide/<username>" PAGE AFTER SUCCESSFUL LOGIN
            # EXAMPLE: /cook_guide/pramod
            return redirect('/travello/TravelBuddy/' + username + '/')
        else:
            messages.info(request, "invalid username or password")

            # REDIRECTING BACK TO "login" IF THE "username" DOES NOT MATCH WITH IT'S THE CORRESPONDING "password"
            return redirect('login')

    # IF THE REQUEST METHOD IS GET EXECUTE else BLOCK
    else:
        return render(request, 'login.html')


# "logout" METHOD IS CALLED WHET THE USER LOGOUT'S OF HIS ACCOUNT
def logout(request):

    # LOGGING-OUT THE USER
    auth.logout(request)

    # REDIRECTING THE USER TO THE HOME PAGE
    return redirect('/')
