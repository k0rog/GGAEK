from django.shortcuts import render
from users.forms import UserRegistrationForm


def index(request):
    if request.method == 'POST':
        if request.POST.get('password2', None):
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()

    form = UserRegistrationForm(request.POST or None)

    return render(request, 'index.html', {'form': form})
