from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import AppUser
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    """Custom logout view that accepts GET requests for cleaner navigation."""
    logout(request)
    return redirect('index')


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = AppUser
    fields = ('first_name', 'last_name', 'email')
    template_name = 'accounts/my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
