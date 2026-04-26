import { logoutUser } from "./auth.js";
import { getCurrentUser, loadState, saveState } from "./storage.js";
import { analyzeSkills, formatDate, getRoleConfig, normalizeSkill } from "./utils.js";

let state = loadState();
const user = getCurrentUser(state);

if (!user || user.role !== "student") {
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

document.querySelector("#skillForm").addEventListener("submit", onAddSkill);
document.addEventListener("click", handlePageClick);

renderStudentDashboard();

function renderStudentDashboard() {
  state = loadState();
  const freshUser = getCurrentUser(state);
  const roleConfig = getRoleConfig(state, freshUser.targetRole);
  const analysis = analyzeSkills(freshUser.skills, roleConfig.requiredSkills);

  document.querySelector("#studentWelcome").textContent = `${freshUser.name}, your growth path is looking clear.`;
  document.querySelector("#studentTargetRole").textContent = freshUser.targetRole;
  document.querySelector("#readinessScore").textContent = `${analysis.score}% ready`;
  document.querySelector("#membershipCount").textContent = `${freshUser.joinedGroupIds.length} joined`;
  document.querySelector("#eventCount").textContent = `${freshUser.registeredEventIds.length} registered`;

  renderSkillChips(freshUser);
  renderAnalysis(analysis);
  renderStudentGroups(freshUser);
  renderStudentEvents(freshUser);
}

function renderSkillChips(currentUser) {
  const container = document.querySelector("#studentSkillChips");
  container.innerHTML = "";

  currentUser.skills.forEach((skill) => {
    const chip = document.createElement("div");
    chip.className = "chip";
    chip.innerHTML = `<span>${skill}</span><button type="button" data-action="remove-skill" data-skill="${skill}">x</button>`;
    container.appendChild(chip);
  });
}

function renderAnalysis(analysis) {
  fillChips("#matchedSkills", analysis.matched);
  fillChips("#missingSkills", analysis.missing);

  const suggestionsList = document.querySelector("#suggestionsList");
  suggestionsList.innerHTML = "";
  const recommendations = analysis.missing.length
    ? analysis.missing.map((skill) => `Build ${skill} through one project, one group discussion, and one event this month.`)
    : ["You match every listed requirement. Keep building projects and participating in hackathons."];

  recommendations.forEach((tip) => {
    const item = document.createElement("li");
    item.textContent = tip;
    suggestionsList.appendChild(item);
  });
}

function renderStudentGroups(currentUser) {
  const container = document.querySelector("#studentGroups");
  container.innerHTML = "";

  const groups = state.groups
    .map((group) => ({ ...group, matchCount: group.skillsRequired.filter((skill) => currentUser.skills.includes(skill)).length }))
    .sort((a, b) => b.matchCount - a.matchCount);

  groups.forEach((group) => {
    const joined = currentUser.joinedGroupIds.includes(group.id);
    const item = document.createElement("article");
    item.className = "stack-item";
    item.innerHTML = `
      <h4>${group.name}</h4>
      <div class="meta-row">
        <span class="pill neutral">${group.matchCount} skill match</span>
        <span class="pill">${group.skillsRequired.join(" | ")}</span>
      </div>
      <p>${group.description}</p>
      <button type="button" data-action="toggle-group" data-group-id="${group.id}">${joined ? "Joined" : "Join Group"}</button>
    `;
    container.appendChild(item);
  });
}

function renderStudentEvents(currentUser) {
  const container = document.querySelector("#studentEvents");
  container.innerHTML = "";

  state.events.forEach((event) => {
    const registered = currentUser.registeredEventIds.includes(event.id);
    const group = state.groups.find((entry) => entry.id === event.groupId);
    const item = document.createElement("article");
    item.className = "stack-item";
    item.innerHTML = `
      <h4>${event.name}</h4>
      <div class="meta-row">
        <span class="pill accent">${formatDate(event.date)}</span>
        <span class="pill neutral">${group?.name ?? "General"}</span>
      </div>
      <p>${event.description}</p>
      <button type="button" data-action="toggle-event" data-event-id="${event.id}">${registered ? "Registered" : "Register"}</button>
    `;
    container.appendChild(item);
  });
}

function onAddSkill(event) {
  event.preventDefault();
  const input = document.querySelector("#skillInput");
  const freshUser = getCurrentUser(state);
  const skill = normalizeSkill(input.value);

  if (!skill || freshUser.skills.some((entry) => entry.toLowerCase() === skill.toLowerCase())) {
    input.value = "";
    return;
  }

  freshUser.skills.push(skill);
  saveState(state);
  input.value = "";
  renderStudentDashboard();
}

function handlePageClick(event) {
  const trigger = event.target.closest("[data-action]");
  if (!trigger) return;

  const freshUser = getCurrentUser(state);

  if (trigger.dataset.action === "remove-skill") {
    freshUser.skills = freshUser.skills.filter((skill) => skill !== trigger.dataset.skill);
  }

  if (trigger.dataset.action === "toggle-group") {
    const groupId = trigger.dataset.groupId;
    const index = freshUser.joinedGroupIds.indexOf(groupId);
    if (index >= 0) freshUser.joinedGroupIds.splice(index, 1);
    else freshUser.joinedGroupIds.push(groupId);
  }

  if (trigger.dataset.action === "toggle-event") {
    const eventId = trigger.dataset.eventId;
    const index = freshUser.registeredEventIds.indexOf(eventId);
    if (index >= 0) freshUser.registeredEventIds.splice(index, 1);
    else freshUser.registeredEventIds.push(eventId);
  }

  saveState(state);
  renderStudentDashboard();
}

function fillChips(selector, values) {
  const container = document.querySelector(selector);
  container.innerHTML = values.length
    ? values.map((value) => `<div class="chip"><span>${value}</span></div>`).join("")
    : `<div class="chip"><span>None yet</span></div>`;
}
