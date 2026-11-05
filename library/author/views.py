
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Author
from .forms import AuthorForm
from authentication.decorators import librarian_required
from .serializers import AuthorSerializer


@librarian_required
def author_list(request):
    error = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            form = AuthorForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('author_list')

        elif action == 'delete':
            form = AuthorForm()

            author_id = request.POST.get('author_id')
            author = get_object_or_404(Author, id=author_id)

            if author.books.exists():
                error = (
                    f'Cannot delete {author.name} {author.surname}: '
                    'this author is associated with books.'
                )
            else:
                author.delete()
                return redirect('author_list')
        else:
            form = AuthorForm()

    else:
        form = AuthorForm()

    authors = Author.get_all()

    return render(
        request,
        'author/author_list.html',
        {
            'authors': authors,
            'form': form,
            'error': error,
        }
    )

@api_view(['GET', 'POST'])
def author_list_api(request):
    if request.method == 'GET':
        authors = Author.get_all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def author_detail_api(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
