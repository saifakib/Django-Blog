from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Author, Category, Article, Comment
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import CreateArticle, RegistationForm, CommentForm
from django.contrib import messages
# Create your views here.
def index(request):
    post = Article.objects.all().order_by('-posted_on')
    paginator = Paginator(post, 4)              # Show 04 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    search = request.GET.get('q')
    if search:
        post = post.filter(
            Q(title__icontains=search)|
            Q(body__icontains=search)

        )
    context={
        "post":total_article
    }
    return render(request, "index.html", context)

def getauthor(request, name):
    post_author = get_object_or_404(User, username=name)                           # here we find User name : ex/ saif
    auth = get_object_or_404(Author, name=post_author.id)                          # here we find saif.id all information
    post = Article.objects.filter(article_author=auth.id).order_by('-posted_on')   # here we find all post from saif
    paginator = Paginator(post, 4)                                               # Show 25 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context={
        "auth":auth,
        "post":total_article
    }
    return render(request, "profile.html", context)

def getsingle(request, id):
    post = get_object_or_404(Article, pk=id)
    #getComment = Comment.objects.filter(post.id)
    first = Article.objects.first()
    last = Article.objects.last()
    related = Article.objects.filter(category=post.category).exclude(id=id)[:4]


    context={
        "post":post,
        "first":first,
        "last":last,
        "related":related,


    }
    return render(request, "single.html", context)

def getTopic(request, name):
    cat = get_object_or_404(Category, name=name)
    post = Article.objects.filter(category=cat.id).order_by('-posted_on')
    paginator = Paginator(post, 4)      # Show 25 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    return render(request, "category.html",{"post":total_article, "cat":cat})


def getLogin(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, ' Login Successfuly')
            #messages.success(request, 'Login')
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Username & password dont mismatch ')
            #messages.error(request, 'Username & password mismatch')
    return render(request,'login.html')

def getLogout(request):
    logout(request)
    return redirect('/')


def getCreate(request):
   if request.user.is_authenticated:
       creator = get_object_or_404(Author, name=request.user.id)  #creator from name of Author class thats have request.user.id means this moment login user id
       form = CreateArticle(request.POST or None, request.FILES or None)
       if form.is_valid():
           isinstance = form.save(commit=False)
           isinstance.article_author = creator              # login user id pass to article_author of Article Class
           isinstance.save()
           messages.add_message(request, messages.SUCCESS,'Article created')
           #messages.success(request, 'Article created')
           return redirect('/profile')
       else:
           messages.warning(request, 'Article Not Deleted')
       return render(request, 'create.html',{'form':form})
   else:
       return redirect('/login')

def getProfile(request):
    if request.user.is_authenticated:
        author = get_object_or_404(Author, name=request.user.id)
        posts = Article.objects.filter(article_author=request.user.id)
        return render(request, 'logged_in_profile.html',{'posts':posts,'author':author})
    else:
        return redirect('login')

def getUpdate(request, pid):
    if request.user.is_authenticated:
        creator = get_object_or_404(Author, name=request.user.id)
        post = get_object_or_404(Article, id=pid)
        form = CreateArticle(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            isinstance = form.save(commit=False)
            isinstance.article_author = creator              # login user id pass to article_author of Article Class
            isinstance.save()
            messages.success(request, 'Article updated.')
            return redirect('/profile')
        return render(request, 'create.html',{'form':form})
    else:
        return redirect('/login')

def getDelete(request, pid):
    if request.user.is_authenticated:
        post = get_object_or_404(Article, id=pid)
        post.delete()
        return redirect('/profile')

def getRegister(request):
    if request.method == 'POST':
        form = RegistationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegistationForm()
    return render(request,'registation.html',{'form':form})