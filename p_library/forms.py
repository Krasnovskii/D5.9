from django import forms
from p_library.models import Author, Book
from django.forms import formset_factory


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = '__all__'


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'