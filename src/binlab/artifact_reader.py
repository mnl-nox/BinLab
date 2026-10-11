#!/usr/bin/env python3
"""Serviços de leitura estática e geração de relatórios para arquivos."""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Union


SOURCE_SUFFIXES = {".c", ".h", ".cc", ".cpp", ".cxx", ".s", ".asm", ".S"}
HEX_SUFFIXES = {".hex", ".ihex"}


def detect_format(data: bytes) -> str:
    """Identifica alguns formatos comuns pela assinatura inicial."""
    if data.startswith(b"\x7fELF"):
        return "ELF"
    if data.startswith(b"MZ"):
        return "DOS/Windows (MZ/PE possível)"
    if data.startswith((b"\xfe\xed\xfa\xce", b"\xce\xfa\xed\xfe", b"\xfe\xed\xfa\xcf", b"\xcf\xfa\xed\xfe")):
        return "Mach-O"
    if data.startswith(b"\xca\xfe\xba\xbe"):
        return "Mach-O universal / Java class possível"
    if data.startswith(b"\x00asm"):
        return "WebAssembly"
    if data.startswith(b"\x00\x00\x01\x00"):
        return "Windows COFF object possível"
    return "Formato não reconhecido (binário bruto ou formato não suportado)"


def printable_strings(data: bytes, minimum: int = 4) -> List[str]:
    """Extrai sequências ASCII imprimíveis consecutivas."""
    matches = re.findall(rb"[\x20-\x7e]{" + str(minimum).encode() + rb",}", data)
    return [match.decode("ascii", errors="replace") for match in matches]


def format_hex_dump(data: bytes, limit: int = 512) -> str:
    """Formata bytes em linhas com offset, hexadecimal e ASCII."""
    lines = []
    for offset in range(0, min(len(data), limit), 16):
        chunk = data[offset:offset + 16]
        hex_part = " ".join(f"{byte:02X}" for byte in chunk)
        ascii_part = "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in chunk)
        lines.append(f"{offset:08X}  {hex_part:<47}  |{ascii_part}|")
    if len(data) > limit:
        lines.append(f"... dump limitado aos primeiros {limit} bytes (arquivo: {len(data)} bytes).")
    return "\n".join(lines)


def parse_hex_text(text: str) -> bytes:
    """Lê hexadecimal bruto ou Intel HEX e retorna os bytes decodificados."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("O arquivo hexadecimal está vazio.")
    if all(line.startswith(":") for line in lines):
        result = bytearray()
        upper_address = 0
        for line_number, line in enumerate(lines, 1):
            try:
                record = bytes.fromhex(line[1:])
            except ValueError as error:
                raise ValueError(f"Registro Intel HEX inválido na linha {line_number}.") from error
            if len(record) < 5 or len(record) != record[0] + 5 or sum(record) & 0xFF:
                raise ValueError(f"Tamanho ou checksum inválido na linha {line_number}.")
            count, address, kind = record[0], int.from_bytes(record[1:3], "big"), record[3]
            payload = record[4:4 + count]
            if kind == 0:
                absolute = upper_address + address
                if absolute > len(result):
                    result.extend(b"\x00" * (absolute - len(result)))
                end = absolute + count
                if end > len(result):
                    result.extend(b"\x00" * (end - len(result)))
                result[absolute:end] = payload
            elif kind == 1:
                break
            elif kind == 4 and count == 2:
                upper_address = int.from_bytes(payload, "big") << 16
            elif kind == 2 and count == 2:
                upper_address = int.from_bytes(payload, "big") << 4
            elif kind not in (3, 5):
                raise ValueError(f"Tipo de registro Intel HEX {kind} não suportado (linha {line_number}).")
        if not result:
            raise ValueError("O arquivo Intel HEX não contém dados.")
        return bytes(result)

    compact = re.sub(r"(?i)0x", "", text)
    compact = re.sub(r"[\s,;:_-]", "", compact)
    if not compact or len(compact) % 2:
        raise ValueError("Hexadecimal bruto deve conter pares de dígitos (ex.: DE AD BE EF).")
    try:
        return bytes.fromhex(compact)
    except ValueError as error:
        raise ValueError("O arquivo contém caracteres que não são hexadecimais.") from error


def _summarize_c(text: str) -> str:
    """Gera resumo heurístico de elementos comuns em C."""
    without_comments = re.sub(r"/\*.*?\*/|//[^\n]*", " ", text, flags=re.S)
    includes = re.findall(r"^\s*#\s*include\s*[<\"]([^>\"]+)[>\"]", text, re.M)
    macros = re.findall(r"^\s*#\s*define\s+(\w+)", text, re.M)
    functions = re.findall(r"(?m)^\s*[\w\s*]+\s+\w+\s*\([^;{}]*\)\s*\{", without_comments)
    declarations = re.findall(r"\b(struct|union|enum)\s+\w+", without_comments)
    lines = [
        "Resumo estático de C (contagens aproximadas; não é compilação):",
        f"  Linhas: {len(text.splitlines())}",
        f"  Includes: {len(includes)}" + (f" ({', '.join(includes[:10])})" if includes else ""),
        f"  Macros: {len(macros)}" + (f" ({', '.join(macros[:10])})" if macros else ""),
        f"  Definições de função detectadas: {len(functions)}",
        f"  Estruturas/uniões/enums: {len(declarations)}",
        "Trecho inicial:",
        "\n".join(text.splitlines()[:40]) or "(arquivo vazio)",
    ]
    return "\n".join(lines)


def _summarize_assembly(text: str) -> str:
    """Gera resumo heurístico de linhas de assembly."""
    code = [line.strip() for line in text.splitlines() if line.strip()]
    instructions = [line for line in code if not line.startswith((".", "#", ";")) and not line.endswith(":")]
    labels = [line for line in code if line.endswith(":")]
    directives = [line for line in code if line.startswith(".")]
    return "\n".join((
        "Resumo estático de assembly (heurístico; sintaxe varia por assembler):",
        f"  Linhas não vazias: {len(code)}; instruções estimadas: {len(instructions)}",
        f"  Labels: {len(labels)}; diretivas: {len(directives)}",
        "Trecho inicial:",
        "\n".join(text.splitlines()[:60]) or "(arquivo vazio)",
    ))


def inspect_source(path: Union[str, Path]) -> str:
    """Lê uma fonte C/assembly e retorna um relatório textual."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        raise ValueError(f"Não foi possível ler o arquivo: {error}") from error
    summary = _summarize_c(text) if path.suffix in {".c", ".h", ".cc", ".cpp", ".cxx"} else _summarize_assembly(text)
    return f"Arquivo-fonte: {path} ({len(text.encode('utf-8'))} bytes em UTF-8)\n{summary}"


def _objdump_file(path: str, options: list) -> str:
    """Executa objdump sem shell e retorna saída limitada para o relatório."""
    tool = shutil.which("objdump")
    if not tool:
        return "GNU objdump não encontrado; desassemblagem indisponível."
    try:
        result = subprocess.run(
            [tool] + options + ["--", path], capture_output=True, text=True,
            errors="replace", timeout=20, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return f"objdump não conseguiu analisar o arquivo: {error}"
    output = result.stdout or result.stderr or "objdump não produziu saída."
    if len(output) > 16000:
        output = output[:16000] + "\n... saída limitada a 16000 caracteres."
    return output


def inspect_binary(data: bytes, name: str, disassemble: bool = True) -> str:
    """Gera relatório para bytes binários, sem gravar no fluxo de saída."""
    strings = printable_strings(data)
    lines = [
        f"Arquivo binário: {name}",
        f"Tamanho: {len(data)} bytes",
        f"Formato provável: {detect_format(data)}",
        f"SHA-256: {hashlib.sha256(data).hexdigest()}",
        "",
        "Hex dump (até 512 bytes):",
        format_hex_dump(data),
        "",
        f"Strings ASCII (até 30 de {len(strings)}):",
    ]
    lines.extend(f"  {value[:160]}" for value in strings[:30])
    if len(strings) > 30:
        lines.append("  ...")
    if disassemble:
        lines.extend(("", "Informações e desassemblagem via GNU objdump (saída limitada):", _objdump_file(name, ["-f", "-h", "-d"])))
    return "\n".join(lines)


def disassemble_hex_bytes(data: bytes, architecture: str) -> str:
    """Desassembla bytes HEX temporários com arquitetura definida pelo usuário."""
    tool = shutil.which("objdump")
    if not tool:
        return "GNU objdump não encontrado; desassemblagem indisponível."
    if not architecture:
        return ""
    try:
        with tempfile.NamedTemporaryFile(prefix="binary-reader-", suffix=".bin") as temporary:
            temporary.write(data)
            temporary.flush()
            result = subprocess.run(
                [tool, "-D", "-b", "binary", "-m", architecture, "--", temporary.name],
                capture_output=True, text=True, errors="replace", timeout=20, check=False,
            )
    except (OSError, subprocess.TimeoutExpired) as error:
        return f"objdump não conseguiu analisar os bytes: {error}"
    output = result.stdout or result.stderr or "objdump não produziu saída."
    if len(output) > 16000:
        output = output[:16000] + "\n... saída limitada a 16000 caracteres."
    return "Desassemblagem dos bytes hexadecimais:\n" + output


def inspect_file(path: Union[str, Path], architecture: Optional[str] = None) -> str:
    """Identifica, lê e relata uma fonte, arquivo HEX ou arquivo binário."""
    path = Path(path).expanduser()
    if not path.is_file():
        raise ValueError("Arquivo não encontrado ou caminho não aponta para um arquivo.")
    if path.suffix in SOURCE_SUFFIXES:
        return inspect_source(path)
    try:
        data = path.read_bytes()
    except OSError as error:
        raise ValueError(f"Não foi possível ler o arquivo: {error}") from error
    if path.suffix.lower() in HEX_SUFFIXES:
        try:
            data = parse_hex_text(data.decode("ascii"))
        except (UnicodeDecodeError, ValueError) as error:
            raise ValueError(f"Falha ao interpretar arquivo hexadecimal: {error}") from error
        report = f"Arquivo hexadecimal convertido em {len(data)} bytes.\n{inspect_binary(data, str(path), disassemble=False)}"
        if architecture:
            report += "\n\n" + disassemble_hex_bytes(data, architecture)
        return report
    return inspect_binary(data, str(path))
