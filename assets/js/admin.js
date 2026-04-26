import { logoutUser } from "./auth.js";
import { getCurrentUser, loadState, saveState } from "./storage.js";
import { analyzeSkills, getRoleConfig, parseCsv } from "./utils.js";

let state = loadState();
const user = getCurrentUser(state);

if (!user || user.role !== "admin") {
  window.location.href = "index.html";
}

document.querySelector("#logoutBtn").addEventListener("click", () => {
  logoutUser();
  window.location.href = "index.html";
});

document.querySelector("#resetBtn").addEventListener("click", () => {
  localStorage.removeItem("skillbuddy-demo-state-v2");
  window.location.href = "index.html";
});

document.querySelector("#roleForm").addEventListener("submit", onCreateRoleRequirement);
document.querySelector("#groupForm").addEventListener("submit", onCreateGroup);
document.querySelector("#eventForm").addEventListener("submit", onCreateEvent);

renderAdminDashboard();

function renderAdminDashboard() {
  state = loadState();
  const freshUser = getCurrentUser(state);
  const students = state.users.filter((person) => person.role === "student");

  document.querySelector("#adminWelcome").textContent = `${freshUser.name}, here is today's placement readiness snapshot.`;
  document.querySelector("#totalStudents").textContent = students.length;
  document.querySelector("#totalGroups").textContent = state.groups.length;
  document.querySelector("#totalEvents").textContent = state.events.length;

  renderRoleList();
  renderEventGroupOptions();
  renderStudentMonitor();
}

function renderRoleList() {
  const roleList = document.querySelector("#roleList");
  roleList.innerHTML = "";

  state.rolesCatalog.forEach((role) => {
    const item = document.createElement("article");
    item.className = "stack-item";
    item.innerHTML = `<h4>${role.name}</h4><p>${role.requiredSkills.join(", ")}</p>`;
    roleList.appendChild(item);
  });
}

function renderEventGroupOptions() {
  const select = document.querySelector("#eventGroupSelect");
  select.innerHTML = state.groups.map((group) => `<option value="${group.id}">${group.name}</option>`).join("");
}

function renderStudentMonitor() {
  const container = document.querySelector("#studentMonitor");
  container.innerHTML = "";

  const students = state.users.filter((entry) => entry.role === "student");
  students.forEach((student) => {
    const requirement = getRoleConfig(state, student.targetRole);
    const analysis = analyzeSkills(student.skills, requirement.requiredSkills);
    const item = document.createElement("article");
    item.className = "stack-item";
    item.innerHTML = `
      <h4>${student.name}</h4>
      <div class="meta-row">
        <span class="pill">${student.targetRole}</span>
        <span class="pill accent">${analysis.score}% ready</span>
      </div>
      <p>Missing skills: ${analysis.missing.length ? analysis.missing.join(", ") : "None"}</p>
    `;
    container.appendChild(item);
  });
}

function onCreateRoleRequirement(event) {
  event.preventDefault();
  const name = document.querySelector("#roleNameInput").value.trim();
  const skills = parseCsv(document.querySelector("#roleSkillsInput").value);
  if (!name || !skills.length) return;

  state.rolesCatalog.push({ id: `role-${Date.now()}`, name, requiredSkills: skills });
  saveState(state);
  event.target.reset();
  renderAdminDashboard();
}

function onCreateGroup(event) {
  event.preventDefault();
  state.groups.push({
    id: `group-${Date.now()}`,
    name: document.querySelector("#groupNameInput").value.trim(),
    description: document.querySelector("#groupDescInput").value.trim(),
    createdBy: getCurrentUser(state).id,
    skillsRequired: parseCsv(document.querySelector("#groupSkillsInput").value)
  });

  saveState(state);
  event.target.reset();
  renderAdminDashboard();
}

function onCreateEvent(event) {
  event.preventDefault();
  state.events.push({
    id: `event-${Date.now()}`,
    name: document.querySelector("#eventNameInput").value.trim(),
    groupId: document.querySelector("#eventGroupSelect").value,
    date: document.querySelector("#eventDateInput").value,
    description: document.querySelector("#eventDescInput").value.trim()
  });

  saveState(state);
  event.target.reset();
  renderAdminDashboard();
}
