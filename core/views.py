from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import CharField
from django.http import JsonResponse
from django.db.models.functions import Substr
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post
from .utils import searchProfiles, shorten_caption
import random
from itertools import chain

User=get_user_model()
# Create your views here. 
@login_required(login_url='login')
def index(request):
    user = request.user
    profile= request.user.profile
    
    posts = Post.objects.annotate(short_caption=Substr('caption', 1, 50, output_field=CharField()))
    followers_list = user.followers.all()  
    following_list = user.following.all()

    all_users = User.objects.all()
    user_following_all = []
    for user in followers_list:
        user_list = User.objects.get(username=user.username)
        user_following_all.append(user_list)

    new_suggestion_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username = request.user.username)
    suggestion_list = [x for x in list(new_suggestion_list) if (x not in list(current_user))]
    random.shuffle(suggestion_list)
    username_profile=[]
    username_profile_list=[]

    for users in suggestion_list:
        username_profile.append(users.username)

    for username in username_profile:
        profile_lists= Profile.objects.filter(username = username)
        username_profile_list.append(profile_lists)
        

    suggestion_username_profile_list =  list(chain(*username_profile_list))
    print(suggestion_username_profile_list)
    

    context={
        'profile':profile,
        'posts': posts,
        'suggestions': suggestion_username_profile_list
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

def user_profiles(request):

    profiles, search_query = searchProfiles(request)

    context= {
        'profiles':profiles,
        'search_query':search_query
    }

    return render(request, 'core/profiles.html', context)

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

@login_required
def follow(request, username):
        user = request.user
        profile = get_object_or_404(Profile, username=username)
        if user != profile.user:
           
            user.followers.add(profile.user)
            
            messages.success(request, "Successfully followed user")
            return redirect(reverse('user_profile', kwargs={'username':username}))
        else:
            messages.error(request, 'cannot follow yourself')
        return redirect(reverse('user_profile', kwargs={'username':username}))

@login_required
def unfollow(request, username):
    user = request.user
    profile = get_object_or_404(Profile, username=username)
    user.followers.remove(profile.user)
    messages.success(request, "Successfully unfollowed user")
    return redirect(reverse('user_profile', kwargs={'username':username}))

def userProfile(request, username):
    user = request.user
    
    profile = get_object_or_404(Profile, username=username)
    
    user_post=Post.objects.filter(owner=profile)
    
    user_post_count = user_post.count() 
    followers_list = user.followers.all()  
    following_list = user.following.all()  
    # all_users =  User.objects.all()
    # users_following_list = []
    # for u in followers_list:
    #     user_list=User.objects.get(username= u.username)
    #     users_following_list.append(user_list)

    # new_suggestions= [x for x in list(all_users) if (x not in list(users_following_list))]
    # current_user= User.objects.filter(username=request.user.username)
    # final_suggestion_list = [x for x in list(new_suggestions) if (x not in list(current_user))]
    # print(new_suggestions)

    # check if user is following/follower
    is_following = request.user in followers_list

    
    context={
        'user': user,
        'profile': profile,
        'post_count':user_post_count,
        'followers':followers_list,
        'is_following': is_following,
        'following': following_list,
    }
    return render(request, 'core/user-profile.html', context)



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

     # Get the referring URL
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    # Redirect to the referring URL
    return HttpResponseRedirect(referring_url)

def deletePost(request, pk):
    profile = request.user.profile
    post = profile.post_set.get(id=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post Deleted!')
        return redirect('account')
    context = {
        'object': post
    }
    return render(request, 'core/delete_template.html', context)





 
    
