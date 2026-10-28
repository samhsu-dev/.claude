"""Read fixed project markdown sections; no command runs at import."""
import re
from pathlib import Path


def rule_directory(repository: Path, host: str) -> Path:
    return repository / host / "rules" / "project"


def repository_root(path: Path) -> Path:
    return next((root for root in (path, *path.parents) if (root / ".git").exists()), path)


def section(path: Path, heading: str) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^## " + re.escape(heading) + r"\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return match.group(1) if match else ""


def fields(path: Path, heading: str) -> dict[str, str]:
    return dict(re.findall(r"^- ([\w.]+): (.*)$", section(path, heading), re.M))


def arguments(values: dict[str, str], prefix: str) -> list[str]:
    indexed = [(int(key[len(prefix) + 1:]), value) for key, value in values.items() if re.fullmatch(re.escape(prefix) + r"\.\d+", key)]
    return [value for _, value in sorted(indexed)]
