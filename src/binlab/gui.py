#!/usr/bin/env python3
"""Interface gráfica Tkinter para operações e leitura estática do BinLab."""

from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk
from typing import Callable

from . import __version__
from .artifact_reader import inspect_file
from .domain.analysis import analyze_bits
from .domain.numeric import format_integer, parse_integer
from .domain.operations import calculate


BASES = {"Binário (2)": 2, "Octal (8)": 8, "Decimal (10)": 10, "Hexadecimal (16)": 16}
COLORS = {
    "background": "#F7F8FA",
    "panel": "#FFFFFF",
    "surface_alt": "#E9EEF5",
    "accent": "#174EA6",
    "accent_active": "#123C80",
    "text": "#17202A",
    "muted": "#3F4C5B",
    "border": "#65758B",
}


class BinLabGUI:
    """Janela principal com abas para converter, calcular e inspecionar dados."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title(f"BinLab {__version__} — Operações e análise binária")
        root.geometry("980x740")
        root.minsize(760, 600)
        root.configure(bg=COLORS["background"])

        style = ttk.Style(root)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("TFrame", background=COLORS["background"])
        style.configure("Panel.TFrame", background=COLORS["panel"])
        style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text"], font=("TkDefaultFont", 10))
        style.configure("Logo.TLabel", font=("TkDefaultFont", 24, "bold"), foreground=COLORS["accent"])
        style.configure("Muted.TLabel", foreground=COLORS["muted"])
        style.configure("TNotebook", background=COLORS["background"], borderwidth=0)
        style.configure("TNotebook.Tab", padding=(13, 8), background=COLORS["surface_alt"], foreground=COLORS["text"])
        style.map(
            "TNotebook.Tab",
            background=[("selected", COLORS["accent"])],
            foreground=[("selected", COLORS["panel"])],
        )
        style.configure("TButton", padding=(10, 6), font=("TkDefaultFont", 10, "bold"),
                        background=COLORS["accent"], foreground=COLORS["panel"], bordercolor=COLORS["accent"],
                        focuscolor=COLORS["accent"], focusthickness=2)
        style.map(
            "TButton",
            background=[("disabled", COLORS["surface_alt"]), ("active", COLORS["accent_active"])],
            foreground=[("disabled", COLORS["muted"]), ("active", COLORS["panel"])],
        )
        style.configure("TEntry", fieldbackground=COLORS["panel"], foreground=COLORS["text"],
                        insertcolor=COLORS["text"], bordercolor=COLORS["border"], focuscolor=COLORS["accent"])
        style.configure("TCombobox", fieldbackground=COLORS["panel"], foreground=COLORS["text"],
                        arrowcolor=COLORS["text"], bordercolor=COLORS["border"])
        style.configure("TCheckbutton", background=COLORS["background"], foreground=COLORS["text"])

        header = ttk.Frame(root, padding=(24, 14, 24, 8))
        header.pack(fill="x")
        ttk.Label(header, text="BL", style="Logo.TLabel").pack(anchor="w")
        ttk.Label(header, text="Operações e análise binária", style="Muted.TLabel").pack(anchor="w")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=8)
        self._build_converter()
        self._build_calculator()
        self._build_analyzer()
        self._build_reader()

        self.status = tk.StringVar(value="Pronto")
        ttk.Label(root, textvariable=self.status, style="Muted.TLabel", padding=(22, 8)).pack(fill="x")

    def _tab(self, title: str) -> ttk.Frame:
        frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(frame, text=title)
        return frame

    def _field(self, parent: ttk.Frame, label: str, row: int, default: str = "") -> ttk.Entry:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=9)
        entry = ttk.Entry(parent, width=42)
        entry.grid(row=row, column=1, sticky="ew", pady=9)
        if default:
            entry.insert(0, default)
        parent.columnconfigure(1, weight=1)
        return entry

    def _output(self, parent: ttk.Frame, height: int = 12) -> tk.Text:
        holder = ttk.Frame(parent, style="Panel.TFrame", padding=8)
        holder.pack(fill="both", expand=True, pady=(16, 0))
        output = tk.Text(holder, height=height, wrap="word", bg=COLORS["panel"], fg=COLORS["text"],
                         insertbackground=COLORS["text"], selectbackground=COLORS["accent"],
                         selectforeground=COLORS["panel"], relief="solid", borderwidth=1,
                         highlightthickness=1, highlightbackground=COLORS["border"],
                         highlightcolor=COLORS["accent"], padx=12, pady=10, font=("TkFixedFont", 10))
        scrollbar = ttk.Scrollbar(holder, orient="vertical", command=output.yview)
        output.configure(yscrollcommand=scrollbar.set)
        output.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return output

    def _show(self, output: tk.Text, text: str) -> None:
        output.configure(state="normal")
        output.delete("1.0", "end")
        output.insert("1.0", text.rstrip() + "\n")
        output.configure(state="disabled")

    def _run(self, output: tk.Text, action: Callable[[], str]) -> None:
        try:
            result = action()
        except (ValueError, OSError, UnicodeError) as error:
            self._show(output, f"Erro: {error}")
            self.status.set("Revise os dados informados")
        except Exception as error:  # Keep GUI errors visible instead of closing the window.
            self._show(output, f"Falha ao processar: {error}")
            self.status.set("A operação não foi concluída")
        else:
            self._show(output, result)
            self.status.set("Operação concluída")

    def _build_converter(self) -> None:
        tab = self._tab("Conversor")
        ttk.Label(tab, text="Converta inteiros entre as bases mais comuns.", style="Muted.TLabel").pack(anchor="w", pady=(0, 8))
        form = ttk.Frame(tab)
        form.pack(fill="x")
        self.convert_value = self._field(form, "Valor de entrada", 0, "0x2A")
        ttk.Label(form, text="Base de origem").grid(row=1, column=0, sticky="w", padx=(0, 12), pady=9)
        self.source_base = ttk.Combobox(form, values=list(BASES), state="readonly", width=38)
        self.source_base.current(3)
        self.source_base.grid(row=1, column=1, sticky="ew", pady=9)
        ttk.Label(form, text="Base de destino").grid(row=2, column=0, sticky="w", padx=(0, 12), pady=9)
        self.target_base = ttk.Combobox(form, values=list(BASES), state="readonly", width=38)
        self.target_base.current(0)
        self.target_base.grid(row=2, column=1, sticky="ew", pady=9)
        ttk.Button(tab, text="Converter", command=lambda: self._run(self.convert_output, self._convert)).pack(anchor="w", pady=(10, 0))
        self.convert_output = self._output(tab, 10)

    def _convert(self) -> str:
        source = BASES[self.source_base.get()]
        target = BASES[self.target_base.get()]
        value = parse_integer(self.convert_value.get(), source)
        return (f"Entrada: {self.convert_value.get()}\n"
                f"Decimal: {value}\n"
                f"Binário: {format_integer(value, 2)}\n"
                f"Octal: {format_integer(value, 8)}\n"
                f"Hexadecimal: {format_integer(value, 16)}\n"
                f"Resultado na base {target}: {format_integer(value, target)}")

    def _build_calculator(self) -> None:
        tab = self._tab("Calculadora")
        ttk.Label(tab, text="Informe os operandos em binário; para NOT, defina a largura em bits.", style="Muted.TLabel").pack(anchor="w", pady=(0, 8))
        form = ttk.Frame(tab)
        form.pack(fill="x")
        self.operand_a = self._field(form, "Operando A", 0, "1010")
        self.operand_b = self._field(form, "Operando B / deslocamento", 1, "0011")
        ttk.Label(form, text="Operação").grid(row=2, column=0, sticky="w", padx=(0, 12), pady=9)
        self.operator = ttk.Combobox(form, values=["+", "-", "*", "//", "%", "AND", "OR", "XOR", "NOT", "<<", ">>"], state="readonly")
        self.operator.current(0)
        self.operator.grid(row=2, column=1, sticky="ew", pady=9)
        self.width_entry = self._field(form, "Largura de NOT (opcional)", 3)
        ttk.Button(tab, text="Calcular", command=lambda: self._run(self.calc_output, self._calculate)).pack(anchor="w", pady=(10, 0))
        self.calc_output = self._output(tab, 10)

    def _calculate(self) -> str:
        a_text = self.operand_a.get().strip().replace("_", "")
        a = parse_integer(a_text, 2)
        operator = self.operator.get()
        b_text = self.operand_b.get().strip().replace("_", "")
        if operator == "NOT":
            bit_text = a_text[2:] if a_text.lower().startswith("0b") else a_text
            width = int(self.width_entry.get()) if self.width_entry.get().strip() else len(bit_text)
            result = calculate(a, operator, width=width)
        else:
            b = parse_integer(b_text, 2)
            result = calculate(a, operator, b)
        return (f"{a_text} {operator} {b_text or '(sem B)'}\n"
                f"Binário: {format_integer(result, 2)}\n"
                f"Decimal: {result}\n"
                f"Hexadecimal: {format_integer(result, 16)}")

    def _build_analyzer(self) -> None:
        tab = self._tab("Análise de bits")
        ttk.Label(tab, text="Interpreta a sequência como valor sem sinal e complemento de dois.", style="Muted.TLabel").pack(anchor="w", pady=(0, 8))
        self.bits_entry = ttk.Entry(tab)
        self.bits_entry.insert(0, "0100_0001")
        self.bits_entry.pack(fill="x", pady=10)
        ttk.Button(tab, text="Analisar", command=lambda: self._run(self.analysis_output, self._analyze)).pack(anchor="w")
        self.analysis_output = self._output(tab, 14)

    def _analyze(self) -> str:
        analysis = analyze_bits(self.bits_entry.get())
        result = [f"Largura: {analysis.width} bits", f"Sem sinal: {analysis.unsigned_value}",
                  f"Complemento de dois: {analysis.signed_value}", f"Hexadecimal: 0x{analysis.hexadecimal}",
                  f"Bits 1: {analysis.ones}", f"Bits 0: {analysis.zeros}"]
        if analysis.byte_hex is not None:
            result.extend((f"Bytes hex: {analysis.byte_hex}", f"ASCII: {analysis.ascii_text}"))
        else:
            result.append("ASCII: sequência não alinhada em bytes")
        return "\n".join(result)

    def _build_reader(self) -> None:
        tab = self._tab("Leitor de arquivos")
        ttk.Label(tab, text="Leitura estática: fontes C/assembly, HEX/Intel HEX e arquivos binários.", style="Muted.TLabel").pack(anchor="w", pady=(0, 8))
        row = ttk.Frame(tab)
        row.pack(fill="x")
        self.path_entry = ttk.Entry(row)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(row, text="Escolher arquivo…", command=self._browse).pack(side="right")
        controls = ttk.Frame(tab)
        controls.pack(fill="x", pady=12)
        self.disassemble_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(controls, text="Desassemblar HEX com objdump", variable=self.disassemble_var).pack(side="left")
        ttk.Label(controls, text="Arquitetura:").pack(side="left", padx=(16, 6))
        self.arch_entry = ttk.Entry(controls, width=22)
        self.arch_entry.insert(0, "i386:x86-64")
        self.arch_entry.pack(side="left")
        ttk.Button(tab, text="Ler arquivo", command=lambda: self._run(self.reader_output, self._inspect_file)).pack(anchor="w")
        self.reader_output = self._output(tab, 16)

    def _browse(self) -> None:
        path = filedialog.askopenfilename(
            title="Selecione C, assembly, HEX ou um binário",
            initialdir=str(Path.home()),
        )
        if path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)

    def _inspect_file(self) -> str:
        raw_path = self.path_entry.get().strip()
        if not raw_path:
            raise ValueError("Selecione um arquivo existente.")
        architecture = self.arch_entry.get().strip() if self.disassemble_var.get() else None
        return inspect_file(raw_path, architecture)


def main() -> None:
    """Inicia a janela principal do BinLab."""
    try:
        root = tk.Tk()
    except tk.TclError as error:
        print(
            "Não foi possível abrir a interface gráfica. O BinLab precisa de uma "
            "sessão X11/XWayland acessível. Verifique DISPLAY e XAUTHORITY ou "
            "execute o comando em um desktop com suporte gráfico.\n"
            f"Detalhe: {error}",
            file=sys.stderr,
        )
        raise SystemExit(1) from None
    BinLabGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
