
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404

from .models import CustomUser
from .decorators import librarian_required

from .forms import RegisterForm, LoginForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'authentication/register.html', {
        'form': form,
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                email=email,
                password=password,
            )

            if user is not None:
                login(request, user)
                return redirect('home')

            form.add_error(None, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {
        'form': form,
    })


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

    return redirect('home')

@librarian_required
def user_list_view(request):
    users = CustomUser.objects.all().order_by('last_name', 'first_name')

    return render(request, 'authentication/user_list.html', {
        'users': users,
    })

@librarian_required
def user_detail_view(request, user_id):
    selected_user = get_object_or_404(CustomUser, id=user_id)

    return render(request, 'authentication/user_detail.html', {
        'selected_user': selected_user,
    })