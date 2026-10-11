#!/usr/bin/env python3
"""Leitor estático educacional para fontes C/assembly e arquivos binários/hex."""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


SOURCE_SUFFIXES = {".c", ".h", ".cc", ".cpp", ".cxx", ".s", ".asm", ".S"}


def detect_format(data: bytes) -> str:
    """Identifica alguns contêineres executáveis comuns pelo cabeçalho."""
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


def printable_strings(data: bytes, minimum: int = 4) -> list[str]:
    """Extrai sequências ASCII imprimíveis consecutivas."""
    matches = re.findall(rb"[\x20-\x7e]{" + str(minimum).encode() + rb",}", data)
    return [match.decode("ascii", errors="replace") for match in matches]


def show_hex_dump(data: bytes, limit: int = 512) -> None:
    """Mostra os primeiros bytes em linhas com offset, hexadecimal e ASCII."""
    shown = data[:limit]
    for offset in range(0, len(shown), 16):
        chunk = shown[offset:offset + 16]
        hex_part = " ".join(f"{byte:02X}" for byte in chunk)
        ascii_part = "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in chunk)
        print(f"{offset:08X}  {hex_part:<47}  |{ascii_part}|")
    if len(data) > limit:
        print(f"... dump limitado aos primeiros {limit} bytes (arquivo: {len(data)} bytes).")


def parse_hex_text(text: str) -> bytes:
    """Lê bytes em hexadecimal, separados por espaço/vírgula, ou Intel HEX."""
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


def summarize_c(text: str) -> None:
    """Apresenta contagens aproximadas de elementos comuns em C."""
    without_comments = re.sub(r"/\*.*?\*/|//[^\n]*", " ", text, flags=re.S)
    includes = re.findall(r"^\s*#\s*include\s*[<\"]([^>\"]+)[>\"]", text, re.M)
    macros = re.findall(r"^\s*#\s*define\s+(\w+)", text, re.M)
    functions = re.findall(r"(?m)^\s*[\w\s*]+\s+\w+\s*\([^;{}]*\)\s*\{", without_comments)
    print("Resumo estático de C (contagens aproximadas; não é compilação):")
    print(f"  Linhas: {len(text.splitlines())}")
    print(f"  Includes: {len(includes)}" + (f" ({', '.join(includes[:10])})" if includes else ""))
    print(f"  Macros: {len(macros)}" + (f" ({', '.join(macros[:10])})" if macros else ""))
    print(f"  Definições de função detectadas: {len(functions)}")
    type_declarations = len(re.findall(r"\b(struct|union|enum)\s+\w+", without_comments))
    print(f"  Estruturas/uniões/enums: {type_declarations}")
    print("Trecho inicial:")
    print("\n".join(text.splitlines()[:40]) or "(arquivo vazio)")


def summarize_assembly(text: str) -> None:
    """Conta linhas de assembly de forma heurística e mostra o início."""
    code = [line.strip() for line in text.splitlines() if line.strip()]
    instructions = [line for line in code if not line.startswith((".", "#", ";")) and not line.endswith(":" )]
    labels = [line for line in code if line.endswith(":")]
    directives = [line for line in code if line.startswith(".")]
    print("Resumo estático de assembly (heurístico; sintaxe varia por assembler):")
    print(f"  Linhas não vazias: {len(code)}; instruções estimadas: {len(instructions)}")
    print(f"  Labels: {len(labels)}; diretivas: {len(directives)}")
    print("Trecho inicial:")
    print("\n".join(text.splitlines()[:60]) or "(arquivo vazio)")


def inspect_source(path: Path) -> None:
    """Lê e resume fonte C ou assembly como texto, sem compilá-lo."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        raise ValueError(f"Não foi possível ler o arquivo: {error}") from error
    print(f"Arquivo-fonte: {path} ({len(text.encode('utf-8'))} bytes em UTF-8)")
    if path.suffix in {".c", ".h", ".cc", ".cpp", ".cxx"}:
        summarize_c(text)
    else:
        summarize_assembly(text)


def inspect_binary(data: bytes, name: str, disassemble: bool = True) -> None:
    """Exibe informações estáticas e, se disponível, solicita disassembly ao objdump."""
    print(f"Arquivo binário: {name}")
    print(f"Tamanho: {len(data)} bytes")
    print(f"Formato provável: {detect_format(data)}")
    print(f"SHA-256: {hashlib.sha256(data).hexdigest()}")
    print("\nHex dump (até 512 bytes):")
    show_hex_dump(data)
    strings = printable_strings(data)
    print(f"\nStrings ASCII (até 30 de {len(strings)}):")
    for value in strings[:30]:
        print(f"  {value[:160]}")
    if len(strings) > 30:
        print("  ...")
    tool = shutil.which("objdump")
    if disassemble and tool:
        print("\nInformações e desassemblagem via GNU objdump (saída limitada):")
        try:
            result = subprocess.run(
                [tool, "-f", "-h", "-d", "--", name],
                capture_output=True, text=True, errors="replace", timeout=20, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            print(f"objdump não conseguiu analisar o arquivo: {error}")
        else:
            output = result.stdout or result.stderr or "objdump não produziu saída."
            print(output[:16000])
            if len(output) > 16000:
                print("... saída limitada a 16000 caracteres.")
    elif disassemble:
        print("\nGNU objdump não encontrado; dump hexadecimal e strings continuam disponíveis.")


def disassemble_hex_bytes(data: bytes, architecture: str) -> None:
    """Desmonta bytes de um dump hexadecimal com arquitetura indicada pelo usuário."""
    tool = shutil.which("objdump")
    if not tool:
        print("GNU objdump não encontrado; desassemblagem indisponível.")
        return
    if not architecture:
        return
    try:
        with tempfile.NamedTemporaryFile(prefix="binary-reader-", suffix=".bin") as temporary:
            temporary.write(data)
            temporary.flush()
            result = subprocess.run(
                [tool, "-D", "-b", "binary", "-m", architecture, "--", temporary.name],
                capture_output=True, text=True, errors="replace", timeout=20, check=False,
            )
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f"objdump não conseguiu analisar os bytes: {error}")
        return
    output = result.stdout or result.stderr or "objdump não produziu saída."
    print("\nDesassemblagem dos bytes hexadecimais:")
    print(output[:16000])
    if len(output) > 16000:
        print("... saída limitada a 16000 caracteres.")


def read_artifact() -> None:
    """Abre um arquivo escolhido pelo usuário e seleciona leitor pelo tipo/extensão."""
    raw_path = input("Caminho do arquivo (C, assembly, binário ou .hex): ").strip()
    if not raw_path:
        raise ValueError("Informe um caminho de arquivo.")
    path = Path(raw_path).expanduser()
    if not path.is_file():
        raise ValueError("Arquivo não encontrado ou caminho não aponta para um arquivo.")
    suffix = path.suffix
    if suffix in SOURCE_SUFFIXES:
        inspect_source(path)
        return
    try:
        data = path.read_bytes()
    except OSError as error:
        raise ValueError(f"Não foi possível ler o arquivo: {error}") from error
    if suffix.lower() in {".hex", ".ihex"}:
        try:
            data = parse_hex_text(data.decode("ascii"))
        except (UnicodeDecodeError, ValueError) as error:
            raise ValueError(f"Falha ao interpretar arquivo hexadecimal: {error}") from error
        print(f"Arquivo hexadecimal convertido em {len(data)} bytes.")
        inspect_binary(data, str(path), disassemble=False)
        architecture = input(
            "Arquitetura para objdump (ex.: i386:x86-64, i386, arm, aarch64; vazio para ignorar): "
        ).strip()
        if architecture:
            disassemble_hex_bytes(data, architecture)
        return
    inspect_binary(data, str(path))
