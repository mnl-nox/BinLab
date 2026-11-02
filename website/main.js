const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#primary-nav");
const themeButton = document.querySelector(".theme-toggle");
const root = document.documentElement;

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
  root.dataset.theme = nextTheme;
  const themeColor = document.querySelector('meta[name="theme-color"]');
  themeColor?.setAttribute("content", nextTheme === "dark" ? "#0b1020" : "#f5f7fa");
  themeButton.setAttribute("aria-label", nextTheme === "dark" ? "Ativar tema claro" : "Ativar tema escuro");
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && navigation?.classList.contains("is-open")) {
    navigation.classList.remove("is-open");
    menuButton?.setAttribute("aria-expanded", "false");
    menuButton?.setAttribute("aria-label", "Abrir navegação");
    menuButton?.focus();
  }
});
