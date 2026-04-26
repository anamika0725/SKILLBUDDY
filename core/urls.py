from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_router, name='dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('account/delete/', views.delete_account, name='delete_account'),
    path('skills/add/', views.add_skill, name='add_skill'),
    path('skills/update/', views.update_skill, name='update_skill'),
    path('skills/<int:skill_id>/remove/', views.remove_skill, name='remove_skill'),
    path('resume/upload/', views.upload_resume, name='upload_resume'),
    path('groups/<int:group_id>/toggle/', views.toggle_group_membership, name='toggle_group_membership'),
    path('events/<int:event_id>/toggle/', views.toggle_event_registration, name='toggle_event_registration'),
    path('job-requirements/create/', views.create_job_requirement, name='create_job_requirement'),
    path('job-requirements/<int:requirement_id>/delete/', views.delete_job_requirement, name='delete_job_requirement'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('students/<int:student_id>/delete/', views.delete_student, name='delete_student'),
]
