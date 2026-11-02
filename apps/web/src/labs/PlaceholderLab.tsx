import type { LabDefinition } from "../data/labs";

export default function PlaceholderLab({ lab }: { lab: LabDefinition }) {
  const Icon = lab.icon;
  return (
    <div className="empty-lab">
      <div className="empty-icon"><Icon size={28} /></div>
      <span className="eyebrow">LABORATÓRIO / ROADMAP</span>
      <h2>{lab.title}</h2>
      <p>{lab.description}. Este módulo está previsto na arquitetura BinLab Engineering e ainda não possui ferramentas implementadas.</p>
      <span className="status-pill">{lab.status}</span>
    </div>
  );
}
