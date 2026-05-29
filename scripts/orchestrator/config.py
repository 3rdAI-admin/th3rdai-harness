"""Dependency-free reader for the harness YAML subset, plus typed config loaders.

Supported subset (see plans/native-orchestrator/01-config-and-runlog.md):
  - indentation-based nested mappings (2-space convention, any depth)
  - lists of scalars (``- item``) and lists of mappings (``- key: value`` + continued)
  - scalars: strings, ints, floats, booleans, null
  - inline empty collections ``[]`` and ``{}``
  - ``#`` comments (full-line and inline) and blank lines

Anything outside this subset — tabs in indentation, flow collections with content,
folded/literal block scalars (``>`` / ``|``) — raises YAMLSubsetError with line
context rather than silently guessing.

Paths are resolved relative to a detected repo root (``PROJECT_ROOT`` env override,
else this file's location); no absolute, machine-specific paths are persisted.
"""
from __future__ import annotations

import os
from pathlib import Path

_BLOCK_SCALAR_MARKERS = {"|", ">", "|-", ">-", "|+", ">+"}
_NULLS = {"", "null", "Null", "NULL", "~"}
_TRUE = {"true", "True", "TRUE"}
_FALSE = {"false", "False", "FALSE"}


class YAMLSubsetError(ValueError):
    """Raised when input uses YAML constructs outside the supported subset."""


def repo_root() -> Path:
    """Repo root: ``PROJECT_ROOT`` if set, else two levels up from this file."""
    env = os.environ.get("PROJECT_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    # scripts/orchestrator/config.py -> parents[2] == repo root
    return Path(__file__).resolve().parents[2]


# --- scalar parsing ---------------------------------------------------------

def _scalar(token: str):
    s = token.strip()
    if s in _BLOCK_SCALAR_MARKERS:
        raise YAMLSubsetError(f"block scalars ({s!r}) are not supported; keep values single-line")
    if s in _NULLS:
        return None
    if s == "[]":
        return []
    if s == "{}":
        return {}
    if s in _TRUE:
        return True
    if s in _FALSE:
        return False
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
    if s[0] in "[{":
        raise YAMLSubsetError(f"flow collections with content are not supported: {s!r}")
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


# --- tokenizing -------------------------------------------------------------

def _strip_inline_comment(s: str) -> str:
    in_single = in_double = False
    for i, c in enumerate(s):
        if c == "'" and not in_double:
            in_single = not in_single
        elif c == '"' and not in_single:
            in_double = not in_double
        elif c == "#" and not in_single and not in_double:
            if i == 0 or s[i - 1] == " ":
                return s[:i].rstrip()
    return s


def _tokenize(text: str):
    """Return [(indent, content, lineno)] for significant lines."""
    out = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        n = 0
        while n < len(raw) and raw[n] in " \t":
            n += 1
        if "\t" in raw[:n]:
            raise YAMLSubsetError(f"line {lineno}: tab in indentation; use spaces")
        body = raw[n:]
        if body == "" or body.lstrip().startswith("#"):
            continue
        content = _strip_inline_comment(body).rstrip()
        if content == "":
            continue
        out.append((n, content, lineno))
    return out


def _colon_pos(content: str):
    """Index of the ``key:`` separator (``:`` followed by space), outside quotes."""
    in_single = in_double = False
    for i, c in enumerate(content):
        if c == "'" and not in_double:
            in_single = not in_single
        elif c == '"' and not in_single:
            in_double = not in_double
        elif c == ":" and not in_single and not in_double:
            if i + 1 < len(content) and content[i + 1] == " ":
                return i
    return None


def _is_mapping_line(content: str) -> bool:
    return content.endswith(":") or _colon_pos(content) is not None


def _split_kv(content: str):
    if content.endswith(":"):
        return content[:-1].strip(), ""
    pos = _colon_pos(content)
    if pos is None:
        raise YAMLSubsetError(f"expected 'key: value', got {content!r}")
    return content[:pos].strip(), content[pos + 1:].strip()


# --- recursive descent over the line list -----------------------------------

def _parse_node(lines, idx, indent):
    _, content, _ = lines[idx]
    if content == "-" or content.startswith("- "):
        return _parse_seq(lines, idx, indent)
    if _is_mapping_line(content):
        return _parse_map(lines, idx, indent)
    return _scalar(content), idx + 1


def _parse_map(lines, idx, indent):
    result = {}
    while idx < len(lines):
        cind, content, lineno = lines[idx]
        if cind < indent:
            break
        if cind > indent:
            raise YAMLSubsetError(f"line {lineno}: unexpected indentation")
        if content == "-" or content.startswith("- "):
            raise YAMLSubsetError(f"line {lineno}: sequence not allowed at mapping indent in this subset")
        key, rest = _split_kv(content)
        if rest == "":
            if idx + 1 < len(lines) and lines[idx + 1][0] > indent:
                child = lines[idx + 1][0]
                value, idx = _parse_node(lines, idx + 1, child)
            else:
                value, idx = None, idx + 1
            result[key] = value
        else:
            result[key] = _scalar(rest)
            idx += 1
    return result, idx


def _parse_seq(lines, idx, indent):
    result = []
    while idx < len(lines):
        cind, content, lineno = lines[idx]
        if cind < indent:
            break
        if cind > indent:
            raise YAMLSubsetError(f"line {lineno}: unexpected indentation in sequence")
        if not (content == "-" or content.startswith("- ")):
            break
        after = content[1:].lstrip(" ")
        if after == "":
            if idx + 1 < len(lines) and lines[idx + 1][0] > indent:
                child = lines[idx + 1][0]
                value, idx = _parse_node(lines, idx + 1, child)
            else:
                value, idx = None, idx + 1
            result.append(value)
            continue
        content_indent = cind + (len(content) - len(after))
        # Treat the text after '- ' as a node line at its own column, so a
        # mapping item ('- key: val' + aligned continuations) parses correctly.
        lines[idx] = (content_indent, after, lineno)
        value, idx = _parse_node(lines, idx, content_indent)
        result.append(value)
    return result, idx


# --- public API -------------------------------------------------------------

def load_yaml_string(text: str):
    lines = _tokenize(text)
    if not lines:
        return None
    value, idx = _parse_node(lines, 0, lines[0][0])
    if idx != len(lines):
        raise YAMLSubsetError(f"line {lines[idx][2]}: unexpected indentation or trailing content")
    return value


def load_yaml(path):
    p = Path(path)
    if not p.is_absolute():
        p = repo_root() / p
    return load_yaml_string(p.read_text(encoding="utf-8"))


def load_agents() -> dict:
    doc = load_yaml("configs/agents.yaml")
    return doc.get("agents", {}) if isinstance(doc, dict) else {}


def load_routing() -> dict:
    doc = load_yaml("configs/routing.yaml")
    return doc.get("routes", {}) if isinstance(doc, dict) else {}


def load_models() -> dict:
    doc = load_yaml("configs/models.yaml")
    return doc.get("model_profiles", {}) if isinstance(doc, dict) else {}


def load_tools() -> dict:
    return load_yaml("configs/tools.yaml")


def cross_ref_problems() -> list:
    """Cross-reference checks mirroring scripts/07-validate-harness.sh.

    Returns a list of human-readable problems; empty means the configs are
    internally consistent.
    """
    problems = []
    root = repo_root()
    agents = load_agents()
    models = load_models()
    routes = load_routing()

    for name, spec in agents.items():
        if not isinstance(spec, dict):
            problems.append(f"agent '{name}': malformed entry")
            continue
        profile = spec.get("model_profile")
        if profile not in models:
            problems.append(f"agent '{name}': model_profile '{profile}' not in models.yaml")
        for field in ("contract", "default_skill"):
            rel = spec.get(field)
            if rel and not (root / rel).exists():
                problems.append(f"agent '{name}': {field} path '{rel}' does not exist")

    for rname, rspec in routes.items():
        if not isinstance(rspec, dict):
            problems.append(f"route '{rname}': malformed entry")
            continue
        for agent in rspec.get("agents", []) or []:
            if agent not in agents:
                problems.append(f"route '{rname}': agent '{agent}' not defined in agents.yaml")
        stage = rspec.get("stage")
        if stage and not (root / stage).exists():
            problems.append(f"route '{rname}': stage path '{stage}' does not exist")

    return problems
