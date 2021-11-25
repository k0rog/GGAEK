from .models import CustomUser
from django import forms


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'registration__input',
                'placeholder': 'Введите пароль',
            }), label='Введите пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'registration__input',
                'placeholder': 'Повторите пароль',
            }), label='Повторите пароль')

    def clean_email(self):
        email = self.cleaned_data['email']

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this email already exists!')

        return email

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 6:
            raise forms.ValidationError('Password is too short!')

        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise forms.ValidationError('Passwords are not the same')

        return password2

    class Meta:
        model = CustomUser
        fields = ['email']
        labels = {
            'email': 'Электронная почта',
        }
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'registration__input',
                'placeholder': 'Введите Email',
            })
        }


class UserAuthorizationForm(forms.ModelForm):
    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'"Login was unsuccessful. Try again. '
                                        f'The user email or password provided is incorrect.')

        user = CustomUser.objects.filter(email=email).first()
        if user and not user.check_password(password):
            raise forms.ValidationError(f'"Login was unsuccessful. Try again. '
                                        f'The user email or password provided is incorrect.')

        return self.cleaned_data

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        help_texts = {
            'username': None,
        }
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'registration__input',
                'id': 'psw',
                'placeholder': 'Введите пароль',
                'name': 'psw'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'registration__input',
                'id': 'email',
                'placeholder': 'Введите Email',
                'name': 'email'
            })
        }
