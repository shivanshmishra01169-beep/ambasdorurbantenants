from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import CrewApplication


@login_required
def home_view(request):
    try:
        app = CrewApplication.objects.get(user=request.user)
        return redirect('dashboard')
    except CrewApplication.DoesNotExist:
        return redirect('team_selection')
