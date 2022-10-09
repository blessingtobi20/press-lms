from copy import copy
from email import message
from django.shortcuts import render, redirect
from .models import BorrowedBook, Membership, Notification, Book, Copy
from .forms import BookCreationForm, MembershipCreationForm, BookBorrowingForm
from .serial_num_generator import auto_generate
from django.contrib import messages
from account.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# Create your views here.

'''members management'''
@login_required
def member_list(request):
    member = Membership.objects.all()
    book = Book.objects.all()
    return render(request, "core/member-list.html", {"member": member, "book": book})


def member_create(request):
    current_user = request.user

    form = MembershipCreationForm()
    if request.method == "POST":
        form = MembershipCreationForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            number = form.cleaned_data["phone_number"]
            reg = form.cleaned_data["reg"]
            level = form.cleaned_data['current_level']
            gender = form.cleaned_data['gender']
            hall = form.cleaned_data['residence_hall']
            block = form.cleaned_data['hall_block']
            room = form.cleaned_data['room']

            college = form.cleaned_data['college']
            department = form.cleaned_data['department']

            new_member = Membership.objects.create(user=current_user, name=name, email=email, phone_number=number,
                                                    reg=reg, current_level=level, gender=gender,
                                                    residence_hall=hall, hall_block=block,
                                                    room=room, college=college, department=department)
            new_member.save()

            notification_heading = "Membership Creation"
            notification_message = f"Membership for {name} created successfully by {current_user.username}"
            alert = Notification.objects.create(heading=notification_heading, message=notification_message)
            alert.save()

            messages.success(request, "Member added successfully")
            return redirect("core:member_list")
        else:
            messages.info(request, "There is a problem in your form!")
            return redirect("core:member_create")

    return render(request, "core/member-create.html", {"form": form})


def member_detail(request, pk):
    current_user = request.user

    member = Membership.objects.get(id=pk)

    book = []
    if member.borrowed_book.exists():
        borrowed_book = member.borrowed_book.all()
        
        for item in borrowed_book:
            book.append(item)

            if request.method == "POST":    
                if request.POST.get("returnBook"):
                    item.delete()

                    notification_heading = "Book Returning"
                    notification_message = f"{member.name} returned a '{item.book.title}': {item.borrowed_book_copy.unique_number}"
                    alert = Notification.objects.create(heading=notification_heading, message=notification_message)
                    alert.save()

                    messages.info(request, 'Book has being returned')
                    return redirect("core:member_detail", member.id)

    if request.method == "POST":
        if request.POST.get("remove"):
            member.delete()

            messages.success(request, "Membership terminated successfully")
            return redirect("core:member_list")

    return render(request, "core/member-detail.html", {"member": member, "book": book})


def book_borrow(request, pk):
    current_user = request.user

    book = Book.objects.all()
    member = Membership.objects.get(id=pk)
    form = BookBorrowingForm()

    if request.method == "POST":
        form = BookBorrowingForm(request.POST)
        if form.is_valid():
            book_name = form.cleaned_data["book"]
            return_date = request.POST["return_date"]
            unique_num = request.POST["serial_num"]            

            if Book.objects.filter(title=book_name).exists():
                the_book = Book.objects.get(title=book_name)

                if Copy.objects.filter(unique_number=unique_num):
                    book_copy = Copy.objects.get(unique_number=unique_num)

                    if the_book == book_copy.book:

                        if BorrowedBook.objects.filter(copy=book_copy.id).exists():
                            messages.info(request, "Book with that serial number has been borrowed")
                            return redirect("core:book_borrow", member.id)
                        else:
                            borrow_book = BorrowedBook.objects.create(book=book_name, copy=book_copy, 
                                                                        borrower=member, date_to_be_returned=return_date)

                            borrow_book.save()

                            notification_heading = "Book Borrowing"
                            notification_message = f"{member.email} borrowed '{book_name}' with serial number '{book_copy}'"
                            alert = Notification.objects.create(heading=notification_heading, message=notification_message)
                            alert.save()

                            messages.success(request, "Book borrowed successfully")
                            return redirect("core:member_detail", member.id)
                    else:
                        messages.info(request, "Book doesn't have such serial number")
                        return redirect("core:book_borrow", member.id)
                else:
                    messages.info(request, "Serial number doesn't exists")
                    return redirect("core:book_borrow", member.id)

    else:
        return render(request, "core/book-borrow.html", {"book": book, "member": member, "form": form})


'''book management'''
@login_required
def book_list(request):
    book = Book.objects.all()
    counting = 0
    return render(request, "core/book-list.html", {"book": book, "counting": counting})


def book_create(request):
    form = BookCreationForm()

    if request.method == "POST":
        form = BookCreationForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            location = form.cleaned_data['location']

            new_book = Book.objects.create(title=title, author=author, location=location)
            new_book.save()

            return redirect("core:book_copy", new_book.id)

            '''
            # To create many books as possible
            # amount = 0
            # if amount < quantity:
            #     while amount < quantity:
            #         amount += 1
            #         serial = auto_generate(n=10)
            #         book = Copy.objects.create(book=new_book, unique_number=serial)
            #         book.save()

            #     notification_heading = "Book Creation"
            #     notification_message = f"Uploaded '{title}' book with {quantity} copies"
            #     alert = Notification.objects.create(heading=notification_heading, message=notification_message)
            #     alert.save()

            #     messages.info(request, "Book added Successfully!")
            #     return redirect("core:book_list")
            
            else:
                new_book.delete()
                messages.info(request, "Book quantity field error")
                return redirect("core:book_create")
                '''
        else:
            messages.info(request, "Form is not valid!")
            return redirect("core:book_create")
    else:
        return render(request, "core/book-create-form.html", {"form": form})



def copy_create(request, pk):
    book = Book.objects.get(id=pk)

    if request.method == 'POST':

        if request.POST.get('save'):
            if request.POST.get('book_number') == "":
                messages.info(request, "You did not add a book number!")
                return redirect("core:book_copy", book.id)
            
            book_number = request.POST.get('book_number')

            copy = Copy.objects.create(book=book, unique_number=book_number)
            copy.save
            
            book.quantity = book.quantity + 1
            book.save()

            messages.success(request, 'Copy added successfully')
            return redirect("core:book_detail", book.id)

        elif request.POST.get('save_and_continue'):
            if request.POST.get('book_number') == "":

                messages.info(request, "You did not add a book number!")
                return redirect("core:book_copy", book.id)

            book_number = request.POST.get('book_number')

            copy = Copy.objects.create(book=book, unique_number=book_number)
            copy.save

            book.quantity = book.quantity + 1
            book.save()

            messages.info(request, 'Copy added successfully')
            return redirect("core:book_copy", book.id)

        elif request.POST.get('deleteBook'):
            book.delete()

            messages.success(request, 'Book removed successfully')
            return redirect("core:book_list")

    return render(request, 'core/copy-create-form.html', {"book": book})



def book_detail(request, pk):
    book = Book.objects.get(id=pk)
    book_copy = book.copies.all()

    borrowed_book_amount = 0
    
    books = [] # "books" is for borrowed books

    for item in book_copy:
        if BorrowedBook.objects.filter(copy=item).exists():
            borrowed_book_amount += 1
            books.append(item)

    optional = 0
    # the purpose of using optional is to check whether a book has being borrowed
    # therefore it can't be deleted or updated
    for book in book_copy: 
        while book.borrowed_book_copy.exists():
            optional += 1
            break
        else:
            pass
      
    return render(request, "core/book-detail.html", {"book": book,
                                                    "books_borrowed": books,
                                                    "borrowed_book_amount": borrowed_book_amount,
                                                    "book_copy": book_copy,
                                                    "books": books,
                                                    "optional": optional})


def book_update(request, pk):
    current_user = request.user
    if Library.objects.filter(owner=current_user):
        library = Library.objects.get(owner=current_user)

    book = Book.objects.get(id=pk)
    book_amount =  book.quantity_serial.all()
    book_form = BookCreationForm(instance=book)

    optional = 0
    # the purpose of using optional is to check whether a book has being borrowed
    # therfore it can't be updated
    for item in book_amount: 
        while item.borrowed_book_serial.exists():
            optional += 1
            break
        else:
            pass
    
    book_amount_list = []

    if book_amount:
        for item in book_amount:
            book_amount_list.append(item)
    
    if request.method == "POST":
        book_form = BookCreationForm(request.POST, instance=book)
        if request.POST.get("done"):
            if book_form.is_valid():
                title = book_form.cleaned_data['title']
                author = book_form.cleaned_data['author']
                location = book_form.cleaned_data['location']
                quantity = book_form.cleaned_data['quantity']
                image = book_form.cleaned_data['cover']

                if request.POST.get("keep_changes"):
                    # appending new copies and old copies
                    amount = 0
                    if amount < quantity:
                        while amount < quantity:
                            amount += 1
                            serial = auto_generate(n=10)
                            new_book_copy = BookAmount.objects.create(book=book, serial_number=serial)
                            new_book_copy.save()
                            book_amount_list.append(new_book_copy)

                        book.title = title
                        book.author = author
                        book.location = location
                        book.quantity = len(book_amount_list)
                        book.image = image

                        book.save()

                        notification_heading = "Book Update"
                        notification_message = f"Edited '{title}' book with ({quantity}) added copies"
                        alert = Notification.objects.create(library_name=library, heading=notification_heading, message=notification_message)
                        alert.save()

                        messages.success(request, "Update successful")
                        return redirect("core:book_detail", book.id)
                    else:
                        messages.info(request, "Book quantity field error")
                        return redirect("core:book_update", book.id)
                else:
                    amount = 0
                    if amount < quantity:
                        # Deleting previous copies
                        for item in book_amount_list:
                            if BookAmount.objects.filter(serial_number=item).exists():
                                item.delete()

                        # adding new copies
                        while amount < quantity:
                            amount += 1
                            serial = auto_generate(n=10)
                            new_book_copy = BookAmount.objects.create(book=book, serial_number=serial)
                            new_book_copy.save()

                        book_form.save()

                        notification_heading = "Book Update"
                        notification_message = f"Edited '{title}' book with ({quantity}) new copies"
                        alert = Notification.objects.create(library_name=library, heading=notification_heading, message=notification_message)
                        alert.save()

                        messages.success(request, 'Update Successful')
                        return redirect("core:book_detail", book.id)
                    else:
                        messages.info(request, "Book quantity field error")
                        return redirect("core:book_update", book.id)
            else:
                messages.info(request, 'Form input is invalid!')
                return redirect("core:book_update", book.id)
                    
                    
    return render(request, 'core/book-update.html', {"book_form": book_form,
                                                    "book": book,
                                                    "book_amount_list": book_amount_list,
                                                    "optional": optional})


def book_delete(request, pk):
    current_user = request.user
    if Library.objects.filter(owner=current_user):
        library = Library.objects.get(owner=current_user)

    book = Book.objects.get(id=pk)
    book_amount = book.quantity_serial.all()    


    optional = 0
    # the purpose of using optional is to check whether a book has being borrowed
    # therfore it can't be deleted
    for item in book_amount: 
        while item.borrowed_book_serial.exists():
            optional += 1
            break
        else:
            pass
        
    if request.POST.get("confirmDelete"):
        book.delete()

        notification_heading = "Book Deleting"
        notification_message = f"Deleted '{book.title}' book and ({book.quantity}) copies with it"
        alert = Notification.objects.create(library_name=library, heading=notification_heading, message=notification_message)
        alert.save()

        messages.success(request, "Book removed successfully")
        return redirect("core:book_list")


    return render(request, "core/book-delete.html", {"book": book, "optional": optional})



'''notifications'''
def notification(request):
    notify = Notification.objects.all()
    return render(request, 'core/notification.html', {"notify": notify})


'''profile'''
def profile(request):
    user = request.user
    return render(request, 'profile/dashboard.html', {"user": user,})


def profile_member(request):
    member = Membership.objects.all()
    member_counter = 0

    borrowed_counter = 0

    for item in member:
        if item.library_name.owner == request.user:
            member_counter += 1
            if item.borrowed_book_name.exists():
                borrowed_counter += 1
                

    return render(request, "profile/members.html", {"member_counter": member_counter,
                                                    "borrowed": borrowed_counter})


def profile_book(request):
    book_amount = BookAmount.objects.all()
    borrowed_book = BorrowedBook.objects.all()
    book_counter = 0
    book = 0

    for item in book_amount:
        if item.book.library_name.owner == request.user:
            book_counter += 1


    for item2 in borrowed_book:
        if item2.book.library_name.owner == request.user:
            book += 1



    return render(request, "profile/books.html", {"book_counter": book_counter,
                                                    "borrowed_book": book})


def profile_library_delete(request):
    the_libarary = Library.objects.get(owner=request.user)
    current_user = request.user

    if request.method == "POST":
        if request.POST.get('Sure'):
            the_libarary.delete()
            current_user.delete()
            return redirect("account:login")

    return render(request, 'profile/library-option.html')


def profile_password_change(request):
    current_user = request.user
    if Library.objects.filter(owner=current_user):
        library = Library.objects.get(owner=current_user)


    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password1 = request.POST["new_password1"]
        new_password2 = request.POST["new_password2"]
        
        if old_password and new_password1 and new_password2:

            if request.user.is_authenticated:
                user = User.objects.get(email=request.user.email)

                if user.check_password(old_password):

                    if new_password1 == new_password2:

                        if len(new_password1) >= 8:
                            user.set_password(new_password1)
                            user.save()

                            username = user.username

                            login_again = authenticate(username=username, password=new_password1)
                            login(request, login_again)

                            '''Try to make change password to not log out'''
                            notification_heading = "Password Change"
                            notification_message = f"Your account password was changed"
                            alert = Notification.objects.create(library_name=library, heading=notification_heading, message=notification_message)
                            alert.save()

                            messages.success(request, "Password Changed Successfully")
                            return redirect("core:profile")
                        else:
                            messages.info(request, "New Password Characters should not be less than 8")
                            return redirect("core:profile_password_change")
                    else:
                        messages.info(request, "New passwords did not match!")
                        return redirect("core:profile_password_change")
                else:
                    messages.info(request, "Old Password is not correct")
                    return redirect("core:profile_password_change")
        else:
            messages.info(request, "Please completely fill the form")
            return redirect("core:profile_password_change")
    else:
        return render(request, "profile/password-change.html")