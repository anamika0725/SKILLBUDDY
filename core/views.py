from pathlib import Path

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from pypdf import PdfReader

from .ai_resume import analyze_resume_with_gemini
from .forms import AddSkillForm, DeleteAccountForm, EventForm, GroupForm, JobRequirementForm, LoginForm, RegisterForm, ResumeUploadForm, UpdateSkillForm
from .models import Event, JobRequirement, Resume, Skill, SkillGroup, StudentProfile, User


def home(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')

    return render(request, 'core/login.html', {'form': form})


def register_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')

    return render(request, 'core/register.html', {'form': form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('home')


@login_required
def dashboard_router(request: HttpRequest) -> HttpResponse:
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('student_dashboard')


@login_required
def student_dashboard(request: HttpRequest) -> HttpResponse:
    if request.user.role != 'student':
        return redirect('admin_dashboard')

    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    skill_form = AddSkillForm()
    update_skill_form = UpdateSkillForm(profile=profile)
    resume_form = ResumeUploadForm()
    delete_account_form = DeleteAccountForm()
    target_requirement = _get_target_requirement(profile)
    report = _build_skill_gap_report(profile, target_requirement)
    _refresh_resume_analysis(profile, target_requirement)

    groups = SkillGroup.objects.prefetch_related('skills_required', 'members')
    events = Event.objects.select_related('group').prefetch_related('participants')

    context = {
        'profile': profile,
        'skill_form': skill_form,
        'update_skill_form': update_skill_form,
        'resume_form': resume_form,
        'delete_account_form': delete_account_form,
        'student_skills': report['student_skills'],
        'matched_skills': report['matched_skills'],
        'missing_skills': report['missing_skills'],
        'readiness_score': report['readiness_score'],
        'target_requirement': target_requirement,
        'resume': getattr(profile, 'resume', None),
        'resume_suggestions': _csv_to_list(getattr(getattr(profile, 'resume', None), 'improvement_suggestions', '')),
        'resume_matched_skills': _csv_to_list(getattr(getattr(profile, 'resume', None), 'matched_skills', '')),
        'resume_missing_skills': _csv_to_list(getattr(getattr(profile, 'resume', None), 'missing_skills', '')),
        'groups': groups,
        'events': events,
    }
    return render(request, 'core/student_dashboard.html', context)


@login_required
def admin_dashboard(request: HttpRequest) -> HttpResponse:
    if request.user.role != 'admin':
        return redirect('student_dashboard')

    students = User.objects.filter(role='student').select_related('student_profile')
    for student in students:
        StudentProfile.objects.get_or_create(user=student)

    context = {
        'students': students,
        'groups': SkillGroup.objects.prefetch_related('skills_required'),
        'events': Event.objects.select_related('group'),
        'requirements': JobRequirement.objects.prefetch_related('required_skills'),
        'role_form': JobRequirementForm(),
        'group_form': GroupForm(),
        'event_form': EventForm(),
        'student_count': students.count(),
        'group_count': SkillGroup.objects.count(),
        'event_count': Event.objects.count(),
        'delete_account_form': DeleteAccountForm(),
    }
    return render(request, 'core/admin_dashboard.html', context)


@login_required
def add_skill(request: HttpRequest) -> HttpResponse:
    if request.user.role != 'student' or request.method != 'POST':
        return redirect('dashboard')

    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    form = AddSkillForm(request.POST)
    if form.is_valid():
        skill = _resolve_skill(form.cleaned_data['name'])
        profile.skills.add(skill)
        _refresh_resume_analysis(profile)
        messages.success(request, 'Skill added successfully.')
    return redirect('student_dashboard')


@login_required
def upload_resume(request: HttpRequest) -> HttpResponse:
    if request.user.role != 'student' or request.method != 'POST':
        return redirect('dashboard')

    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    form = ResumeUploadForm(request.POST, request.FILES, instance=getattr(profile, 'resume', None))
    if form.is_valid():
        resume = form.save(commit=False)
        resume.student = profile
        resume.save()

        extracted_text = _extract_resume_text(resume.file.path)
        requirement = JobRequirement.objects.filter(title__iexact=profile.target_role).prefetch_related('required_skills').first()
        matched_names, missing_names, score = _analyze_resume_text(extracted_text, requirement)
        ai_result = _analyze_resume_with_ai(extracted_text, requirement) if requirement else None

        resume.extracted_text = extracted_text[:20000]
        resume.analysis_score = score
        resume.is_ready = score >= 70
        resume.analysis_summary = _build_resume_summary(requirement, matched_names, missing_names, ai_result)
        resume.improvement_suggestions = ', '.join(_build_resume_suggestions(missing_names, ai_result))
        resume.matched_skills = ', '.join(matched_names)
        resume.missing_skills = ', '.join(missing_names)
        resume.save(update_fields=['extracted_text', 'analysis_score', 'is_ready', 'analysis_summary', 'improvement_suggestions', 'matched_skills', 'missing_skills', 'uploaded_at'])

        messages.success(request, 'Resume uploaded and analyzed successfully.')
    else:
        messages.error(request, 'Please upload a valid PDF or TXT resume.')
    return redirect('student_dashboard')


@login_required
def remove_skill(request: HttpRequest, skill_id: int) -> HttpResponse:
    if request.user.role != 'student' or request.method != 'POST':
        return redirect('dashboard')

    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    skill = get_object_or_404(Skill, id=skill_id)
    profile.skills.remove(skill)
    _refresh_resume_analysis(profile)
    messages.success(request, 'Skill removed.')
    return redirect('student_dashboard')


@login_required
def update_skill(request: HttpRequest) -> HttpResponse:
    if request.user.role != 'student' or request.method != 'POST':
        return redirect('dashboard')

    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    form = UpdateSkillForm(request.POST, profile=profile)
    if form.is_valid():
        current_skill = form.cleaned_data['current_skill']
        replacement_name = form.cleaned_data['name'].strip()
        replacement_skill = _resolve_skill(replacement_name)
        profile.skills.remove(current_skill)
        profile.skills.add(replacement_skill)
        _refresh_resume_analysis(profile)
        messages.success(request, 'Skill updated successfully.')
    else:
        messages.error(request, 'Please choose a skill to replace and enter the updated name.')
    return redirect('student_dashboard')


@login_required
def toggle_group_membership(request: HttpRequest, group_id: int) -> HttpResponse:
    if request.user.role != 'student' or request.method != 'POST':
        return redirect('dashboard')

    group = get_object_or_404(SkillGroup, id=group_id)
    if group.members.filter(id=request.user.id).exists():
        group.members.remove(request.user)
        messages.success(request, 'You left the group.')
    else:
        group.members.add(request.user)
        messages.success(request, 'You joined the group.')
    return redirect('student_dashboard')


@login_required
def toggle_event_registration(request: HttpRequest, event_id: int) -> HttpResponse:
    if request.user.role != 'student' or request.method != 'POST':
        return redirect('dashboard')

    event = get_object_or_404(Event, id=event_id)
    if event.participants.filter(id=request.user.id).exists():
        event.participants.remove(request.user)
        messages.success(request, 'Event registration removed.')
    else:
        event.participants.add(request.user)
        messages.success(request, 'Event registered successfully.')
    return redirect('student_dashboard')


@login_required
def create_job_requirement(request: HttpRequest) -> HttpResponse:
    if request.user.role != 'admin' or request.method != 'POST':
        return redirect('dashboard')

    form = JobRequirementForm(request.POST)
    if form.is_valid():
        requirement = form.save(commit=False)
        requirement.created_by = request.user
        requirement.save()
        _attach_skills(requirement.required_skills, form.cleaned_data['required_skills'])
        messages.success(request, 'Job requirement created.')
    else:
        messages.error(request, 'Please correct the job requirement form.')
    return redirect('admin_dashboard')


@login_required
def delete_job_requirement(request: HttpRequest, requirement_id: int) -> HttpResponse:
    if request.user.role != 'admin' or request.method != 'POST':
        return redirect('dashboard')

    requirement = get_object_or_404(JobRequirement, id=requirement_id)
    requirement.delete()
    messages.success(request, 'Job requirement deleted successfully.')
    return redirect('admin_dashboard')


@login_required
def create_group(request: HttpRequest) -> HttpResponse:
    if request.user.role != 'admin' or request.method != 'POST':
        return redirect('dashboard')

    form = GroupForm(request.POST)
    if form.is_valid():
        group = form.save(commit=False)
        group.created_by = request.user
        group.save()
        _attach_skills(group.skills_required, form.cleaned_data['skills_required'])
        messages.success(request, 'Group created successfully.')
    else:
        messages.error(request, 'Please correct the group form.')
    return redirect('admin_dashboard')


@login_required
def delete_group(request: HttpRequest, group_id: int) -> HttpResponse:
    if request.user.role != 'admin' or request.method != 'POST':
        return redirect('dashboard')

    group = get_object_or_404(SkillGroup, id=group_id)
    group.delete()
    messages.success(request, 'Group deleted successfully.')
    return redirect('admin_dashboard')


@login_required
def create_event(request: HttpRequest) -> HttpResponse:
    if request.user.role != 'admin' or request.method != 'POST':
        return redirect('dashboard')

    form = EventForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.created_by = request.user
        event.save()
        messages.success(request, 'Event published successfully.')
    else:
        messages.error(request, 'Please correct the event form.')
    return redirect('admin_dashboard')


@login_required
def delete_event(request: HttpRequest, event_id: int) -> HttpResponse:
    if request.user.role != 'admin' or request.method != 'POST':
        return redirect('dashboard')

    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, 'Event deleted successfully.')
    return redirect('admin_dashboard')


@login_required
def delete_student(request: HttpRequest, student_id: int) -> HttpResponse:
    if request.user.role != 'admin' or request.method != 'POST':
        return redirect('dashboard')

    student = get_object_or_404(User, id=student_id, role='student')
    student.delete()
    messages.success(request, 'Student deleted successfully.')
    return redirect('admin_dashboard')


@login_required
def delete_account(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return redirect('dashboard')

    form = DeleteAccountForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Please confirm account deletion first.')
        return redirect('dashboard')

    user = request.user
    logout(request)
    user.delete()
    messages.success(request, 'Your account has been deleted successfully.')
    return redirect('home')


def _attach_skills(manager, raw_skills: str) -> None:
    names = [item.strip() for item in raw_skills.split(',') if item.strip()]
    for name in names:
        skill = _resolve_skill(name)
        manager.add(skill)


def _get_target_requirement(profile: StudentProfile) -> JobRequirement | None:
    requirements = JobRequirement.objects.prefetch_related('required_skills')
    if profile.target_role:
        target_requirement = requirements.filter(title__iexact=profile.target_role).first()
        if target_requirement:
            return target_requirement
    return requirements.first()


def _build_skill_gap_report(profile: StudentProfile, requirement: JobRequirement | None = None) -> dict[str, object]:
    requirement = requirement or _get_target_requirement(profile)
    student_skills = list(profile.skills.all())
    student_skill_names = {_normalize_skill_name(skill.name) for skill in student_skills}
    required_skills = list(requirement.required_skills.all()) if requirement else []
    matched_skills = [skill for skill in required_skills if _normalize_skill_name(skill.name) in student_skill_names]
    missing_skills = [skill for skill in required_skills if _normalize_skill_name(skill.name) not in student_skill_names]
    readiness_score = round((len(matched_skills) / len(required_skills)) * 100) if required_skills else 0
    return {
        'student_skills': student_skills,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'readiness_score': readiness_score,
    }


def _extract_resume_text(file_path: str) -> str:
    suffix = Path(file_path).suffix.lower()
    if suffix == '.pdf':
        reader = PdfReader(file_path)
        parts = [(page.extract_text() or '') for page in reader.pages]
        return '\n'.join(parts)
    if suffix == '.txt':
        return Path(file_path).read_text(encoding='utf-8', errors='ignore')
    return ''


def _analyze_resume_text(text: str, requirement: JobRequirement | None) -> tuple[list[str], list[str], int]:
    if not requirement:
        return [], [], 0

    ai_result = _analyze_resume_with_ai(text, requirement)
    if ai_result:
        return ai_result['matched_skills'], ai_result['missing_skills'], ai_result['score']

    text_lower = text.lower()
    required_names = [skill.name for skill in requirement.required_skills.all()]
    matched = [name for name in required_names if name.lower() in text_lower]
    missing = [name for name in required_names if name.lower() not in text_lower]
    score = round((len(matched) / len(required_names)) * 100) if required_names else 0
    return matched, missing, score


def _analyze_resume_with_ai(text: str, requirement: JobRequirement) -> dict[str, object] | None:
    required_names = [skill.name for skill in requirement.required_skills.all()]
    try:
        return analyze_resume_with_gemini(text, requirement.title, required_names)
    except Exception:
        return None


def _build_resume_summary(requirement: JobRequirement | None, matched_names: list[str], missing_names: list[str], ai_result: dict[str, object] | None = None) -> str:
    if ai_result and ai_result.get('summary'):
        return str(ai_result['summary'])
    if not requirement:
        return 'Upload a resume after selecting a target role to get a tailored review.'
    if matched_names:
        return f"Your resume shows evidence for {len(matched_names)} required skill(s) for the {requirement.title} role."
    return f"Your resume needs stronger evidence for the {requirement.title} role."


def _build_resume_suggestions(missing_names: list[str], ai_result: dict[str, object] | None = None) -> list[str]:
    if ai_result and ai_result.get('improvement_suggestions'):
        return [str(item) for item in ai_result['improvement_suggestions']]
    if missing_names:
        return [f"Add project or experience evidence for {name}." for name in missing_names[:4]]
    return ['Keep improving your projects and add measurable outcomes to strengthen the resume.']


def _csv_to_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(',') if item.strip()]


def _normalize_skill_name(value: str) -> str:
    return ' '.join(value.split()).strip().lower()


def _resolve_skill(name: str) -> Skill:
    cleaned_name = ' '.join(name.split()).strip()
    existing_skill = Skill.objects.filter(name__iexact=cleaned_name).first()
    if existing_skill:
        return existing_skill
    return Skill.objects.create(name=cleaned_name)


def _refresh_resume_analysis(profile: StudentProfile, requirement: JobRequirement | None = None) -> None:
    resume = getattr(profile, 'resume', None)
    if not resume:
        return

    requirement = requirement or _get_target_requirement(profile)
    matched_names, missing_names, score = _analyze_resume_text(resume.extracted_text, requirement)
    ai_result = _analyze_resume_with_ai(resume.extracted_text, requirement) if requirement else None
    updated_values = {
        'analysis_score': score,
        'is_ready': score >= 70,
        'analysis_summary': _build_resume_summary(requirement, matched_names, missing_names, ai_result)
        if ai_result or not resume.analysis_summary else resume.analysis_summary,
        'improvement_suggestions': ', '.join(_build_resume_suggestions(missing_names, ai_result))
        if ai_result or not resume.improvement_suggestions else resume.improvement_suggestions,
        'matched_skills': ', '.join(matched_names),
        'missing_skills': ', '.join(missing_names),
    }
    changed_fields = [field for field, value in updated_values.items() if getattr(resume, field) != value]
    if not changed_fields:
        return

    for field, value in updated_values.items():
        setattr(resume, field, value)
    resume.save(update_fields=changed_fields)
