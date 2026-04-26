from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    organization = models.CharField(max_length=255, blank=True)


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    target_role = models.CharField(max_length=150, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='students')

    def __str__(self):
        return f"{self.user.username} profile"


class JobRequirement(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_requirements')
    required_skills = models.ManyToManyField(Skill, blank=True, related_name='job_requirements')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class SkillGroup(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='managed_groups')
    skills_required = models.ManyToManyField(Skill, blank=True, related_name='skill_groups')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='joined_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=150)
    group = models.ForeignKey(SkillGroup, on_delete=models.CASCADE, related_name='events')
    event_date = models.DateField()
    description = models.TextField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='registered_events')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date', 'name']

    def __str__(self):
        return self.name


class Resume(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='resume')
    file = models.FileField(upload_to='resumes/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'txt'])])
    extracted_text = models.TextField(blank=True)
    analysis_score = models.PositiveIntegerField(default=0)
    is_ready = models.BooleanField(default=False)
    analysis_summary = models.TextField(blank=True)
    improvement_suggestions = models.TextField(blank=True)
    matched_skills = models.TextField(blank=True)
    missing_skills = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.username} resume"
