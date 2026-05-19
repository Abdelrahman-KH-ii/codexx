from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm, ProfileForm, RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard:switch_role')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        
        # Auto-enroll new user in all published courses
        from courses.models import Course, Enrollment
        published_courses = Course.objects.filter(is_published=True)
        for c in published_courses:
            Enrollment.objects.get_or_create(user=self.object, course=c)
            
        messages.success(self.request, 'Welcome to Nexus AI. Your journey begins now.')
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:switch_role')
        return super().dispatch(request, *args, **kwargs)


class NexusLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class NexusLogoutView(LogoutView):
    next_page = 'home'


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})
