from django.contrib.auth.views import LogoutView


class UserLogoutView(LogoutView):
    def get_next_page(self):
        print(self.request.path)
        return self.request.path
