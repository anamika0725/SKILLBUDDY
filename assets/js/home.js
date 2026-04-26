import { loginUser, registerUser } from "./auth.js";
import { resetState } from "./storage.js";

const authDialog = document.querySelector("#authDialog");
const authMessage = document.querySelector("#authMessage");
const loginForm = document.querySelector("#loginForm");
const registerForm = document.querySelector("#registerForm");
const loginTabBtn = document.querySelector("#loginTabBtn");
const registerTabBtn = document.querySelector("#registerTabBtn");

document.querySelector("#seedResetBtn").addEventListener("click", () => {
  resetState();
  window.location.href = "index.html";
});

document.querySelector("#openAuthBtn").addEventListener("click", () => openAuth("login"));
document.querySelector("#heroRegisterBtn").addEventListener("click", () => openAuth("register"));
document.querySelector("#studentDemoBtn").addEventListener("click", () => {
  const result = loginUser({
    email: "student@skillbuddy.com",
    password: "student123",
    role: "student"
  });
  if (result.ok) window.location.href = "student.html";
});
document.querySelector("#adminDemoBtn").addEventListener("click", () => {
  const result = loginUser({
    email: "admin@skillbuddy.com",
    password: "admin123",
    role: "admin"
  });
  if (result.ok) window.location.href = "admin.html";
});

loginTabBtn.addEventListener("click", () => setAuthTab("login"));
registerTabBtn.addEventListener("click", () => setAuthTab("register"));

loginForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const result = loginUser({
    email: document.querySelector("#loginEmail").value.trim(),
    password: document.querySelector("#loginPassword").value,
    role: document.querySelector("#loginRole").value
  });

  if (!result.ok) {
    setAuthMessage(result.message);
    return;
  }

  window.location.href = result.user.role === "student" ? "student.html" : "admin.html";
});

registerForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const result = registerUser({
    name: document.querySelector("#registerName").value.trim(),
    email: document.querySelector("#registerEmail").value.trim(),
    password: document.querySelector("#registerPassword").value,
    role: document.querySelector("#registerRole").value,
    targetRole: document.querySelector("#registerTarget").value.trim(),
    skills: document.querySelector("#registerSkills").value
  });

  if (!result.ok) {
    setAuthMessage(result.message);
    return;
  }

  window.location.href = result.user.role === "student" ? "student.html" : "admin.html";
});

function openAuth(tab) {
  setAuthTab(tab);
  authDialog.showModal();
}

function setAuthTab(tab) {
  const isLogin = tab === "login";
  loginTabBtn.classList.toggle("active", isLogin);
  registerTabBtn.classList.toggle("active", !isLogin);
  loginForm.classList.toggle("hidden", !isLogin);
  registerForm.classList.toggle("hidden", isLogin);
  setAuthMessage("");
}

function setAuthMessage(message) {
  authMessage.textContent = message;
}
