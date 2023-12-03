from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from core.models import Profile
from django.contrib.auth.decorators import login_required
User=get_user_model()

# Create your views here.
@login_required(login_url='login')
def inbox(request):
    
    user = request.user
    profile = request.user.profile

    context={
        'profile': profile,
    }   
    return render(request,  'chatapp/inbox.html', context)