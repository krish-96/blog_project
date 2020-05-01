from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactUsForm, SignUpForm, CommentForm, CreatePostForm, UpdateAuthorForm
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Post, Author, Comment, Public_Post, Author_Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

@unauthenticated_user
def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            name = request.POST.get('username')
            messages.success(request, f'{name} account created successfully.')
            return redirect('blog:login')
        else:
            messages.error(request, 'Please Correct the errors!')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'blog/register.html', context)

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username.upper()}! You are logged in.")
            return redirect('blog:dashboard')
        else:
            messages.info(request, 'Username OR Password is incorrect!')
    context = {}
    return render(request, 'blog/new_login.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "Thanks for using our web services. You are logged out.")
    return redirect('blog:login')


def home(request):
    context = {}
    return render(request, 'blog/index.html', context)


@login_required(login_url='blog:login')
def dashboard_view(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()

    my_posts = posts.filter(creator=request.user.author)
    my_total_posts = my_posts.count()
    my_total_published_posts = my_posts.filter(status='P').count()
    my_total_draft_posts = my_posts.filter(status='D').count()
    # my_total_public_posts = my_posts.filter(privacy='Public').count()
    my_total_public_posts = my_posts.filter(status='P', privacy='Public').count()
    my_total_private_posts = my_posts.filter(privacy='Private').count()

    latest_posts = posts.order_by('-published_date')[:5:]
    top_posts = []
    for post in posts:
        com_count = post.comment_set.all().count()
        post_title = post.title
        t = (com_count, post_title)
        top_posts.append(t)
    top_posts.sort(reverse=True)
    most_commented = []
    context = {
        'latest_posts': latest_posts,
        'comments': comments,
        'most_commented': most_commented,
        'my_total_posts': my_total_posts,
        'my_total_public_posts': my_total_public_posts,
        'my_total_private_posts': my_total_private_posts,
        'my_total_published_posts': my_total_published_posts,
        'my_total_draft_posts': my_total_draft_posts,
    }

    return render(request, 'blog/user-dashboard.html', context)


@login_required(login_url='blog:login')
def profile_view(request):
    author = Author.objects.get(slug=request.user)
    post_list = author.post_set.all()

    total_posts = post_list.count()
    recent_posts = post_list.order_by('-published_date')[:5:]

    context = {'post_list': post_list,
               'author': author,
               'total_posts': total_posts,
               'recent_posts': recent_posts,
               }
    return render(request, 'blog/user_profile.html', context)


@login_required(login_url='blog:login')
def settings_view(request):
    author = Author.objects.get(slug=request.user)
    context = {'author': author}
    return render(request, 'blog/settings.html', context)


class AuthorPostsList(ListView):
    model = Author_Post
    paginate_by = 5
    template_name =  "blog/my-posts-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Author_Post.objects.all().filter(creator=self.request.user.author )
        print(Author_Post.objects.all().filter(creator=self.request.user.author ).count())
        return context


class PostsList(ListView):
    model = Public_Post
    paginate_by = 10
    template_name = 'blog/post_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Public_Post.objects.all()
        print(Public_Post.objects.all().count())
        return context


def post_view(request, slug):
    post = Post.objects.get(slug=slug)
    comments = post.comment_set.filter(active=True)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.save()
                messages.success(request, f"Your comment submitted successfully.")
                return redirect('blog:post', slug=post.slug)
        else:
            messages.error(request, f"Please SignIn to  comment on posts!")
            return redirect("blog:login")

    else:
        form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required(login_url='blog:login')
def create_post_view(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)

        print("validating of form starting")
        if form.is_valid:
            post = form.save(commit=False)
            post.creator = Author.objects.get(name=request.user)
            post.save()
            return redirect('blog:my-posts')
    form = CreatePostForm()
    context = {'form': form}
    return render(request, 'blog/post_form.html', context)


@login_required(login_url='blog:login')
def post_update_view(request,slug):
    try:
        post = Post.objects.get(slug=slug)
    except :
        messages.error(request, "The requested post is not Found.")
        return redirect("blog:posts")
    if post.creator == request.user.author:
        form = CreatePostForm(instance=post)
        context = {"form": form}
        return render(request, 'blog/post_form.html', context)
    else:
        messages.error(request, "You're are not allowed to view the requested page! You can update your Posts.")
        return redirect('blog:my-posts')


@login_required(login_url='blog:login')
def post_delete_view(request,slug):
    post = Post.objects.get(slug=slug)
    if post.creator == request.user.author or request.user.is_superuser:
        if request.method == 'POST':
            post.delete()
            return redirect('blog:my-posts')
        context = {'post':post}
        return render(request, 'blog/post_confirm_delete.html', context)
    else:
        messages.error(request, "You're are not allowed to delete Someone's Post! Here's your posts list.")
        return redirect('blog:my-posts')



class AuthorsList(ListView):
    model = Author
    paginate_by = 6

from django.db.models import Q
def author_view(request, slug):
    author = Author.objects.get(slug=slug)
    post_list = author.post_set.filter(~Q(status='D'),~Q(privacy='Private'))
    recent_posts = post_list.order_by('-published_date')[:5:]
    total_posts = post_list.count()
    context = {'post_list': post_list,
               'author': author,
               'total_posts': total_posts,
               'recent_posts': recent_posts,
               }
    return render(request, 'blog/author_detail.html', context)


@login_required(login_url='blog:login')
def author_update_view(request, slug):
    if slug == request.user.author.slug:
        author = Author.objects.get(slug=slug)
    else:
        messages.error(request, "You're are not allowed to view the requested page! You can update your profile.")
        author = Author.objects.get(slug=request.user.author.slug)

    if request.method == "POST":
        form = form = UpdateAuthorForm(request.POST,request.FILES,instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('blog:user-profile')
        else:
            messages.error(request, "plaease correct the errors")

    form = UpdateAuthorForm(instance=author)
    context = {"form" : form}
    return render(request, 'blog/author_form.html', context)


def contact_mail(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            mail = request.POST.get('email')
            sub = request.POST.get('subject')
            meassage = request.POST.get('body')

            email = EmailMessage(
                'Hello! You got a mail from ' + "mail",
                "Name : " + str(name) + '\n'
                    f"Email : {str(mail)} \n"
                    f"Subject : {str(sub)} \n"
                    f"Meassage : {str(meassage)} \n",
                settings.EMAIL_HOST_USER,  # 'from@example.com',
                ['nagaraj015973@gmail.com', 'love.haters.fully@gmail.com'],  # to@example.com',
            )
            email.send(fail_silently=False)
            form.save()
            return redirect('blog:home')
    else:
        form = ContactUsForm()
    context = { "form": form, }
    return render(request, 'blog/contactus.html', context)