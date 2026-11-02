import {
  Activity, Binary, Boxes, Cpu, FileCode2, HardDrive, Network, ShieldCheck
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

export type LabId = "binary" | "architecture" | "compiler" | "systems" | "network" | "security" | "science" | "ai";

export type LabDefinition = {
  id: LabId;
  title: string;
  description: string;
  icon: LucideIcon;
  status: "Disponível" | "Em desenvolvimento" | "Planejado";
};

export const labs: LabDefinition[] = [
  { id: "binary", title: "Binary & Logic", description: "Bases, bits e operações lógicas", icon: Binary, status: "Disponível" },
  { id: "architecture", title: "Arquitetura", description: "CPU, ISA, memória e organização", icon: Cpu, status: "Em desenvolvimento" },
  { id: "compiler", title: "Compiler & Code", description: "Compiladores, C, Assembly e ABI", icon: FileCode2, status: "Planejado" },
  { id: "systems", title: "Operating Systems", description: "Processos, memória virtual e kernel", icon: HardDrive, status: "Planejado" },
  { id: "network", title: "Network & Web", description: "Protocolos, diagnóstico e serviços", icon: Network, status: "Planejado" },
  { id: "security", title: "Security & Forensics", description: "Análise estática e investigação", icon: ShieldCheck, status: "Planejado" },
  { id: "science", title: "Scientific Computing", description: "Modelagem, métodos e simulação", icon: Activity, status: "Planejado" },
  { id: "ai", title: "AI & Data", description: "Dados, modelos e inferência local", icon: Boxes, status: "Planejado" }
];
