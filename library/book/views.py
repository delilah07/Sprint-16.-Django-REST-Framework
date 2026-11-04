
from django.shortcuts import render, get_object_or_404

from .models import Book
from .forms import BookSearchForm


def book_list(request):
    books = Book.objects.all()

    form = BookSearchForm(request.GET)

    if form.is_valid():
        title = form.cleaned_data['title']
        author = form.cleaned_data['author']

        if title:
            books = books.filter(name__icontains=title)

        if author:
            books = books.filter(
                authors__name__icontains=author
            ) | books.filter(
                authors__surname__icontains=author
            )

    books = books.distinct()

    return render(request, 'book/book_list.html', {
        'books': books,
        'form': form,
    })


def book_detail(request, book_id):
    selected_book = get_object_or_404(Book, id=book_id)

    return render(request, 'book/book_detail.html', {
        'selected_book': selected_book
    })
