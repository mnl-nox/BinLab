import { useMemo, useState } from "react";
import {
  Activity, ArrowLeftRight, Binary, BookOpen, Boxes, Cpu, FileCode2,
  GitBranch, HardDrive, Menu, Moon, Network,
  ShieldCheck, Sun, Terminal, X
} from "lucide-react";
import { bitwiseOperation, convertInteger, formatInteger, parseInteger, type NumericBase } from "./domain/numbers";

type LabId = "binary" | "architecture" | "compiler" | "systems" | "network" | "security" | "science" | "ai";
const labs: { id: LabId; title: string; description: string; icon: typeof Binary; status: string }[] = [
  { id: "binary", title: "Binary & Logic", description: "Bases, bits e operações lógicas", icon: Binary, status: "Disponível" },
  { id: "architecture", title: "Arquitetura", description: "CPU, ISA, memória e organização", icon: Cpu, status: "Em desenvolvimento" },
  { id: "compiler", title: "Compiler & Code", description: "Compiladores, C, Assembly e ABI", icon: FileCode2, status: "Planejado" },
  { id: "systems", title: "Operating Systems", description: "Processos, memória virtual e kernel", icon: HardDrive, status: "Planejado" },
  { id: "network", title: "Network & Web", description: "Protocolos, diagnóstico e serviços", icon: Network, status: "Planejado" },
  { id: "security", title: "Security & Forensics", description: "Análise estática e investigação", icon: ShieldCheck, status: "Planejado" },
  { id: "science", title: "Scientific Computing", description: "Modelagem, métodos e simulação", icon: Activity, status: "Planejado" },
  { id: "ai", title: "AI & Data", description: "Dados, modelos e inferência local", icon: Boxes, status: "Planejado" }
];

const baseOptions: { value: NumericBase; label: string }[] = [
  { value: 2, label: "Binário · 2" }, { value: 8, label: "Octal · 8" },
  { value: 10, label: "Decimal · 10" }, { value: 16, label: "Hexadecimal · 16" }
];

function BinaryLab() {
  const [input, setInput] = useState("255");
  const [base, setBase] = useState<NumericBase>(10);
  const [left, setLeft] = useState("1100");
  const [right, setRight] = useState("1010");
  const [operator, setOperator] = useState<"&" | "|" | "^" | "<<">("&");

  const converted = useMemo(() => {
    try { return convertInteger(input, base); } catch { return null; }
  }, [input, base]);

  const bitResult = useMemo(() => {
    try {
      const a = parseInteger(left, 2);
      const b = parseInteger(right, operator === "<<" ? 10 : 2);
      return formatInteger(bitwiseOperation(a, operator, b), 2);
    } catch { return null; }
  }, [left, right, operator]);

  return (
    <div className="lab-content">
      <div className="section-heading">
        <div><span className="eyebrow">LABORATÓRIO 01 / FUNDAMENTOS</span><h2>Binary & Logic Lab</h2><p>Explore representações numéricas e operações bit a bit sem enviar dados para serviços externos.</p></div>
        <span className="live-indicator"><i /> Execução local</span>
      </div>
      <div className="tool-grid">
        <section className="panel converter-panel">
          <div className="panel-heading"><div className="panel-icon"><ArrowLeftRight size={18} /></div><div><h3>Conversor de bases</h3><p>Um inteiro, quatro representações</p></div></div>
          <label className="field-label" htmlFor="number-input">Valor de entrada</label>
          <div className="input-row">
            <input id="number-input" value={input} onChange={(event) => setInput(event.target.value)} spellCheck={false} autoComplete="off" />
            <select aria-label="Base de entrada" value={base} onChange={(event) => setBase(Number(event.target.value) as NumericBase)}>
              {baseOptions.map((option) => <option key={option.value} value={option.value}>Base {option.value}</option>)}
            </select>
          </div>
          <div className="result-list">
            {baseOptions.map((option) => <div className="result-row" key={option.value}><span>{option.label}</span><code>{converted?.[option.value] ?? "—"}</code></div>)}
          </div>
          <p className="helper-text">Inteiros via BigInt. A saída usa prefixos 0b, 0o e 0x para identificar as bases.</p>
        </section>
        <section className="panel logic-panel">
          <div className="panel-heading"><div className="panel-icon"><Binary size={18} /></div><div><h3>Operações bit a bit</h3><p>Manipulação direta de bits</p></div></div>
          <label className="field-label" htmlFor="operand-a">Operando A · binário</label>
          <input id="operand-a" className="full-input mono" value={left} onChange={(event) => setLeft(event.target.value)} spellCheck={false} />
          <div className="operator-row">
            <label className="field-label" htmlFor="operator">Operação</label>
            <select id="operator" value={operator} onChange={(event) => setOperator(event.target.value as typeof operator)}>
              <option value="&">AND · &</option><option value="|">OR · |</option><option value="^">XOR · ^</option><option value="<<">SHIFT LEFT · &lt;&lt;</option>
            </select>
          </div>
          <label className="field-label" htmlFor="operand-b">{operator === "<<" ? "Deslocamento · decimal" : "Operando B · binário"}</label>
          <input id="operand-b" className="full-input mono" value={right} onChange={(event) => setRight(event.target.value)} spellCheck={false} />
          <div className="logic-result"><span>Resultado</span><code>{bitResult ?? "Entrada inválida"}</code></div>
          <p className="helper-text">O deslocamento é limitado a 4096 posições. Os operandos são interpretados como inteiros.</p>
        </section>
      </div>
      <section className="note-panel"><BookOpen size={18} /><div><strong>Modelo mental</strong><p>Uma operação bit a bit trabalha sobre a representação inteira. AND mantém bits presentes nos dois operandos; OR combina bits; XOR mantém posições diferentes; deslocamento move os bits e equivale a multiplicar por uma potência de dois para valores não negativos.</p></div></section>
    </div>
  );
}

function PlaceholderLab({ lab }: { lab: typeof labs[number] }) {
  const Icon = lab.icon;
  return <div className="empty-lab"><div className="empty-icon"><Icon size={28} /></div><span className="eyebrow">LABORATÓRIO / ROADMAP</span><h2>{lab.title}</h2><p>{lab.description}. Este módulo está previsto na arquitetura BinLab Engineering e ainda não possui ferramentas implementadas.</p><span className="status-pill">{lab.status}</span></div>;
}

export default function App() {
  const [activeLab, setActiveLab] = useState<LabId>("binary");
  const [dark, setDark] = useState(true);
  const [mobileOpen, setMobileOpen] = useState(false);
  const currentLab = labs.find((lab) => lab.id === activeLab) ?? labs[0];

  return (
    <div className={dark ? "app-shell theme-dark" : "app-shell theme-light"}>
      <aside className={mobileOpen ? "sidebar sidebar-open" : "sidebar"}>
        <div className="brand"><div className="brand-mark">BL<span>.</span></div><div><strong>BINLAB</strong><small>ENGINEERING</small></div><button className="mobile-close" onClick={() => setMobileOpen(false)} aria-label="Fechar menu"><X size={18} /></button></div>
        <div className="workspace-label">WORKSPACE</div>
        <button className="workspace-switch"><span className="workspace-dot" /> Local workspace <span className="chevron">⌄</span></button>
        <div className="nav-label">LABORATÓRIOS</div>
        <nav className="lab-nav" aria-label="Laboratórios">
          {labs.map((lab, index) => {
            const Icon = lab.icon;
            return <button key={lab.id} className={activeLab === lab.id ? "nav-item active" : "nav-item"} onClick={() => { setActiveLab(lab.id); setMobileOpen(false); }}><Icon size={17} /><span>{lab.title}</span>{index === 0 ? <i className="nav-live" /> : <span className="nav-lock">·</span>}</button>;
          })}
        </nav>
        <div className="sidebar-bottom"><div className="system-status"><span className="status-dot" /><div><strong>Modo local</strong><small>Sem conexão com API</small></div></div><a href="https://github.com/mnl-nox/BinLab" target="_blank" rel="noreferrer"><GitBranch size={15} /> Repositório GitHub</a></div>
      </aside>
      {mobileOpen && <button className="mobile-backdrop" onClick={() => setMobileOpen(false)} aria-label="Fechar navegação" />}
      <main className="main-area">
        <header className="topbar"><button className="mobile-menu" onClick={() => setMobileOpen(true)} aria-label="Abrir menu"><Menu size={20} /></button><div className="breadcrumbs"><span>Workspace</span><b>/</b><strong>{currentLab.title}</strong></div><div className="top-actions"><div className="environment-tag"><span /> LOCAL ENVIRONMENT</div><button className="theme-toggle" onClick={() => setDark((value) => !value)} aria-label={dark ? "Ativar tema claro" : "Ativar tema escuro"} title="Alternar tema">{dark ? <Sun size={17} /> : <Moon size={17} />}</button></div></header>
        <div className="page-wrap">
          {activeLab === "binary" ? <BinaryLab /> : <PlaceholderLab lab={currentLab} />}
          <footer className="app-footer"><span>BINLAB ENGINEERING <b>·</b> WEB FOUNDATION 0.1.0</span><span><Terminal size={13} /> Local-first computational workspace</span></footer>
        </div>
      </main>
    </div>
  );
}