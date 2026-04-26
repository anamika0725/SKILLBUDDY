from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Event, JobRequirement, Resume, Skill, SkillGroup, StudentProfile, User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    email = forms.EmailField()
    organization = forms.CharField(required=False)
    target_role = forms.CharField(required=False)
    skills = forms.CharField(required=False, help_text='Comma separated skills')

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'role', 'organization', 'target_role', 'skills', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.organization = self.cleaned_data['organization']

        if commit:
            user.save()
            if user.role == 'student':
                profile, _ = StudentProfile.objects.get_or_create(user=user)
                profile.target_role = self.cleaned_data['target_role']
                profile.save()
                for skill_name in self.cleaned_data['skills'].split(','):
                    name = skill_name.strip()
                    if name:
                        skill = Skill.objects.filter(name__iexact=name).first()
                        if not skill:
                            skill = Skill.objects.create(name=name)
                        profile.skills.add(skill)
        return user


class AddSkillForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Add a skill like React or SQL'}))


class UpdateSkillForm(forms.Form):
    current_skill = forms.ModelChoiceField(queryset=Skill.objects.none(), empty_label='Select a current skill')
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Replace with a new skill'}))

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)
        if profile:
            self.fields['current_skill'].queryset = profile.skills.all()


class JobRequirementForm(forms.ModelForm):
    required_skills = forms.CharField(help_text='Comma separated skills', widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'HTML, CSS, JavaScript'}))

    class Meta:
        model = JobRequirement
        fields = ('title', 'description', 'required_skills')


class GroupForm(forms.ModelForm):
    skills_required = forms.CharField(help_text='Comma separated skills', widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Python, Django, SQL'}))

    class Meta:
        model = SkillGroup
        fields = ('name', 'description', 'skills_required')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'group', 'event_date', 'description')
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('file',)


class DeleteAccountForm(forms.Form):
    confirm = forms.BooleanField(label='I understand this will permanently delete my account and related data')
