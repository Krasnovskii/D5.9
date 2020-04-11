from django.http import HttpResponse, HttpResponseRedirect
from .models import Book
from django.template import loader
from p_library.models import Redaction
from p_library.models import Author
from p_library.forms import AuthorForm, BookForm
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.shortcuts import render



def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)

def index(request):
    template = loader.get_template('index.html')
    books_count = Book.objects.all().count()
    books = Book.objects.all()
    biblio_data = {
        "title": "мою библиотеку",
        "books_count": books_count,
        "books": books,
    }
    return HttpResponse(template.render(biblio_data))


def redactions(request):
    template = loader.get_template('redactions.html')
    redactions = Redaction.objects.all()
    data = {
        "redactions": redactions,
    }
    return HttpResponse(template.render(data, request))


class AuthorEdit(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('p_library:author_list')
    template_name = 'author_edit.html'


class AuthorList(ListView):
    model = Author
    template_name = 'authors_list.html'


def author_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        if author_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
    return render(request, 'manage_authors.html', {'author_formset': author_formset})



def books_authors_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    BookFormSet = formset_factory(BookForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if author_formset.is_valid() and book_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            for book_form in book_formset:
                book_form.save()
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
        book_formset = BookFormSet(prefix='books')
    return render( request, 'manage_books_authors.html', {'author_formset': author_formset, 'book_formset': book_formset})
