import uuid
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    YEAR_CHOICES = [
        ('1', '1st Year'), ('2', '2nd Year'),
        ('3', '3rd Year'), ('4', '4th Year'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    college_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    city = models.CharField(max_length=100)
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    why_join = models.TextField(help_text="Why do you want to join CampusCrew?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"


class CrewApplication(models.Model):
    TEAM_CHOICES = [
        ('technical', 'Tech Team'),
        ('marketing', 'Marketing Team'),
        ('accommodation', 'Accommodation Partner'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='crew_application')
    team = models.CharField(max_length=30, choices=TEAM_CHOICES)

    # Common fields
    profile_photo = models.ImageField(upload_to='crew_photos/')
    whatsapp = models.CharField(max_length=15)
    skills = models.TextField()
    experience = models.TextField(blank=True)
    why_join = models.TextField()

    # Tech team specific
    github_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    tech_stack = models.CharField(max_length=300, blank=True)

    # Marketing team specific
    social_media_handles = models.CharField(max_length=300, blank=True)
    campaign_idea = models.TextField(blank=True)

    # Accommodation partner specific
    city_area = models.CharField(max_length=100, blank=True)
    accommodation_type = models.CharField(max_length=200, blank=True)

    # IDs
    crew_id = models.CharField(max_length=20, unique=True, blank=True)
    referral_code = models.CharField(max_length=20, unique=True, blank=True)
    referral_count = models.PositiveIntegerField(default=0)
    reward_points = models.PositiveIntegerField(default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.crew_id:
            team_prefix = {
                'technical': 'CC-TECH',
                'marketing': 'CC-MKT',
                'accommodation': 'CC-ACC',
            }.get(self.team, 'CC')
            while True:
                code = f"{team_prefix}-{str(uuid.uuid4().int)[:5]}"
                if not CrewApplication.objects.filter(crew_id=code).exists():
                    self.crew_id = code
                    self.referral_code = code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.team} ({self.crew_id})"
