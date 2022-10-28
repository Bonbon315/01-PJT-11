from django import views
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm, CommentForm
from .models import Review
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    reviews = Review.objects.all()
    context = {"reviews": reviews}
    return render(request, "reviews/index.html", context)


def detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    comment_form = CommentForm()

    context = {
        "review": review,
        "comments": review.comment_set.all(),
        "comment_form": comment_form,
    }
    return render(request, "reviews/detail.html", context)


@login_required
def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("reviews:index")
    else:
        review_form = ReviewForm()
    context = {"review_form": review_form}
    return render(request, "reviews/create.html", context=context)


@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        if request.method == "POST":
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                review_form.save()
                return redirect("reviews:detail", review.pk)
        else:
            review_form = ReviewForm(instance=review)
        context = {"review_form": review_form}
        return render(request, "reviews/update.html", context)
    else:
        return redirect("reviews:detail", review.pk)


@login_required
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        if request.method == "POST":
            review.delete()
            return redirect("reviews:index")
    else:
        return redirect("reviews:detail", review.pk)
    return render(request, "reviews/detail.html")


@login_required
def like(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user in review.like_users.all():
        review.like_users.remove(request.user)
        is_liked = False
    else:
        review.like_users.add(request.user)
        is_liked = True
    context = {
        "isLiked": is_liked,
        "likeCount": review.like_users.count(),
    }
    return redirect("reviews:detail", review.pk)


# 홈페이지
def home(request):
    return render(request, "reviews/home.html")


# 댓글기능
@login_required
def comment_create(request, pk):
    review = get_object_or_404(Review, pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()

        context = {
            "content": comment.content,
            "userName": comment.user.username,
        }
        return redirect("reviews:detail", review.pk)


@login_required
def comment_delete(request, review_pk, comment_pk):
    review = Review.objects.get(pk=review_pk)
    comment = review.comment_set.get(pk=comment_pk)
    if request.user == comment.user:
        if request.method == "POST":
            comment.delete()
    return redirect("reviews:detail", review.pk)
