#!/usr/bin/env python3
"""Serviços de leitura estática e geração de relatórios para arquivos."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path
from typing import List, Optional, Union


SOURCE_SUFFIXES = {".c", ".h", ".cc", ".cpp", ".cxx", ".s", ".asm", ".S"}
HEX_SUFFIXES = {".hex", ".ihex"}

MAX_SOURCE_BYTES = 2 * 1024 * 1024
MAX_BINARY_BYTES = 8 * 1024 * 1024
MAX_HEX_TEXT_BYTES = 4 * 1024 * 1024
MAX_HEX_DECODED_BYTES = 1024 * 1024
MAX_HEX_GAP_BYTES = 64 * 1024
MAX_STRINGS = 30
MAX_STRING_LENGTH = 160
MAX_OBJDUMP_OUTPUT = 64 * 1024
OBJDUMP_TIMEOUT_SECONDS = 20
MAX_ADDRESS = 0xFFFFFFFF


def _read_limited(path: Path, limit: int, description: str) -> bytes:
    """Lê no máximo limit+1 bytes, impedindo leitura integral ilimitada."""
    try:
        with path.open("rb") as stream:
            data = stream.read(limit + 1)
    except OSError as error:
        raise ValueError("Não foi possível ler o arquivo: {}".format(error)) from error
    if len(data) > limit:
        raise ValueError("{} excede o limite de {} bytes.".format(description, limit))
    return data


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
    """Extrai no máximo 30 strings ASCII, sem materializar todas as ocorrências."""
    if not isinstance(data, bytes):
        raise ValueError("Os dados devem ser bytes.")
    if isinstance(minimum, bool) or not isinstance(minimum, int) or minimum < 1:
        raise ValueError("O tamanho mínimo de string deve ser um inteiro positivo.")
    results = []
    start = None
    for index, value in enumerate(data):
        if 32 <= value <= 126:
            if start is None:
                start = index
        elif start is not None:
            if index - start >= minimum:
                results.append(data[start:min(index, start + MAX_STRING_LENGTH)].decode("ascii"))
                if len(results) >= MAX_STRINGS:
                    return results
            start = None
    if start is not None and len(data) - start >= minimum and len(results) < MAX_STRINGS:
        results.append(data[start:min(len(data), start + MAX_STRING_LENGTH)].decode("ascii"))
    return results


def format_hex_dump(data: bytes, limit: int = 512) -> str:
    """Formata bytes em linhas com offset, hexadecimal e ASCII."""
    if not isinstance(data, bytes):
        raise ValueError("Os dados devem ser bytes.")
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError("O limite do dump deve ser um inteiro não negativo.")
    lines = []
    for offset in range(0, min(len(data), limit), 16):
        chunk = data[offset:offset + 16]
        hex_part = " ".join("{:02X}".format(byte) for byte in chunk)
        ascii_part = "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in chunk)
        lines.append("{:08X}  {:<47}  |{}|".format(offset, hex_part, ascii_part))
    if len(data) > limit:
        lines.append("... dump limitado aos primeiros {} bytes (arquivo: {} bytes).".format(limit, len(data)))
    return "\n".join(lines)


def parse_hex_text(text: str) -> bytes:
    """Lê hexadecimal bruto ou Intel HEX com limites de texto, endereço e span."""
    if not isinstance(text, str):
        raise ValueError("O conteúdo hexadecimal deve ser texto.")
    if len(text) > MAX_HEX_TEXT_BYTES:
        raise ValueError("Texto HEX excede o limite de {} caracteres.".format(MAX_HEX_TEXT_BYTES))
    try:
        text.encode("ascii")
    except UnicodeEncodeError as error:
        raise ValueError("O arquivo HEX deve conter somente caracteres ASCII.") from error

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("O arquivo hexadecimal está vazio.")

    if all(line.startswith(":") for line in lines):
        records = []
        upper_address = 0
        eof_seen = False
        for line_number, line in enumerate(lines, 1):
            if eof_seen:
                raise ValueError("Há registros após EOF na linha {}.".format(line_number))
            payload_text = line[1:]
            if not payload_text or len(payload_text) % 2 or not re.fullmatch(r"[0-9A-Fa-f]+", payload_text):
                raise ValueError("Formato hexadecimal inválido na linha {}.".format(line_number))
            try:
                record = bytes.fromhex(payload_text)
            except ValueError as error:
                raise ValueError("Registro Intel HEX inválido na linha {}.".format(line_number)) from error
            if len(record) < 5:
                raise ValueError("Registro Intel HEX truncado na linha {}.".format(line_number))
            count = record[0]
            if len(record) != count + 5:
                raise ValueError("Contagem de bytes inválida na linha {}.".format(line_number))
            if sum(record) & 0xFF:
                raise ValueError("Checksum inválido na linha {}.".format(line_number))

            address = int.from_bytes(record[1:3], "big")
            kind = record[3]
            data = record[4:4 + count]

            if kind == 0:
                absolute = upper_address + address
                end = absolute + count
                if end > MAX_ADDRESS + 1:
                    raise ValueError("Endereço Intel HEX fora do espaço de 32 bits na linha {}.".format(line_number))
                if count:
                    records.append((absolute, end, data, line_number))
            elif kind == 1:
                if count != 0 or address != 0:
                    raise ValueError("Registro EOF deve ter endereço e contagem iguais a zero (linha {}).".format(line_number))
                eof_seen = True
            elif kind == 2:
                if count != 2 or address != 0:
                    raise ValueError("Registro de endereço segmentado inválido na linha {}.".format(line_number))
                upper_address = int.from_bytes(data, "big") << 4
            elif kind == 3:
                if count != 4 or address != 0:
                    raise ValueError("Registro de início segmentado inválido na linha {}.".format(line_number))
            elif kind == 4:
                if count != 2 or address != 0:
                    raise ValueError("Registro de endereço linear inválido na linha {}.".format(line_number))
                upper_address = int.from_bytes(data, "big") << 16
            elif kind == 5:
                if count != 4 or address != 0:
                    raise ValueError("Registro de início linear inválido na linha {}.".format(line_number))
            else:
                raise ValueError("Tipo de registro Intel HEX {} não suportado (linha {}).".format(kind, line_number))

        if not eof_seen:
            raise ValueError("Arquivo Intel HEX sem registro EOF.")
        if not records:
            raise ValueError("O arquivo Intel HEX não contém dados.")

        records.sort(key=lambda item: (item[0], item[1]))
        previous_end = 0
        max_end = 0
        for start, end, _data, line_number in records:
            if start < previous_end:
                raise ValueError("Registros Intel HEX sobrepostos (linha {}).".format(line_number))
            if start - previous_end > MAX_HEX_GAP_BYTES:
                raise ValueError("Intervalo esparso Intel HEX excede {} bytes.".format(MAX_HEX_GAP_BYTES))
            previous_end = end
            max_end = max(max_end, end)
        if max_end > MAX_HEX_DECODED_BYTES:
            raise ValueError("Span Intel HEX excede o limite de {} bytes.".format(MAX_HEX_DECODED_BYTES))

        result = bytearray(max_end)
        for start, end, data, _line_number in records:
            result[start:end] = data
        return bytes(result)

    compact = re.sub(r"(?i)0x", "", text)
    compact = re.sub(r"[\s,;:_-]", "", compact)
    if not compact or len(compact) % 2:
        raise ValueError("Hexadecimal bruto deve conter pares de dígitos (ex.: DE AD BE EF).")
    if len(compact) // 2 > MAX_HEX_DECODED_BYTES:
        raise ValueError("Hexadecimal bruto excede o limite de {} bytes.".format(MAX_HEX_DECODED_BYTES))
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
        "  Linhas: {}".format(len(text.splitlines())),
        "  Includes: {}".format(len(includes)) + (" ({})".format(", ".join(includes[:10])) if includes else ""),
        "  Macros: {}".format(len(macros)) + (" ({})".format(", ".join(macros[:10])) if macros else ""),
        "  Definições de função detectadas: {}".format(len(functions)),
        "  Estruturas/uniões/enums: {}".format(len(declarations)),
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
        "  Linhas não vazias: {}; instruções estimadas: {}".format(len(code), len(instructions)),
        "  Labels: {}; diretivas: {}".format(len(labels), len(directives)),
        "Trecho inicial:",
        "\n".join(text.splitlines()[:60]) or "(arquivo vazio)",
    ))


def inspect_source(path: Union[str, Path]) -> str:
    """Lê fonte C/assembly com limite aplicado durante a leitura."""
    path = Path(path)
    raw = _read_limited(path, MAX_SOURCE_BYTES, "Arquivo-fonte")
    text = raw.decode("utf-8", errors="replace")
    summary = _summarize_c(text) if path.suffix in {".c", ".h", ".cc", ".cpp", ".cxx"} else _summarize_assembly(text)
    return "Arquivo-fonte: {} ({} bytes)\n{}".format(path, len(raw), summary)


def _run_bounded(command: list, timeout: int = OBJDUMP_TIMEOUT_SECONDS,
                 output_limit: int = MAX_OBJDUMP_OUTPUT) -> str:
    """Executa ferramenta sem shell e limita stdout+stderr enquanto são drenados."""
    environment = {"PATH": os.environ.get("PATH", ""), "LANG": "C", "LC_ALL": "C"}
    if os.name == "nt" and "SYSTEMROOT" in os.environ:
        environment["SYSTEMROOT"] = os.environ["SYSTEMROOT"]
    try:
        process = subprocess.Popen(
            command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            close_fds=True, env=environment,
        )
    except OSError as error:
        raise ValueError("Não foi possível iniciar objdump: {}".format(error)) from error

    buffers = [bytearray(), bytearray()]
    total = [0]
    lock = threading.Lock()
    overflow = threading.Event()

    def drain(pipe, index):
        while True:
            chunk = pipe.read(4096)
            if not chunk:
                break
            with lock:
                remaining = output_limit - total[0]
                if remaining > 0:
                    buffers[index].extend(chunk[:remaining])
                total[0] += len(chunk)
                if total[0] > output_limit:
                    overflow.set()
            if overflow.is_set():
                try:
                    process.kill()
                except OSError:
                    pass

    readers = [
        threading.Thread(target=drain, args=(process.stdout, 0)),
        threading.Thread(target=drain, args=(process.stderr, 1)),
    ]
    for reader in readers:
        reader.daemon = True
        reader.start()
    timed_out = False
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        process.wait()
    for reader in readers:
        reader.join()
    if overflow.is_set():
        suffix = (chr(10) + "[saída truncada: limite de {} bytes excedido]".format(output_limit)).encode("utf-8")
    elif timed_out:
        suffix = b"\n[processo encerrado por timeout]"
    else:
        suffix = b""
    stdout = bytes(buffers[0])
    stderr = bytes(buffers[1])
    output = stdout or stderr or b"objdump não produziu saída."
    return (output + suffix).decode("utf-8", errors="replace")


def _objdump_file(path: str, options: list) -> str:
    """Executa objdump com timeout e limite de saída durante a execução."""
    tool = shutil.which("objdump")
    if not tool:
        return "GNU objdump não encontrado; desassemblagem indisponível."
    try:
        return _run_bounded([tool] + options + ["--", path])
    except ValueError as error:
        return "objdump não conseguiu analisar o arquivo: {}".format(error)


def inspect_binary(data: bytes, name: str, disassemble: bool = True) -> str:
    """Gera relatório para bytes binários, com limites explícitos."""
    if not isinstance(data, bytes):
        raise ValueError("Os dados binários devem ser bytes.")
    if len(data) > MAX_BINARY_BYTES:
        raise ValueError("Arquivo binário excede o limite de {} bytes.".format(MAX_BINARY_BYTES))
    strings = printable_strings(data)
    lines = [
        "Arquivo binário: {}".format(name),
        "Tamanho: {} bytes".format(len(data)),
        "Formato provável: {}".format(detect_format(data)),
        "SHA-256: {}".format(hashlib.sha256(data).hexdigest()),
        "",
        "Hex dump (até 512 bytes):",
        format_hex_dump(data),
        "",
        "Strings ASCII (até {}):".format(MAX_STRINGS),
    ]
    lines.extend("  {}".format(value) for value in strings)
    if len(strings) == MAX_STRINGS:
        lines.append("  ... limite de strings atingido")
    if disassemble:
        lines.extend(("", "Informações e desassemblagem via GNU objdump (saída limitada):",
                      _objdump_file(name, ["-f", "-h", "-d"])))
    return "\n".join(lines)


def disassemble_hex_bytes(data: bytes, architecture: str) -> str:
    """Desassembla bytes HEX temporários com arquitetura definida pelo usuário."""
    if not isinstance(data, bytes) or len(data) > MAX_HEX_DECODED_BYTES:
        raise ValueError("Bytes HEX excedem o limite de desassemblagem.")
    if not isinstance(architecture, str) or not architecture.strip():
        return ""
    tool = shutil.which("objdump")
    if not tool:
        return "GNU objdump não encontrado; desassemblagem indisponível."
    try:
        with tempfile.NamedTemporaryFile(prefix="binary-reader-", suffix=".bin") as temporary:
            temporary.write(data)
            temporary.flush()
            output = _run_bounded([tool, "-D", "-b", "binary", "-m", architecture, "--", temporary.name])
    except (OSError, ValueError) as error:
        return "objdump não conseguiu analisar os bytes: {}".format(error)
    return "Desassemblagem dos bytes hexadecimais:\n" + output


def inspect_file(path: Union[str, Path], architecture: Optional[str] = None) -> str:
    """Identifica, lê e relata fonte, arquivo HEX ou binário com limites."""
    path = Path(path).expanduser()
    if not path.is_file():
        raise ValueError("Arquivo não encontrado ou caminho não aponta para um arquivo.")
    if path.suffix in SOURCE_SUFFIXES:
        return inspect_source(path)

    if path.suffix.lower() in HEX_SUFFIXES:
        raw = _read_limited(path, MAX_HEX_TEXT_BYTES, "Arquivo HEX")
        try:
            data = parse_hex_text(raw.decode("ascii"))
        except (UnicodeDecodeError, ValueError) as error:
            raise ValueError("Falha ao interpretar arquivo hexadecimal: {}".format(error)) from error
        report = "Arquivo hexadecimal convertido em {} bytes.\n{}".format(
            len(data), inspect_binary(data, str(path), disassemble=False)
        )
        if architecture:
            report += "\n\n" + disassemble_hex_bytes(data, architecture)
        return report

    data = _read_limited(path, MAX_BINARY_BYTES, "Arquivo binário")
    return inspect_binary(data, str(path))
