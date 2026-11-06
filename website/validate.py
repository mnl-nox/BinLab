from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
PAGES_BASE_PATH = "/BinLab"


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.tags: set[str] = set()
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.tags.add(tag)
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.errors.append(f"ID duplicado: {element_id}")
            self.ids.add(element_id)

        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.references.append((attribute, value))

        if tag == "a" and values.get("target") == "_blank":
            rel = set((values.get("rel") or "").lower().split())
            if not {"noopener", "noreferrer"}.issubset(rel):
                self.errors.append("Links target=_blank devem usar rel=noopener noreferrer.")

        if tag == "img" and not values.get("alt"):
            self.errors.append("Imagem sem atributo alt.")


def validate_page(path: Path) -> list[str]:
    parser = SiteParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    errors = [f"{path.name}: {error}" for error in parser.errors]

    if "lang" not in (path.read_text(encoding="utf-8").split("<html", 1)[-1].split(">", 1)[0]):
        errors.append(f"{path.name}: atributo lang ausente no elemento html.")
    if "main" not in parser.tags:
        errors.append(f"{path.name}: elemento main ausente.")
    if "title" not in parser.tags:
        errors.append(f"{path.name}: elemento title ausente.")

    for attribute, reference in parser.references:
        parsed = urlparse(reference)
        if parsed.scheme or reference.startswith("//"):
            continue
        if reference.startswith("#"):
            if reference[1:] not in parser.ids:
                errors.append(f"{path.name}: âncora local inexistente: {reference}")
            continue

        if parsed.path.startswith("/"):
            if parsed.path == PAGES_BASE_PATH:
                relative_path = ""
            elif parsed.path.startswith(f"{PAGES_BASE_PATH}/"):
                relative_path = parsed.path[len(PAGES_BASE_PATH) + 1 :]
            else:
                errors.append(
                    f"{path.name}: caminho local fora da base do site {PAGES_BASE_PATH}: {reference}"
                )
                continue
            target = (ROOT / relative_path).resolve()
        else:
            target = (path.parent / parsed.path).resolve()
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            errors.append(f"{path.name}: {attribute} local inexistente: {reference}")

    return errors


def main() -> int:
    pages = [ROOT / "index.html", ROOT / "404.html"]
    errors: list[str] = []
    for page in pages:
        errors.extend(validate_page(page))

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1

    print(f"Validated {len(pages)} HTML pages and their local references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
