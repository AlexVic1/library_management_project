from django.shortcuts import redirect, render
from .forms import LoginForm
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('list_menu'))
            else:
                messages.error(request,'Invalid credentials')
                form = LoginForm()
                context={'form':form}
                html_template = loader.get_template('login.html')
                return HttpResponse(html_template.render(context, request))
        else:
            messages.error(request,'Form validation error')
    else:
        form = LoginForm()
        context={'form':form}
        html_template = loader.get_template('login.html')
        return HttpResponse(html_template.render(context, request))

def logout_view(request):
    logout(request)
    return redirect('login')

