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
    
    if request.user.is_authenticated:
        return redirect('core:book_list')

    if request.user.is_anonymous:
        return redirect('account:login')

    return render(request, 'account/landing_page.html')


def logging_in(request):
    if request.user.is_authenticated:
        return redirect("core:book_list")

    if request.method == "POST":
        username = request.POST['Username']
        password = request.POST['Password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:member_list')
        else:
            messages.info(request, 'Invalid username/password')
            return redirect('account:login')


    return render(request, "account/login.html")


def logging_out(request):
    logout(request)
    return redirect("account:login")


def terms_and_conditions(request):
    return render(request, "account/terms&conditions.html")