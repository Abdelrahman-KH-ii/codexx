from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Profile

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'glass-input',
            'placeholder': 'you@email.com',
            'autocomplete': 'email',
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'glass-input',
            'placeholder': 'username',
            'autocomplete': 'username',
        })
    )
    role = forms.ChoiceField(
        choices=[
            ('student', 'Student / طالب العلم'),
            ('instructor', 'Instructor / معلم المساق'),
        ],
        widget=forms.Select(attrs={
            'class': 'glass-input',
            'style': 'background: #1c1b1c; color: #fff; border: none; border-bottom: 2px solid var(--outline-variant); padding: 0.75rem 1rem; width: 100%; font-family: inherit; font-size: 0.95rem;'
        }),
        initial='student',
        label="Register as / التسجيل كـ"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'glass-input',
            'placeholder': '••••••••',
            'autocomplete': 'new-password',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'glass-input',
            'placeholder': '••••••••',
            'autocomplete': 'new-password',
        })
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Save role to user profile
            profile = user.profile
            profile.role = self.cleaned_data['role']
            profile.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_name = 'username'
        self.fields[field_name].label = 'Email'
        self.fields[field_name].widget = forms.EmailInput(attrs={
            'class': 'glass-input',
            'placeholder': 'you@email.com',
            'autocomplete': 'email',
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'glass-input',
            'placeholder': '••••••••',
            'autocomplete': 'current-password',
        })


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar', 'github_url')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'glass-input', 'rows': 4}),
            'github_url': forms.URLInput(attrs={'class': 'glass-input'}),
        }
