import { projects } from "./data/projects.js";
import { supportMethods } from "./data/support.js";
import { translations } from "./data/i18n.js";

const $ = (selector) => document.querySelector(selector);
const validUrl = (url) => {
  try {
    return new URL(url).protocol === "https:";
  } catch {
    return false;
  }
};
const readPreference = (key, validValues, fallback) => {
  try {
    const saved = localStorage.getItem(key);
    return validValues.includes(saved) ? saved : fallback;
  } catch {
    return fallback;
  }
};
const savePreference = (key, value) => {
  try { localStorage.setItem(key, value); } catch { /* Storage may be disabled */ }
};
let lang = readPreference("derigava-support-lang", ["ru", "en"], "ru");
let theme = readPreference("derigava-support-theme", ["dark", "light"], "dark");

function createLink(url, label, className) {
  const link = document.createElement("a");
  link.href = url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.className = className;
  link.textContent = label + " ↗";
  return link;
}
function renderProjects() {
  const list = $("#project-list");
  const fragment = document.createDocumentFragment();
  for (const project of projects) {
    const article = document.createElement("article");
    article.className = "project-card";
    const details = document.createElement("div");
    const meta = document.createElement("div");
    meta.className = "project-card__meta";
    meta.textContent = project.category || "OPEN SOURCE";
    const title = document.createElement("h3");
    title.textContent = project.title;
    const desc = document.createElement("p");
    desc.textContent = project.description[lang] || project.description.ru;
    details.append(meta, title, desc);
    const links = document.createElement("div");
    links.className = "project-card__links";
    for (const item of project.links) {
      if (validUrl(item.url)) {
        links.append(createLink(item.url, translations[lang][item.id] || item.id, ""));
      }
    }
    article.append(details, links);
    fragment.append(article);
  }
  list.replaceChildren(fragment);
}
function renderSupport() {
  const list = $("#support-methods");
  const visible = supportMethods.filter((item) => item.enabled !== false && validUrl(item.url));
  if (!visible.length) {
    const placeholder = document.createElement("p");
    placeholder.className = "empty-state";
    placeholder.textContent = translations[lang].supportSoon;
    list.replaceChildren(placeholder);
    return;
  }
  list.replaceChildren(...visible.map((item) => createLink(item.url, item.label, "method-link")));
}
function applyTheme() {
  document.documentElement.dataset.theme = theme;
  document.querySelectorAll("[data-theme-select]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.themeSelect === theme));
  });
}
function applyLanguage() {
  const dictionary = translations[lang];
  document.documentElement.lang = lang;
  document.title = dictionary.title;
  const description = $('meta[name="description"]');
  if (description) description.content = dictionary.description;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const key = element.dataset.i18n;
    if (key in dictionary) {
      // Only literal author-controlled translations enter these designated slots.
      element.innerHTML = dictionary[key];
    }
  });
  document.querySelectorAll("[data-aria-label]").forEach((element) => {
    const key = element.dataset.ariaLabel;
    if (key in dictionary) element.setAttribute("aria-label", dictionary[key]);
  });
  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.lang === lang));
  });
  renderProjects();
  renderSupport();
}
document.querySelectorAll("[data-lang]").forEach((button) => button.addEventListener("click", () => {
  lang = button.dataset.lang;
  savePreference("derigava-support-lang", lang);
  applyLanguage();
}));
document.querySelectorAll("[data-theme-select]").forEach((button) => button.addEventListener("click", () => {
  theme = button.dataset.themeSelect;
  savePreference("derigava-support-theme", theme);
  applyTheme();
}));
applyTheme();
applyLanguage();
