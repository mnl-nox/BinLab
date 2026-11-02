import { GitBranch, X } from "lucide-react";
import type { LabDefinition, LabId } from "../data/labs";

type SidebarProps = {
  labs: LabDefinition[];
  activeLab: LabId;
  mobileOpen: boolean;
  onSelect: (id: LabId) => void;
  onClose: () => void;
};

export default function Sidebar({ labs, activeLab, mobileOpen, onSelect, onClose }: SidebarProps) {
  return (
    <aside className={mobileOpen ? "sidebar sidebar-open" : "sidebar"}>
      <div className="brand">
        <div className="brand-mark">BL<span>.</span></div>
        <div><strong>BINLAB</strong><small>ENGINEERING</small></div>
        <button className="mobile-close" onClick={onClose} aria-label="Fechar menu"><X size={18} /></button>
      </div>
      <div className="workspace-label">WORKSPACE</div>
      <div className="workspace-switch"><span className="workspace-dot" /> Local workspace <span className="chevron">⌄</span></div>
      <div className="nav-label">LABORATÓRIOS</div>
      <nav className="lab-nav" aria-label="Laboratórios">
        {labs.map((lab, index) => {
          const Icon = lab.icon;
          return (
            <button key={lab.id} className={activeLab === lab.id ? "nav-item active" : "nav-item"} onClick={() => onSelect(lab.id)}>
              <Icon size={17} /><span>{lab.title}</span>{index === 0 ? <i className="nav-live" /> : <span className="nav-lock">·</span>}
            </button>
          );
        })}
      </nav>
      <div className="sidebar-bottom">
        <div className="system-status"><span className="status-dot" /><div><strong>Modo local</strong><small>Sem conexão com API</small></div></div>
        <a href="https://github.com/mnl-nox/BinLab" target="_blank" rel="noreferrer"><GitBranch size={15} /> Repositório GitHub</a>
      </div>
    </aside>
  );
}
