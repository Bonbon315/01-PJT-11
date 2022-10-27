from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from reviews.models import Review

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("accounts:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


def index(request):
    users = get_user_model().objects.all()
    context = {
        "users": users,
    }
    return render(request, "accounts/index.html", context)


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    articles = Review.objects.all()
    context = {
        "user": user,
        "articles": articles,
    }
    return render(request, "accounts/detail.html", context)


def logout(request):
    auth_logout(request)
    return redirect("accounts:index")


@login_required
def follow(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.user == user:
        return redirect("accounts:detail", pk)
    if request.user in user.followers.all():
        # unfollow
        user.followers.remove(request.user)
    else:
        # follow
        user.followers.add(request.user)
    return redirect("accounts:detail", pk)
