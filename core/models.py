from random import choices
from django.db import models
from datetime import datetime
from account.models import User

# Create your models here.


class Membership(models.Model):
    HALLS = (
        ("Abigail", "Abigail"),
        ("Abraham", "Abraham"),
        ("Daniel", "Daniel"),
        ("Deborah", "Deborah"),
        ("Dorcas", "Dorcas"),
        ("Isaac", "Isaac"),
        ("Daniel", "Daniel"),
        ("Joseph", "Joseph"),
        ("Sarah", "Sarah"),
    )
    COLLEAGE = (
        ("College of Pure and Applied Sciences", "College of Pure and Applied Sciences"),
        ("College of Engineering", "College of Engineering"),
        ("College of Business and Social Sciences", "College of Business and Social Sciences"),
        ("College of Agricultural Sciences", "College of Agricultural Sciences"),
    )

    LEVEL = (
        ("100", "100"),
        ("200", "200"),
        ("300", "300"),
        ("400", "400"),
        ("500", "500"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    gender = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    reg = models.CharField(max_length=50)
    current_level = models.CharField(max_length=2000, choices=LEVEL)

    # address
    residence_hall = models.CharField(max_length=20, choices=HALLS)
    room = models.CharField(max_length=5)

    # college
    college = models.CharField(max_length=500, choices=COLLEAGE)
    department = models.CharField(max_length=500)

    date_joined = models.DateTimeField(default=datetime.now)

    def __str__(self):
        if self.reg:
            return self.reg
        else:
            return self.name


# including books
class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200)
    location = models.CharField(max_length=500)
    quantity = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title


class Copy(models.Model):
    book = models.Foreign   Key(Book, related_name="copies", on_delete=models.CASCADE)
    unique_number = models.CharField(max_length=1000)

    def __str__(self):
        return self.unique_number


# Borrowing books
class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, related_name="borrowed_book", on_delete=models.CASCADE)
    copy = models.ForeignKey(Copy, related_name="borrowed_book_copy", on_delete=models.CASCADE)
    borrower = models.ForeignKey(Membership, related_name="borrowed_book", on_delete=models.CASCADE)
    date_borrowed = models.DateTimeField(default=datetime.now)
    date_to_be_returned = models.DateField()


class Notification(models.Model):
    heading = models.CharField(max_length=250)
    message = models.CharField(max_length=5000)

    date_created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.account.username