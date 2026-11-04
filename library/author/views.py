
from django.shortcuts import render, redirect, get_object_or_404

from .models import Author
from .forms import AuthorForm
from authentication.decorators import librarian_required


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
