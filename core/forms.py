from django import forms
from .models import Book, Membership, BorrowedBook


class BookCreationForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            "title",
            "author",
        )



class MembershipCreationForm(forms.ModelForm):

    CHOICES = [('male','male'),('female','female')]
    gender = forms.CharField(label='What is your gender?', widget=forms.RadioSelect(choices=CHOICES))

    class Meta:
        model = Membership
        fields = (
            "name",
            "email",
            "phone_number",
            "reg",
            "current_level",
            "department",
            "residence_hall",
            "room",
        )



class BookBorrowingForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = {
            "book",
        }
