from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.forms import UserRegistrate


def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrate(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, 'Account created for {}'.format(username))
            return redirect('blog-home')
    else:
        user_form = UserRegistrate()
    return render(request, 'blog/registrate.html', context={'user_form': user_form})