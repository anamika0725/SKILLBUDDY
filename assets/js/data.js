export const STORAGE_KEY = "skillbuddy-demo-state-v2";

export const seedData = {
  sessionUserId: null,
  rolesCatalog: [
    { id: "frontend", name: "Frontend Developer", requiredSkills: ["HTML", "CSS", "JavaScript", "React", "Git", "Responsive Design"] },
    { id: "backend", name: "Backend Developer", requiredSkills: ["Python", "Django", "REST API", "SQL", "Git", "Authentication"] },
    { id: "data", name: "Data Analyst", requiredSkills: ["Python", "SQL", "Excel", "Power BI", "Statistics", "Data Visualization"] }
  ],
  users: [
    {
      id: "student-1",
      name: "Aarav Sharma",
      email: "student@skillbuddy.com",
      password: "student123",
      role: "student",
      skills: ["HTML", "CSS", "JavaScript", "Git"],
      targetRole: "Frontend Developer",
      joinedGroupIds: ["group-1"],
      registeredEventIds: ["event-1"]
    },
    {
      id: "admin-1",
      name: "Placement Cell Admin",
      email: "admin@skillbuddy.com",
      password: "admin123",
      role: "admin",
      organization: "SkillBuddy Placement Cell",
      verified: true
    },
    {
      id: "student-2",
      name: "Meera Iyer",
      email: "meera@skillbuddy.com",
      password: "student123",
      role: "student",
      skills: ["Python", "SQL", "Excel"],
      targetRole: "Data Analyst",
      joinedGroupIds: ["group-2"],
      registeredEventIds: ["event-2"]
    }
  ],
  groups: [
    {
      id: "group-1",
      name: "Frontend Sprint Circle",
      description: "Weekly UI practice, portfolio feedback, and mini collaboration sessions.",
      createdBy: "admin-1",
      skillsRequired: ["HTML", "CSS", "React"]
    },
    {
      id: "group-2",
      name: "Data Insights Guild",
      description: "A community for dashboards, storytelling with data, and analytical thinking.",
      createdBy: "admin-1",
      skillsRequired: ["Python", "SQL", "Power BI"]
    },
    {
      id: "group-3",
      name: "Backend Builders Hub",
      description: "API design discussions, database fundamentals, and backend interview prep.",
      createdBy: "admin-1",
      skillsRequired: ["Python", "Django", "SQL"]
    }
  ],
  events: [
    {
      id: "event-1",
      name: "UI Hack Weekend",
      groupId: "group-1",
      date: "2026-04-18",
      description: "A soft-themed interface challenge focused on accessibility and responsive design."
    },
    {
      id: "event-2",
      name: "Data Storytelling Challenge",
      groupId: "group-2",
      date: "2026-04-24",
      description: "Create a dashboard and presentation from a real-world student skills dataset."
    },
    {
      id: "event-3",
      name: "Placement Ready Backend Jam",
      groupId: "group-3",
      date: "2026-05-02",
      description: "Design a skill-gap API and deploy it with authentication and analytics endpoints."
    }
  ]
};
