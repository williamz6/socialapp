from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import CharField
from django.db.models.functions import Substr
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Follow
from .utils import shorten_caption

User=get_user_model()
# Create your views here. 
@login_required(login_url='login')
def index(request):
    profile= request.user.profile
    
    posts = Post.objects.annotate(short_caption=Substr('caption', 1, 50, output_field=CharField()))
    

    context={
        'profile':profile,
        'posts': posts
    }
    # will have random posts
    return render(request,'core/index.html', context)

def signup(request):
    form = RegisterForm()

    if request.method == 'POST':
        form= RegisterForm(request.POST)

        if form.is_valid():
            user= form.save()
            user.save()
            messages.success(request, "user account was created!")
            login(request, user)
            return redirect('account')
        else:
            messages.error(request,"An error occured during registration" )
    context={
        'form': form
    }
    return render(request, 'core/signup.html', context)

def signin(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        email = request.POST['email'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            messages.error(request, f"Sorry {email} does not exist")
  
        
        user= authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('index')

        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'core/signin.html')

def signout(request):
    logout(request)
    messages.info(request, "User was logout")
    return redirect('login')

@login_required(login_url='login')
def userAccount(request):
    profile= request.user.profile

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            profile.profileimg = image
            profile.bio = bio
            profile.location = location
            profile.save()
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            profile.profileimg = image
            profile.bio = bio
            profile.location = location
            profile.save()
        return redirect('account')

    context={
        'profile': profile,
    }
    return render(request, 'core/account.html', context)

def userProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    
    user_post=Post.objects.filter(owner=profile)

    user_post_count = user_post.count()
    followers = request.user.following


    
    context={
        'user': user,
        'profile': profile,
        'post_count':user_post_count,
        'followers':followers,
    }
    return render(request, 'core/user-profile.html', context)

def follow(request, username):

    user = get_object_or_404(User, username=username)
    if request.user == user:
        return redirect('user_profile', username=username)
    follow,created = Follow.objects.get_or_create(follower=request.user, followed=user)
    if created:
        follow.save()
    return redirect('user_profile', username=username)

def unfollow(request, username):
    user = get_object_or_404(User, username=username)
    follow = get_object_or_404(Follow, follower=request.user, followed=user)
    follow.delete()
    return redirect('profile', username=username)

@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        user = request.user.profile
        photo = request.FILES.get('image_upload')
        caption= request.POST['post_comment']

        new_post= Post.objects.create(owner=user, photo=photo, caption=caption)
        new_post.save()
        return redirect('index')
    else:
        return redirect('index')

def likePost(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('index'))   
    
