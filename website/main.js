const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#primary-nav");
const themeButton = document.querySelector(".theme-toggle");
const root = document.documentElement;

function applyTheme(theme, persist = false) {
  const selectedTheme = theme === "light" ? "light" : "dark";
  root.dataset.theme = selectedTheme;
  document.querySelector('meta[name="theme-color"]')?.setAttribute(
    "content",
    selectedTheme === "dark" ? "#0b1020" : "#f5f7fa",
  );
  themeButton?.setAttribute(
    "aria-label",
    selectedTheme === "dark" ? "Ativar tema claro" : "Ativar tema escuro",
  );
  themeButton?.setAttribute(
    "title",
    selectedTheme === "dark" ? "Ativar tema claro" : "Ativar tema escuro",
  );
  document.querySelectorAll(".brand-logo").forEach((logo) => {
    logo.setAttribute(
      "src",
      selectedTheme === "dark" ? "./assets/binlab-logo.svg" : "./assets/binlab-logo-light.svg",
    );
  });

  if (persist) {
    try {
      window.localStorage.setItem("binlab-theme", selectedTheme);
    } catch {
      // The theme still works when storage is unavailable.
    }
  }
}

try {
  const savedTheme = window.localStorage.getItem("binlab-theme");
  if (savedTheme === "light" || savedTheme === "dark") {
    applyTheme(savedTheme);
  } else {
    applyTheme(root.dataset.theme);
  }
} catch {
  applyTheme(root.dataset.theme);
}

menuButton?.addEventListener("click", () => {
  const isOpen = navigation?.classList.toggle("is-open") ?? false;
  menuButton.setAttribute("aria-expanded", String(isOpen));
  menuButton.setAttribute("aria-label", isOpen ? "Fechar navegação" : "Abrir navegação");
});

navigation?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    navigation.classList.remove("is-open");
    menuButton?.setAttribute("aria-expanded", "false");
    menuButton?.setAttribute("aria-label", "Abrir navegação");
  });
});

themeButton?.addEventListener("click", () => {
  const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
  applyTheme(nextTheme, true);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && navigation?.classList.contains("is-open")) {
    navigation.classList.remove("is-open");
    menuButton?.setAttribute("aria-expanded", "false");
    menuButton?.setAttribute("aria-label", "Abrir navegação");
    menuButton?.focus();
  }
});
