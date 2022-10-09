from django.contrib import admin
from .models import Book, BorrowedBook, Membership, Copy, Notification

# Register your models here.

admin.site.register(Book)
admin.site.register(BorrowedBook)
admin.site.register(Membership)
admin.site.register(Copy)
admin.site.register(Notification)

