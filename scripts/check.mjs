import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { projects } from "../site/data/projects.js";
import { supportMethods } from "../site/data/support.js";
import { translations } from "../site/data/i18n.js";

const read = (path) => readFileSync(new URL(path, import.meta.url), "utf8");
const page = read("../site/index.html");
const styles = read("../site/styles.css");
const tokens = read("../site/tokens.css");

assert(page.includes('<html lang="ru" data-theme="dark">'), "Terminal must be the default");
assert(page.includes('content="https://derigava.github.io/support/"'), "Canonical GitHub Pages URL");
assert(!page.includes('src="/') && !page.includes('href="/'), "Avoid root-relative paths");
assert(page.includes('rel="noopener noreferrer"'), "External links need noopener noreferrer");
assert(styles.includes("prefers-reduced-motion"), "Reduced motion");
assert(tokens.includes("--acid: #b8ff2c") && tokens.includes("--acid: #3d6e00"), "Official brand tokens");
assert(projects.length >= 1, "At least one project required");
assert(new Set(projects.map(x => x.id)).size === projects.length, "Project IDs must be unique");
for (const item of projects) {
  assert(item.id && item.title && item.description?.ru && item.description?.en, "Project translations");
  for (const link of item.links) assert(new URL(link.url).protocol === "https:", "HTTPS project links");
}
assert(new Set(supportMethods.map(x => x.id)).size === supportMethods.length, "Unique support IDs");
assert(supportMethods.some(x => x.id === "boosty" && x.enabled && x.url === "https://boosty.to/derigava"), "Boosty support link should be enabled");
assert(page.includes('href="https://boosty.to/derigava"'), "Boosty fallback link should be present in HTML");
for (const item of supportMethods) {
  assert(item.id && item.label && typeof item.enabled === "boolean", "Complete support method");
  if (item.enabled) assert(new URL(item.url).protocol === "https:", "HTTPS payment link");
}
assert.deepEqual(Object.keys(translations.ru).sort(), Object.keys(translations.en).sort(), "Translation keys");
for (const match of page.matchAll(/data-i18n="([^"]+)"/g)) assert(match[1] in translations.ru, "Missing translation " + match[1]);
for (const match of page.matchAll(/data-aria-label="([^"]+)"/g)) assert(match[1] in translations.ru, "Missing ARIA translation " + match[1]);
console.log("Derigava Support static checks passed.");
