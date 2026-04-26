import { loadState, saveState } from "./storage.js";
import { parseCsv } from "./utils.js";

export function loginUser({ email, password, role }) {
  const state = loadState();
  const user = state.users.find(
    (entry) =>
      entry.email.toLowerCase() === email.toLowerCase() &&
      entry.password === password &&
      entry.role === role
  );

  if (!user) {
    return { ok: false, message: "No matching account found for that role." };
  }

  state.sessionUserId = user.id;
  saveState(state);
  return { ok: true, user };
}

export function registerUser({ name, email, password, role, targetRole, skills }) {
  const state = loadState();

  if (state.users.some((entry) => entry.email.toLowerCase() === email.toLowerCase())) {
    return { ok: false, message: "That email is already registered." };
  }

  const newUser = {
    id: `${role}-${Date.now()}`,
    name,
    email: email.toLowerCase(),
    password,
    role
  };

  if (role === "student") {
    newUser.skills = parseCsv(skills);
    newUser.targetRole = targetRole || "Frontend Developer";
    newUser.joinedGroupIds = [];
    newUser.registeredEventIds = [];
  } else {
    newUser.organization = "New SkillBuddy Partner";
    newUser.verified = true;
  }

  state.users.push(newUser);
  state.sessionUserId = newUser.id;
  saveState(state);
  return { ok: true, user: newUser };
}

export function logoutUser() {
  const state = loadState();
  state.sessionUserId = null;
  saveState(state);
}
