from django.utils.deprecation import MiddlewareMixin
from users.forms import UserRegistrationForm, UserAuthorizationForm


class FormPasser(MiddlewareMixin):
    def __call__(self, request):
        if request.POST.get('password2', None):
            request.register_form = UserRegistrationForm(request.POST or None)
            request.auth_form = UserAuthorizationForm()
        else:
            request.register_form = UserRegistrationForm()
            request.auth_form = UserAuthorizationForm(request.POST or None)
        response = self.get_response(request)

        return response
