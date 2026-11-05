
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .forms import BookSearchForm
from .serializers import BookSerializer


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

@api_view(['GET','POST'])
def book_list_api(request):
    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def book_detail_api(request, book_id):
    selected_book = get_object_or_404(Book, id=book_id)
    if request.method == 'GET':
        serializer = BookSerializer(selected_book)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = BookSerializer(selected_book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        serializer = BookSerializer(selected_book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        selected_book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)