from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, CrewApplication


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}))
    full_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX'}))
    college_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'IIT Delhi, NIT Kanpur...'}))
    branch = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'CSE, ECE, ME, MBA...'}))
    year = forms.ChoiceField(choices=Profile.YEAR_CHOICES)
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Kanpur, Delhi...'}))
    github_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'placeholder': 'https://github.com/username'}))
    linkedin_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/...'}))
    instagram_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'placeholder': 'https://instagram.com/...'}))
    why_join = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Why do you want to join CampusCrew? (50-200 words)'}),
        label="Why do you want to join CampusCrew?"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Unique username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password (min 8 chars)'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                phone=self.cleaned_data['phone'],
                college_name=self.cleaned_data['college_name'],
                branch=self.cleaned_data['branch'],
                year=self.cleaned_data['year'],
                city=self.cleaned_data['city'],
                github_url=self.cleaned_data.get('github_url'),
                linkedin_url=self.cleaned_data.get('linkedin_url'),
                instagram_url=self.cleaned_data.get('instagram_url'),
                why_join=self.cleaned_data['why_join'],
            )
        return user


class TechnicalApplicationForm(forms.ModelForm):
    class Meta:
        model = CrewApplication
        fields = ['profile_photo', 'whatsapp', 'skills', 'experience', 'why_join',
                  'github_url', 'portfolio_url', 'tech_stack']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Python, Django, React, ML...'}),
            'experience': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Hackathons, projects, internships...'}),
            'why_join': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Why do you want to join the Tech Team?'}),
            'tech_stack': forms.TextInput(attrs={'placeholder': 'e.g. React + Django + PostgreSQL'}),
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
            'portfolio_url': forms.URLInput(attrs={'placeholder': 'https://yourportfolio.com'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX'}),
        }
        labels = {
            'tech_stack': 'Primary Tech Stack',
            'github_url': 'GitHub Profile',
            'portfolio_url': 'Portfolio Website',
        }


class MarketingApplicationForm(forms.ModelForm):
    class Meta:
        model = CrewApplication
        fields = ['profile_photo', 'whatsapp', 'skills', 'experience', 'why_join',
                  'social_media_handles', 'campaign_idea']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Content creation, Canva, Reels, Copywriting...'}),
            'experience': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Events managed, campaigns run, followers count...'}),
            'why_join': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Why do you want to join the Marketing Team?'}),
            'social_media_handles': forms.TextInput(attrs={'placeholder': 'Instagram: @xyz, LinkedIn: xyz...'}),
            'campaign_idea': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Pitch a marketing campaign idea for the college...'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX'}),
        }
        labels = {
            'social_media_handles': 'Social Media Handles',
            'campaign_idea': 'Campaign Idea (Creative pitch)',
        }


class AccommodationApplicationForm(forms.ModelForm):
    class Meta:
        model = CrewApplication
        fields = ['profile_photo', 'whatsapp', 'skills', 'experience', 'why_join',
                  'city_area', 'accommodation_type']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Local knowledge, networking, communication...'}),
            'experience': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Hostel management, PG contacts, housing networks...'}),
            'why_join': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Why do you want to become an Accommodation Partner?'}),
            'city_area': forms.TextInput(attrs={'placeholder': 'e.g. Civil Lines, IIT Campus Area, Kalyanpur...'}),
            'accommodation_type': forms.TextInput(attrs={'placeholder': 'PG, Hostel, Flat, all of above...'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX'}),
        }
        labels = {
            'city_area': 'Area / Locality',
            'accommodation_type': 'Type of Accommodation you can arrange',
        }
