from django.contrib import admin
from .models import Profile, CrewApplication

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'college_name', 'branch', 'year', 'city']
    search_fields = ['full_name', 'college_name']

@admin.register(CrewApplication)
class CrewApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'crew_id', 'referral_code', 'reward_points', 'status']
    list_editable = ['status', 'reward_points']
    search_fields = ['user__username', 'crew_id']
    list_filter = ['team', 'status']
