from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('join/', views.team_selection, name='team_selection'),
    path('apply/technical/', views.technical_apply, name='technical_apply'),
    path('apply/marketing/', views.marketing_apply, name='marketing_apply'),
    path('apply/accommodation/', views.accommodation_apply, name='accommodation_apply'),
    path('success/', views.success_page, name='success_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
