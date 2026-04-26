# SkillBuddy Project Report
Prepared in a formal submission style based on the attached sample document.

Project Title: SkillBuddy - Skill Gap Analyzer and Student Opportunity Platform
Project Type: Full-stack web application
Technology Base: Django, SQLite, HTML templates, CSS, Python
Prepared On: 13 April 2026
Prepared For: Project report submission

## 1. INTRODUCTION
SkillBuddy is a web-based academic and career readiness platform designed to help students understand the gap between their current skills and the requirements of their target job roles. The system combines skill tracking, job requirement mapping, resume analysis, collaboration groups, and event participation within a single application.

The current implementation is built as a real Django application with database-backed storage and role-based dashboards for both students and administrators. Instead of using static pages or mock data, the project stores users, skills, job requirements, groups, events, and resumes inside a SQLite database. This makes the system suitable for demonstration, academic evaluation, and future production-oriented extension.

The project solves a common problem in student development: learners often know that they want a role such as Frontend Developer, Python Developer, or Data Analyst, but they do not have a clear way to measure how ready they are. SkillBuddy provides a visible readiness score, matched skills, missing skills, and resume-based feedback so that students can make practical decisions about what to learn next.

The platform also improves communication between administrators and students. Administrators can define job requirements, create skill-based groups, publish events or hackathons, and monitor the progress of registered students. Students can then update their skills, join groups, participate in events, and upload resumes to evaluate their preparedness.

## 2. PROBLEM DEFINITION
Students frequently face difficulty in identifying whether their current skill set is sufficient for a chosen career path. In many educational environments, students learn technologies in isolation but do not receive a structured comparison against industry expectations. As a result, they may spend time learning random topics without understanding which skills are required, which skills are already strong, and which gaps are preventing them from becoming job-ready.

Another major challenge is the absence of a unified student progress platform. Existing tools often separate learning plans, resumes, events, and community engagement into different systems. This fragmentation makes it difficult for students to track growth and equally difficult for mentors or administrators to guide them.

The SkillBuddy project addresses this gap by creating a centralized platform where:
- students maintain a live skill profile,
- administrators define target-role skill requirements,
- the system computes skill-gap reports,
- resumes are analyzed against target roles,
- collaboration groups are created around skill domains,
- events and hackathons are published for practice and exposure.

## 3. MOTIVATION
The motivation behind SkillBuddy comes from the growing need to align academic learning with employability. Many students complete coursework but remain uncertain about whether they are ready for internships, placements, or real project work. A project like SkillBuddy helps convert vague learning progress into measurable outcomes.

The platform is also motivated by the idea that learning should not remain passive. Students need a system that not only shows missing skills but also encourages action through peer groups, events, and resume refinement. By combining these functions in one place, the project supports continuous improvement instead of one-time assessment.

From an educational point of view, the project demonstrates the use of full-stack web development concepts such as authentication, relational data modeling, role-based dashboards, file uploads, text extraction, and dynamic recommendation logic. This makes SkillBuddy both a useful product concept and a strong academic project.

## 4. OBJECTIVE
The main objective of SkillBuddy is to create a platform that helps students evaluate and improve their readiness for selected job roles through measurable skill-gap analysis and practical engagement features.

The major objectives are:
- to provide secure student and admin registration with authentication,
- to maintain a database-backed profile of student skills,
- to compare student skills with job requirements and compute readiness,
- to generate matched-skill and missing-skill insights,
- to analyze uploaded resumes against a selected target role,
- to allow administrators to create job requirements, groups, and events,
- to encourage learning through group participation and event registration,
- to present all of this in a clean, responsive, submission-ready web interface.

## 5. REQUIREMENT ANALYSIS
### 5.1 Software Requirements
The current project uses the following software stack and development tools:
- Programming Language: Python 3
- Backend Framework: Django 6.0.3
- Database: SQLite3
- Frontend Rendering: Django Templates with HTML
- Styling: Custom CSS
- Resume Text Extraction: pypdf
- Development Environment: VS Code or any Python-supported editor
- Version Control: Git/GitHub compatible workflow
- Browser Support: Modern desktop browsers such as Chrome, Edge, and Firefox

Core Django modules actively used in the project include:
- authentication and authorization,
- forms,
- ORM-based database operations,
- templates,
- messages framework,
- static and media file handling.

### 5.2 Hardware Requirements
Minimum hardware requirements:
- Processor: Intel Core i3 or equivalent
- RAM: 4 GB
- Storage: 2 GB free space for codebase, Python environment, and database
- Display: 1280 x 720 resolution
- Internet: optional for local development, required for package installation or deployment

Recommended hardware requirements:
- Processor: Intel Core i5 / AMD Ryzen 5 or above
- RAM: 8 GB or above
- Storage: SSD with at least 10 GB free space
- Display: 1920 x 1080 resolution
- Internet: broadband connection for deployment, documentation, and package management

## 6. SYSTEM ARCHITECTURE AND DATA FLOW
SkillBuddy follows a classic Django MVC-like architecture pattern in which models represent the database layer, views process application logic, forms handle validated input, and templates render the user interface.

### 6.1 High-Level Modules
- Authentication Module
- Student Dashboard Module
- Admin Dashboard Module
- Skill Management Module
- Skill Gap Report Module
- Resume Upload and Analysis Module
- Group Management Module
- Event and Hackathon Module
- Account Management Module

### 6.2 Main Actors
- Student
- Admin
- Django Application Server
- SQLite Database
- File Storage for resumes

### 6.3 Data Flow Summary
1. A user registers as either a student or an admin.
2. Django stores user credentials and role information in the database.
3. A student adds or updates skills in the profile section.
4. The system fetches the target job requirement and compares it with saved student skills.
5. The application computes matched skills, missing skills, and readiness percentage.
6. If a resume is uploaded, text is extracted and compared against required skills for the target role.
7. The dashboard displays resume strengths, missing resume skills, and readiness status.
8. Admins create job requirements, groups, and events that become visible to students.
9. Students join groups and register for events to strengthen practical readiness.

### 6.4 Database Design Summary
The current database entities are:
- User: custom Django user with role and organization fields
- Skill: unique skill records used across the application
- StudentProfile: target role and many-to-many student skills
- JobRequirement: role title, description, and required skills
- SkillGroup: collaboration group with skills_required and members
- Event: event details linked to a group with participants
- Resume: uploaded file, extracted text, analysis score, readiness state, matched skills, missing skills

## 7. DEVELOPMENT AND TESTING
### 7.1 Development Approach
The project has been developed as a modular Django application. The implementation is separated into:
- `core/models.py` for data design,
- `core/forms.py` for user input handling,
- `core/views.py` for business logic,
- `core/urls.py` for route definitions,
- `templates/core/` for page rendering,
- `assets/css/main.css` for the shared interface theme.

The development approach appears iterative. Initially the platform supported core student/admin workflows, and it was later enhanced with:
- live skill gap reporting,
- synchronized resume analysis,
- skill update support,
- case-insensitive skill matching,
- refreshed pastel UI themes.

### 7.2 Testing Status
The present codebase includes automated Django test cases for:
- dashboard report updates after student skill changes,
- resume analysis refresh after skill updates,
- skill replacement flow,
- case-insensitive skill matching,
- prevention of duplicate skill records due to case differences.

At the time of report preparation, the automated test suite passes successfully for the `core` application. Manual verification is still important for:
- authentication forms,
- admin dashboard workflows,
- responsive layout behavior,
- resume upload file validation,
- UI rendering consistency.

### 7.3 Testing Strategy Recommended for Submission
- Unit testing for business logic
- Integration testing for student/admin flows
- Form validation testing
- UI testing on desktop and mobile
- File upload testing for PDF and TXT resumes
- Negative testing for invalid credentials and unauthorized access

## 8. SOURCE CODE AND MODULE OVERVIEW
The source code of SkillBuddy is organized in a maintainable way suitable for academic evaluation.

### 8.1 Configuration Layer
`config/settings.py` defines:
- installed apps,
- database configuration,
- static and media paths,
- authentication redirects,
- timezone and template settings.

`config/urls.py` connects Django admin routes and the core application routes.

### 8.2 Core Business Logic Layer
`core/models.py` defines the full relational schema for users, skills, profiles, requirements, groups, events, and resumes.

`core/views.py` contains:
- authentication views,
- role-based dashboard routing,
- student dashboard calculations,
- admin dashboard data loading,
- skill add, update, and remove actions,
- resume upload and analysis logic,
- group and event participation logic,
- reusable helper methods for skill normalization and report generation.

### 8.3 Presentation Layer
The project includes:
- home page,
- login page,
- register page,
- student dashboard,
- admin dashboard,
- shared base template and theme.

The current UI is responsive and uses a custom dark pink and purple pastel palette.

## 9. FEATURES AVAILABLE AT PRESENT TIME
The following features are currently available in the implemented SkillBuddy project:

### 9.1 Authentication and Roles
- user registration for student and admin roles,
- login and logout,
- custom user model with role-based dashboard routing,
- account deletion support.

### 9.2 Student Skill Profile Management
- add new skills,
- remove skills,
- replace an existing skill with an updated one,
- case-insensitive skill reuse to avoid duplicate records such as `html` and `HTML`.

### 9.3 Skill Gap Analysis
- comparison between student skills and required job-role skills,
- matched skill display,
- missing skill display,
- readiness score in percentage,
- recommendation list based on missing skills,
- synchronization after every skill update.

### 9.4 Resume Analysis
- resume upload in PDF or TXT format,
- extraction of text from uploaded files,
- analysis against target-role skill requirements,
- resume readiness score,
- detected strengths and missing skills,
- auto-refresh of report data when profile skills change.

### 9.5 Admin Controls
- create job requirements,
- define required skills for each role,
- create skill-based groups,
- create events and hackathons,
- monitor student target roles and stored skills.

### 9.6 Collaboration Features
- join or leave groups,
- register or cancel event participation,
- use groups and events as guided improvement opportunities.

### 9.7 UI and Experience
- responsive web interface,
- dashboard-based workflow,
- role-specific screens,
- visually updated shared theme,
- database-backed real project behavior instead of dummy data.

## 10. OUTPUT SCREENS AND CURRENT USER JOURNEY
The currently available UI screens in the project are:
- home page,
- login page,
- registration page,
- student dashboard,
- admin dashboard.

### 10.1 Student Journey
1. Student registers and sets a target role.
2. Student adds personal skills.
3. System calculates skill gap against role requirements.
4. Student updates skills as learning progresses.
5. Student uploads resume for analysis.
6. Student joins relevant groups.
7. Student registers for events or hackathons.

### 10.2 Admin Journey
1. Admin logs in to the dashboard.
2. Admin creates job requirements and required skills.
3. Admin creates groups for collaborative learning.
4. Admin publishes events.
5. Admin monitors student progress through dashboard summaries.

### 10.3 Suggested Screenshots for Final College Submission
If the final submission requires screenshots, the following screens should be captured:
- home page
- login page
- register page
- student dashboard with skill gap report
- resume analysis result
- groups and events section
- admin dashboard with student monitoring
- job requirement creation form

## 11. LIMITATIONS OF THE CURRENT VERSION
Although the current project is functional and suitable for demonstration, the present version still has some limitations:
- no advanced analytics dashboard with historical charts,
- no email notifications or reminders,
- no password reset workflow,
- no dedicated API layer for mobile app integration,
- no recommendation engine based on learning resources,
- no resume scoring through NLP models beyond keyword matching,
- no deployment pipeline included in the repository,
- limited automated test coverage compared to full production-grade systems,
- SQLite is suitable for small deployments but not ideal for large-scale multi-user production environments.

## 12. FUTURE SCOPE
SkillBuddy has strong potential for future enhancement. The following improvements can be added in future versions:

### 12.1 Learning Recommendation Engine
- suggest courses, tutorials, and practice projects based on missing skills,
- generate a personalized learning roadmap for each student.

### 12.2 Advanced Resume Intelligence
- integrate NLP-based resume parsing,
- analyze project descriptions, internships, and achievements,
- provide section-wise feedback for resume quality.

### 12.3 Placement and Recruitment Features
- connect students with internships and job postings,
- maintain recruiter-ready profiles,
- match students to openings based on readiness scores.

### 12.4 Notification System
- email alerts for new events and hackathons,
- reminder notifications for missing skills and upcoming deadlines,
- activity alerts for group participation.

### 12.5 Analytics and Reporting
- department-wise performance dashboards,
- trend analysis of student growth over time,
- downloadable reports for faculty and placement coordinators.

### 12.6 Gamification
- badges for completed skill milestones,
- participation points for events and groups,
- leaderboard for healthy learning motivation.

### 12.7 Security and Scalability
- PostgreSQL or MySQL migration,
- cloud deployment,
- media storage in cloud buckets,
- audit logs and stronger admin controls,
- production-ready environment separation.

### 12.8 Mobile and API Expansion
- REST API for frontend/mobile integration,
- Android application for students,
- push notifications and real-time updates.

## 13. MILESTONE AND ENHANCEMENT ROADMAP
The following phased roadmap can be used for future academic or product expansion:

Phase 1 - Completed in current version
- role-based login and registration
- student and admin dashboards
- skill gap report
- resume upload and analysis
- groups and events

Phase 2 - Short-term improvements
- password reset
- richer validation and error handling
- better admin analytics
- improved testing coverage

Phase 3 - Medium-term improvements
- learning recommendation engine
- email notifications
- cloud deployment
- recruiter-facing dashboard

Phase 4 - Long-term improvements
- AI-powered resume evaluation
- mobile app
- public API
- large-scale deployment with production database

## 14. CONCLUSION
SkillBuddy is a meaningful academic software project that successfully combines student development tracking with career readiness analysis. The project demonstrates full-stack web development concepts through a practical use case that is easy to understand and relevant to modern educational needs.

At present, the project already includes real database storage, role-based access, skill management, job requirement mapping, resume analysis, group participation, and event registration. These features make it more than a prototype; it is a working platform that can be expanded into a stronger institutional tool.

The future scope of the project is also significant. With the addition of personalized recommendations, stronger analytics, notifications, recruiter integration, and cloud deployment, SkillBuddy can evolve into a comprehensive student employability platform.

In conclusion, SkillBuddy is suitable for project report submission because it has a clear problem statement, a useful real-world objective, an implemented technical solution, measurable present features, and meaningful opportunities for future enhancement.

## 15. REFERENCES AND BIBLIOGRAPHY
- Django Documentation: https://docs.djangoproject.com/
- Python Documentation: https://docs.python.org/3/
- SQLite Documentation: https://www.sqlite.org/docs.html
- pypdf Documentation: https://pypdf.readthedocs.io/
- Project source files in the current SkillBuddy repository
