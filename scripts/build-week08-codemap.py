#!/usr/bin/env python3
"""week08-service-lab의 심볼과 관계를 뽑아 `<SymbolMap />`의 데이터로 만든다.

손으로 적은 그림이 아니라 **실제 코드를 파싱한 결과**다. 저장소가 바뀌면
다시 돌린다.

    python3 scripts/build-week08-codemap.py [저장소 경로]

관계는 네 종류로 나눈다.
  · call      함수가 함수를 부른다
  · construct 함수가 클래스를 만든다 (사용)
  · returns   함수가 그 타입을 돌려준다
  · param     함수가 그 타입을 받는다
  · inherits  클래스가 클래스를 상속한다
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

REPO = Path(sys.argv[1] if len(sys.argv) > 1 else "../week08-service-lab").resolve()
OUT = Path(__file__).resolve().parent.parent / "site/src/data/week08-codemap.json"

TARGETS = ["core", "api", "mcp_server"]
EXTRA_FILES = ["clients/py_client.py"]
LAYER = {"api": "door", "mcp_server": "door", "core": "core", "clients": "client"}
LAYER_LABEL = {
    "door": "문 — 이번 주에 다는 껍데기",
    "core": "코어 — 6주차에 만든 것",
    "client": "붙이는 쪽 — 남이 우리를 부른다",
}


def module_name(path: Path) -> str:
    return ".".join(path.relative_to(REPO).with_suffix("").parts)


def text(node) -> str:
    return ast.unparse(node) if node is not None else ""


def params_of(node) -> list[dict]:
    a = node.args
    out: list[dict] = []
    positional = a.posonlyargs + a.args
    defaults = [None] * (len(positional) - len(a.defaults)) + list(a.defaults)
    for arg, default in zip(positional, defaults):
        out.append({"name": arg.arg, "annotation": text(arg.annotation),
                    "default": text(default)})
    if a.vararg:
        out.append({"name": "*" + a.vararg.arg, "annotation": text(a.vararg.annotation),
                    "default": ""})
    elif a.kwonlyargs:
        out.append({"name": "*", "annotation": "", "default": ""})
    for arg, default in zip(a.kwonlyargs, a.kw_defaults):
        out.append({"name": arg.arg, "annotation": text(arg.annotation),
                    "default": text(default)})
    if a.kwarg:
        out.append({"name": "**" + a.kwarg.arg, "annotation": text(a.kwarg.annotation),
                    "default": ""})
    return out


def fields_of(node: ast.ClassDef) -> list[dict]:
    out = []
    for item in node.body:
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            out.append({"name": item.target.id, "annotation": text(item.annotation),
                        "default": text(item.value)})
    return out


def signature(node) -> str:
    if isinstance(node, ast.ClassDef):
        bases = ", ".join(text(b) for b in node.bases)
        return f"class {node.name}({bases})" if bases else f"class {node.name}"
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    parts = []
    for p in params_of(node):
        piece = p["name"]
        if p["annotation"]:
            piece += f": {p['annotation']}"
        if p["default"]:
            piece += f" = {p['default']}"
        parts.append(piece)
    returns = f" -> {text(node.returns)}" if node.returns else ""
    return f"{prefix} {node.name}({', '.join(parts)}){returns}"


def decorator_kind(node) -> tuple[str, str]:
    for dec in getattr(node, "decorator_list", []):
        src = ast.unparse(dec)
        if src.startswith(("app.", "router.")):
            method = src.split("(")[0].split(".")[-1].upper()
            path = ""
            if isinstance(dec, ast.Call) and dec.args and isinstance(dec.args[0], ast.Constant):
                path = str(dec.args[0].value)
            return "route", f"{method} {path}".strip()
        if src.startswith("mcp.tool"):
            return "tool", "MCP 도구"
        if "dataclass" in src:
            return "dataclass", ""
    return "", ""


class Collector(ast.NodeVisitor):
    def __init__(self, module: str):
        self.module = module
        self.alias: dict[str, str] = {}
        self.symbols: list[dict] = []
        self.raw: list[tuple[str, str, str]] = []   # (from, target, kind)
        self.scope: list[str] = []

    def visit_Import(self, node):
        for a in node.names:
            self.alias[a.asname or a.name.split(".")[0]] = a.name

    def visit_ImportFrom(self, node):
        base = node.module or ""
        for a in node.names:
            self.alias[a.asname or a.name] = f"{base}.{a.name}" if base else a.name

    def visit_ClassDef(self, node):
        kind, extra = decorator_kind(node)
        self.add(node, kind or "class", extra, bases=[text(b) for b in node.bases],
                 fields=fields_of(node))
        self.scope.append(node.name)
        for base in node.bases:
            self.raw.append((self.here(), self.resolve(base), "inherits"))
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.visit(child)
        self.scope.pop()

    def visit_FunctionDef(self, node):
        self.function(node)

    def visit_AsyncFunctionDef(self, node):
        self.function(node)

    def function(self, node):
        kind, extra = decorator_kind(node)
        params = params_of(node)
        self.add(node, kind or ("method" if self.scope else "function"), extra,
                 params=params, returns=text(node.returns))
        self.scope.append(node.name)
        here = self.here()
        for name in identifiers(text(node.returns)):
            self.raw.append((here, name, "returns"))
        for p in params:
            for name in identifiers(p["annotation"]):
                self.raw.append((here, name, "param"))
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                target = self.resolve(child.func)
                if target:
                    self.raw.append((here, target, "call"))
        self.scope.pop()

    def here(self) -> str:
        return f"{self.module}:{'.'.join(self.scope)}"

    def add(self, node, kind, extra, **more):
        doc = ast.get_docstring(node) or ""
        self.symbols.append({
            "id": f"{self.module}:{'.'.join(self.scope + [node.name])}",
            "module": self.module, "name": node.name, "kind": kind, "extra": extra,
            "signature": signature(node), "line": node.lineno,
            "doc": doc.strip().split("\n")[0] if doc else "",
            "params": more.get("params", []), "returns": more.get("returns", ""),
            "bases": more.get("bases", []), "fields": more.get("fields", []),
        })

    def resolve(self, node) -> str:
        if isinstance(node, ast.Name):
            return self.alias.get(node.id, node.id)
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            base = self.alias.get(node.value.id, node.value.id)
            return f"{base}.{node.attr}"
        return ""


def identifiers(annotation: str) -> list[str]:
    return re.findall(r"[A-Za-z_][A-Za-z0-9_]*", annotation or "")


def main() -> None:
    files: list[Path] = []
    for target in TARGETS:
        files += sorted((REPO / target).rglob("*.py"))
    files += [REPO / f for f in EXTRA_FILES if (REPO / f).exists()]
    files = [f for f in files if "tests" not in f.parts and f.name != "__init__.py"]

    symbols: list[dict] = []
    raw: list[tuple[str, str, str]] = []
    for path in files:
        collector = Collector(module_name(path))
        collector.visit(ast.parse(path.read_text(encoding="utf-8")))
        symbols += collector.symbols
        raw += collector.raw

    index: dict[str, str] = {}
    for s in symbols:
        index[f"{s['module']}.{s['name']}"] = s["id"]
        index.setdefault(s["name"], s["id"])
    known = {s["id"] for s in symbols}
    kind_of = {s["id"]: s["kind"] for s in symbols}

    edges, seen = [], set()
    for caller, target, kind in raw:
        callee = index.get(target)
        if not callee or callee == caller or caller not in known:
            continue
        if kind == "call" and kind_of[callee] in ("class", "dataclass"):
            kind = "construct"
        key = (caller, callee, kind)
        if key in seen:
            continue
        seen.add(key)
        edges.append({"from": caller, "to": callee, "kind": kind})

    modules = [{
        "module": module_name(p), "file": str(p.relative_to(REPO)),
        "layer": LAYER.get(module_name(p).split(".")[0], "core"),
    } for p in files]

    OUT.write_text(json.dumps({
        "repo": "week08-service-lab", "layers": LAYER_LABEL,
        "modules": modules, "symbols": symbols, "edges": edges,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    from collections import Counter
    print(f"모듈 {len(modules)} · 심볼 {len(symbols)} · 관계 {len(edges)}")
    print(" ", dict(Counter(e["kind"] for e in edges)))


if __name__ == "__main__":
    main()
