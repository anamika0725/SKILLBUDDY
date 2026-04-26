import { seedData, STORAGE_KEY } from "./data.js";

export function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  return raw ? JSON.parse(raw) : structuredClone(seedData);
}

export function saveState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

export function resetState() {
  const nextState = structuredClone(seedData);
  saveState(nextState);
  return nextState;
}

export function getCurrentUser(state) {
  return state.users.find((user) => user.id === state.sessionUserId) ?? null;
}
