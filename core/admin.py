from django.contrib import admin

from .models import Event, JobRequirement, Resume, Skill, SkillGroup, StudentProfile, User

admin.site.register(User)
admin.site.register(Skill)
admin.site.register(StudentProfile)
admin.site.register(Resume)
admin.site.register(JobRequirement)
admin.site.register(SkillGroup)
admin.site.register(Event)

# Register your models here.
