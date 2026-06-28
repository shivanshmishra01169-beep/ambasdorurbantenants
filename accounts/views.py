from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TechnicalApplicationForm, MarketingApplicationForm, AccommodationApplicationForm
from .models import CrewApplication, Profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.profile.full_name}! 🎉 You're in CampusCrew now!")
            return redirect('home')
        else:
            messages.error(request, "There are errors in the form, see below.")
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home')
        messages.error(request, "Incorrect username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def team_selection(request):
    # Check if already applied
    existing = CrewApplication.objects.filter(user=request.user).first()
    if existing:
        return redirect('dashboard')
    return render(request, 'accounts/team_selection.html')


@login_required
def technical_apply(request):
    if CrewApplication.objects.filter(user=request.user).exists():
        return redirect('dashboard')
    if request.method == 'POST':
        form = TechnicalApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.team = 'technical'
            app.save()
            return redirect('success_page')
    else:
        form = TechnicalApplicationForm()
    return render(request, 'accounts/apply_form.html', {
        'form': form, 'team': 'technical',
        'team_name': 'Tech Team',
        'team_color': '#6366f1',
        'team_emoji': '💻',
        'description': 'Power CampusCrew with websites, apps, and technical innovation.',
    })


@login_required
def marketing_apply(request):
    if CrewApplication.objects.filter(user=request.user).exists():
        return redirect('dashboard')
    if request.method == 'POST':
        form = MarketingApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.team = 'marketing'
            app.save()
            return redirect('success_page')
    else:
        form = MarketingApplicationForm()
    return render(request, 'accounts/apply_form.html', {
        'form': form, 'team': 'marketing',
        'team_name': 'Marketing Team',
        'team_color': '#f59e0b',
        'team_emoji': '📣',
        'description': 'Grow the brand, run campaigns, and make CampusCrew a household name on campus.',
    })


@login_required
def accommodation_apply(request):
    if CrewApplication.objects.filter(user=request.user).exists():
        return redirect('dashboard')
    if request.method == 'POST':
        form = AccommodationApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.team = 'accommodation'
            app.save()
            return redirect('success_page')
    else:
        form = AccommodationApplicationForm()
    return render(request, 'accounts/apply_form.html', {
        'form': form, 'team': 'accommodation',
        'team_name': 'Accommodation Partner',
        'team_color': '#10b981',
        'team_emoji': '🏠',
        'description': 'Help students settle into the right place and build a real estate network.',
    })


@login_required
def success_page(request):
    app = get_object_or_404(CrewApplication, user=request.user)
    return render(request, 'accounts/success.html', {'app': app})


@login_required
def dashboard(request):
    try:
        app = CrewApplication.objects.get(user=request.user)
    except CrewApplication.DoesNotExist:
        return redirect('team_selection')

    # Get top 3 performers from same college & same team
    college = request.user.profile.college_name
    top_performers = CrewApplication.objects.filter(
        user__profile__college_name=college,
        team=app.team,
        status='approved',
    ).exclude(user=request.user).order_by('-reward_points')[:3]

    # If not enough approved, show all from same college+team sorted by reward_points
    if top_performers.count() < 3:
        top_performers = CrewApplication.objects.filter(
            user__profile__college_name=college,
            team=app.team,
        ).order_by('-reward_points')[:3]

    return render(request, 'accounts/dashboard.html', {
        'app': app,
        'profile': request.user.profile,
        'top_performers': top_performers,
    })
