export function parseCsv(value) {
  return value.split(",").map((item) => normalizeSkill(item)).filter(Boolean);
}

export function normalizeSkill(value) {
  return value.trim().replace(/\s+/g, " ");
}

export function analyzeSkills(userSkills, requiredSkills) {
  const normalizedSkills = userSkills.map((skill) => skill.toLowerCase());
  const matched = requiredSkills.filter((skill) => normalizedSkills.includes(skill.toLowerCase()));
  const missing = requiredSkills.filter((skill) => !normalizedSkills.includes(skill.toLowerCase()));
  const score = requiredSkills.length ? Math.round((matched.length / requiredSkills.length) * 100) : 0;
  return { matched, missing, score };
}

export function getRoleConfig(state, roleName) {
  return state.rolesCatalog.find((role) => role.name === roleName) ?? state.rolesCatalog[0];
}

export function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric"
  });
}

export function requireRole(user, role) {
  if (!user || user.role !== role) {
    window.location.href = role === "student" ? "../../index.html" : "../../index.html";
  }
}
