from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import JobRequirement, Resume, Skill, StudentProfile


class StudentDashboardSyncTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='learner',
            password='secret123',
            role='student',
        )
        self.profile = StudentProfile.objects.create(user=self.user, target_role='Frontend Developer')
        self.requirement = JobRequirement.objects.create(
            title='Frontend Developer',
            description='Frontend stack',
            created_by=self.user,
        )
        self.html = Skill.objects.create(name='HTML')
        self.css = Skill.objects.create(name='CSS')
        self.requirement.required_skills.add(self.html, self.css)
        self.profile.skills.add(self.html)
        self.client.login(username='learner', password='secret123')

    def test_dashboard_report_uses_latest_student_skills(self):
        response = self.client.get(reverse('student_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['readiness_score'], 50)
        self.assertEqual([skill.name for skill in response.context['matched_skills']], ['HTML'])
        self.assertEqual([skill.name for skill in response.context['missing_skills']], ['CSS'])

        self.client.post(reverse('add_skill'), {'name': 'CSS'})
        response = self.client.get(reverse('student_dashboard'))

        self.assertEqual(response.context['readiness_score'], 100)
        self.assertEqual([skill.name for skill in response.context['missing_skills']], [])

    def test_resume_analysis_refreshes_after_skill_change(self):
        resume = Resume.objects.create(
            student=self.profile,
            file='resumes/demo.txt',
            extracted_text='Experienced with HTML and CSS projects.',
            analysis_score=0,
            is_ready=False,
            analysis_summary='',
            improvement_suggestions='',
            matched_skills='',
            missing_skills='',
        )

        self.client.post(reverse('add_skill'), {'name': 'CSS'})
        resume.refresh_from_db()

        self.assertEqual(resume.analysis_score, 100)
        self.assertTrue(resume.is_ready)
        self.assertEqual(set(resume.matched_skills.split(', ')), {'HTML', 'CSS'})
        self.assertEqual(resume.missing_skills, '')
        self.assertIn('Your resume shows evidence', resume.analysis_summary)

    def test_update_skill_replaces_old_skill_and_refreshes_report(self):
        response = self.client.post(reverse('update_skill'), {
            'current_skill': self.html.id,
            'name': 'CSS',
        })

        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.skills.filter(name='HTML').exists())
        self.assertTrue(self.profile.skills.filter(name='CSS').exists())

    def test_dashboard_matches_skills_case_insensitively(self):
        lower_html = Skill.objects.create(name='html')
        lower_css = Skill.objects.create(name='css')
        self.profile.skills.clear()
        self.profile.skills.add(lower_html, lower_css)

        response = self.client.get(reverse('student_dashboard'))

        self.assertEqual(response.context['readiness_score'], 100)
        self.assertEqual({skill.name for skill in response.context['matched_skills']}, {'HTML', 'CSS'})
        self.assertEqual(list(response.context['missing_skills']), [])

    def test_add_skill_reuses_existing_skill_ignoring_case(self):
        self.profile.skills.clear()

        response = self.client.post(reverse('add_skill'), {'name': 'html'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Skill.objects.filter(name__iexact='html').count(), 1)
        self.assertTrue(self.profile.skills.filter(id=self.html.id).exists())

    def test_dashboard_exposes_resume_ai_feedback(self):
        Resume.objects.create(
            student=self.profile,
            file='resumes/demo.txt',
            extracted_text='Experienced with HTML.',
            analysis_score=50,
            is_ready=False,
            analysis_summary='The resume shows some frontend grounding but lacks CSS evidence.',
            improvement_suggestions='Add CSS project bullet points, Quantify project outcomes',
            matched_skills='HTML',
            missing_skills='CSS',
        )

        response = self.client.get(reverse('student_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['resume_suggestions'],
            ['Add CSS project bullet points', 'Quantify project outcomes'],
        )


class AdminDeleteTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_user(
            username='adminuser',
            password='secret123',
            role='admin',
        )
        self.student = get_user_model().objects.create_user(
            username='studentuser',
            password='secret123',
            role='student',
        )
        self.profile = StudentProfile.objects.create(user=self.student, target_role='Backend Developer')
        self.skill = Skill.objects.create(name='Django')
        self.profile.skills.add(self.skill)
        self.requirement = JobRequirement.objects.create(
            title='Backend Developer',
            description='Build APIs',
            created_by=self.admin,
        )
        self.requirement.required_skills.add(self.skill)
        self.group = self.admin.managed_groups.create(
            name='Backend Circle',
            description='Django practice group',
        )
        self.group.skills_required.add(self.skill)
        self.event = self.admin.created_events.create(
            name='API Hackathon',
            group=self.group,
            event_date='2026-04-20',
            description='Build API projects',
        )
        self.client.login(username='adminuser', password='secret123')

    def test_admin_can_delete_job_requirement(self):
        response = self.client.post(reverse('delete_job_requirement', args=[self.requirement.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(JobRequirement.objects.filter(id=self.requirement.id).exists())

    def test_admin_can_delete_group(self):
        response = self.client.post(reverse('delete_group', args=[self.group.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.admin.managed_groups.filter(id=self.group.id).exists())

    def test_admin_can_delete_event(self):
        response = self.client.post(reverse('delete_event', args=[self.event.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.admin.created_events.filter(id=self.event.id).exists())

    def test_admin_can_delete_student(self):
        response = self.client.post(reverse('delete_student', args=[self.student.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(get_user_model().objects.filter(id=self.student.id).exists())
