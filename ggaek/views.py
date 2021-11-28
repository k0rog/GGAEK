from django.shortcuts import render
from users.forms import UserRegistrationForm, UserAuthorizationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect


def index(request):
    if request.method == 'POST':
        if request.POST.get('password2', None):
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('main')

        elif request.POST.get('password', None):
            form = UserAuthorizationForm(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
                if user:
                    login(request, user)

                return redirect(request.path)

    return render(request, 'index.html')
