import { useState } from "react";
import { Terminal } from "lucide-react";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import { labs, type LabId } from "./data/labs";
import BinaryLab from "./labs/binary/BinaryLab";
import PlaceholderLab from "./labs/PlaceholderLab";

export default function App() {
  const [activeLab, setActiveLab] = useState<LabId>("binary");
  const [dark, setDark] = useState(true);
  const [mobileOpen, setMobileOpen] = useState(false);
  const currentLab = labs.find((lab) => lab.id === activeLab) ?? labs[0];

  return (
    <div className={dark ? "app-shell theme-dark" : "app-shell theme-light"}>
      <Sidebar
        labs={labs}
        activeLab={activeLab}
        mobileOpen={mobileOpen}
        onSelect={(id) => { setActiveLab(id); setMobileOpen(false); }}
        onClose={() => setMobileOpen(false)}
      />
      {mobileOpen && <button className="mobile-backdrop" onClick={() => setMobileOpen(false)} aria-label="Fechar navegação" />}
      <main className="main-area">
        <Topbar
          title={currentLab.title}
          dark={dark}
          onToggleTheme={() => setDark((value) => !value)}
          onOpenMenu={() => setMobileOpen(true)}
        />
        <div className="page-wrap">
          {activeLab === "binary" ? <BinaryLab /> : <PlaceholderLab lab={currentLab} />}
          <footer className="app-footer">
            <span>BINLAB ENGINEERING <b>·</b> WEB FOUNDATION 0.1.0</span>
            <span><Terminal size={13} /> Local-first computational workspace</span>
          </footer>
        </div>
      </main>
    </div>
  );
}
