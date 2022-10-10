from django.shortcuts import render, redirect
from .forms import AccountCreationForm
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from core.models import Notification, BorrowedBook
import datetime

# Create your views here.

def landing_page(request):
    book = BorrowedBook.objects.all()
    clock = datetime.datetime.now()
    date = clock.date()

    for copy in book:
        if copy.date_to_be_returned == date:
            notification_heading = "Due Book Return"
            notification_message = f"{copy.borrower.name} borrowed a book on {copy.date_borrowed} to be returned on {copy.date_to_be_returned}"
            alert = Notification.objects.create(heading=notification_heading, message=notification_message)
            alert.save()

    return render(request, 'account/landing_page.html')


def signing_up(request):
    if request.user.is_authenticated:
        return redirect("core:book_list")
        
    form = AccountCreationForm()

    if request.method == "POST":
        form = AccountCreationForm(request.POST)

        if request.POST.get("submit"):
            if form.is_valid():
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                password2 = form.cleaned_data["confirm_password"]
                username = last_name + "-" + first_name

                if User.objects.filter(email=email).exists():
                    messages.info(request, "Email address already being used!")
                    return redirect("account:signup")

                elif first_name == "":
                    messages.info(request, "First name cannot be empty")
                    return redirect("account:signup")

                elif last_name == "":
                    messages.info(request, "Last Name cannot be empty")
                    return redirect("account:signup")

                elif email == "":
                    messages.info(request, "Email address already Empty")
                    return redirect("account:signup")

                elif password == "" or password2 == "":
                    messages.info(request, "Passwords cannot be empty")
                    return redirect("account:signup")
                    
                elif len(password) < 8:
                    messages.info(request, "Passwords should be more than eight characters")
                    return redirect("account:signup")

                elif password == password2:
                    print(f"The passwords are a match: {password}")

                    owner = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                    owner.save

                    # login
                    user = authenticate(username=username, password=password)
                    login(request, user)

                    notification_heading = "Account Creation"
                    notification_message = f"An account for {username} has successfully being created"
                    alert = Notification.objects.create(heading=notification_heading, message=notification_message)
                    alert.save()

                    return redirect("core:member_list")
                else:
                    messages.info(request, "Passwords do not match!")
                    return redirect("account:signup")


    return render(request, "account/signup.html", {"form": form})


def logging_in(request):
    if request.user.is_authenticated:
        return redirect("core:book_list")

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(email=email).exists():
            potential_user = User.objects.get(email=email)
            kinetic_user = potential_user.username

            if potential_user.check_password(password):
                print(password)
                
                logged_user = authenticate(username=kinetic_user, password=password)
                login(request, logged_user)
                messages.success(request, f"Logged in as {email}")
                return redirect("core:member_list")
            else:
                messages.info(request, "Email/Password doesn't exist")
                return redirect("accounts:login")
        else:
            messages.info(request, "Email/Password doesn't exist")
            return redirect("account:login")

    return render(request, "account/login.html")


def logging_out(request):
    logout(request)
    return redirect("account:login")


def terms_and_conditions(request):
    return render(request, "account/terms&conditions.html")