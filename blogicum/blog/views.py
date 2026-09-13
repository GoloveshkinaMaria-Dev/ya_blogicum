# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

# Локальные импорты
from .forms import CommentForm, EditUserForm, PostForm
from .models import Category, Comment, Post
from .constants import POSTS_PER_PAGE
from .utils import get_published_posts

User = get_user_model()


def index(request):
    posts = get_published_posts(
        Post.objects.all()
        .annotate(comment_count=Count("comments"))
        .order_by("-pub_date")
    )
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "blog/index.html", {"page_obj": page_obj})


class PostListView(ListView):
    template_name = "blog/index.html"
    context_object_name = "page_obj"
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        return get_published_posts()


def post_detail(request, post_id):

    published_posts_ids = get_published_posts(Post.objects.all()).values_list(
        "id", flat=True
    )
    q = Q(id__in=published_posts_ids)

    if request.user.is_authenticated:
        q = q | Q(author_id=request.user.id)

    # нет доп filter
    post = get_object_or_404(
        Post.objects.annotate(comment_count=Count("comments")), q, id=post_id
    )

    comments = post.comments.all()
    form = CommentForm()

    return render(
        request,
        "blog/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("blog:profile", username=request.user.username)

    return render(request, "blog/create.html", {"form": form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post.id)

    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post.id)

    return render(request, "blog/create.html", {"form": form})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post.id)

    if request.method == "POST":
        post.delete()
        return redirect("blog:index")

    return render(
        request, "blog/create.html", {"form": None, "post_to_delete": post})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    posts = get_published_posts(category.posts.all())
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "blog/category.html",
        {"category": category, "page_obj": page_obj},
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)

    if request.user == author:
        posts = author.posts.select_related("category").all()
    else:
        posts = get_published_posts(
            Post.objects.all()
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "blog/profile.html",
        {"page_obj": page_obj, "profile_user": author},
    )


@login_required
def edit_profile(request):
    form = EditUserForm(request.POST or None, instance=request.user)

    if form.is_valid():
        form.save()
        return redirect("blog:profile", username=request.user.username)

    return render(request, "blog/user.html", {"form": form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

    return redirect("blog:post_detail", post_id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)

    if request.user != comment.author:
        return redirect("blog:post_detail", post_id=post_id)

    form = CommentForm(request.POST or None, instance=comment)

    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post_id)

    return render(
        request, "blog/comment.html", {"form": form, "comment": comment})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment.objects.select_related(
            "author", "post"), id=comment_id, post_id=post_id
    )

    if request.user != comment.author:
        return redirect("blog:post_detail", post_id=post_id)

    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post_id)

    context = {
        "comment": comment,
    }

    return render(request, "blog/comment.html", context)
