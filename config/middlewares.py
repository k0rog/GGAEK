from django.utils.deprecation import MiddlewareMixin
from users.forms import UserRegistrationForm, UserAuthorizationForm


class FormPasser(MiddlewareMixin):
    def __call__(self, request):
        request.register_form = UserRegistrationForm(request.POST or None)
        request.auth_form = UserAuthorizationForm()
        response = self.get_response(request)

        return response
