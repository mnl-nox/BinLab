import { Menu, Moon, Sun } from "lucide-react";

type TopbarProps = {
  title: string;
  dark: boolean;
  onToggleTheme: () => void;
  onOpenMenu: () => void;
};

export default function Topbar({ title, dark, onToggleTheme, onOpenMenu }: TopbarProps) {
  return (
    <header className="topbar">
      <button className="mobile-menu" onClick={onOpenMenu} aria-label="Abrir menu"><Menu size={20} /></button>
      <div className="breadcrumbs"><span>Workspace</span><b>/</b><strong>{title}</strong></div>
      <div className="top-actions">
        <div className="environment-tag"><span /> LOCAL ENVIRONMENT</div>
        <button className="theme-toggle" onClick={onToggleTheme} aria-label={dark ? "Ativar tema claro" : "Ativar tema escuro"} title="Alternar tema">{dark ? <Sun size={17} /> : <Moon size={17} />}</button>
      </div>
    </header>
  );
}
