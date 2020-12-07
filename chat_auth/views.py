from django.contrib.auth.views import FormView
from django.conf import settings
from .forms import UserAdminCreationForm


class SignUpView(FormView):
    """
    This class will be used to render and process the sign up process.
    """

    form_class = UserAdminCreationForm
    success_url = settings.LOGIN_URL
    template_name = "chat_auth/signup.html"

    def form_valid(self, form):
        """
        This method will be calling the save method of form and login the user.
        """
        user = form.save()
        return super().form_valid(form)
