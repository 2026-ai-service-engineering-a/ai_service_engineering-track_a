#!/usr/bin/env python3
"""week08-service-lab의 심볼과 호출 관계를 뽑아 `<CodeMap />`의 데이터로 만든다.

손으로 적은 그림이 아니라 **실제 코드를 파싱한 결과**다. 저장소가 바뀌면
다시 돌린다.

    python3 scripts/build-week08-codemap.py [저장소 경로]

읽는 것: core/ · api/ · mcp_server/ · clients/py_client.py
쓰는 것: site/src/data/week08-codemap.json
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

REPO = Path(sys.argv[1] if len(sys.argv) > 1
            else "../week08-service-lab").resolve()
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
    rel = path.relative_to(REPO).with_suffix("")
    return ".".join(rel.parts)


def signature(node: ast.AST) -> str:
    if isinstance(node, ast.ClassDef):
        return f"class {node.name}"
    args = []
    a = node.args
    for arg in a.posonlyargs + a.args:
        args.append(arg.arg)
    if a.vararg:
        args.append("*" + a.vararg.arg)
    if a.kwonlyargs and not a.vararg:
        args.append("*")
    for arg in a.kwonlyargs:
        args.append(arg.arg)
    if a.kwarg:
        args.append("**" + a.kwarg.arg)
    returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    return f"{prefix} {node.name}({', '.join(args)}){returns}"


def decorator_kind(node: ast.AST) -> tuple[str, str]:
    """(kind, 부가 설명) — 라우트·도구·데이터클래스를 구분한다."""
    for dec in getattr(node, "decorator_list", []):
        text = ast.unparse(dec)
        if text.startswith("app.") or text.startswith("router."):
            method = text.split("(")[0].split(".")[-1].upper()
            path = ""
            if isinstance(dec, ast.Call) and dec.args:
                first = dec.args[0]
                if isinstance(first, ast.Constant):
                    path = str(first.value)
            return "route", f"{method} {path}".strip()
        if text.startswith("mcp.tool"):
            return "tool", "MCP 도구"
        if "dataclass" in text:
            return "dataclass", ""
    return "", ""


class Collector(ast.NodeVisitor):
    """모듈 하나에서 심볼과 호출을 모은다."""

    def __init__(self, module: str, source: str):
        self.module = module
        self.source = source
        self.alias: dict[str, str] = {}     # 지역 이름 → 정규화된 경로
        self.symbols: list[dict] = []
        self.edges: list[tuple[str, str]] = []
        self.scope: list[str] = []

    # ── import 해석 ──────────────────────────────────────────
    def visit_Import(self, node: ast.Import) -> None:
        for a in node.names:
            self.alias[a.asname or a.name.split(".")[0]] = a.name

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        base = node.module or ""
        for a in node.names:
            local = a.asname or a.name
            self.alias[local] = f"{base}.{a.name}" if base else a.name

    # ── 심볼 수집 ────────────────────────────────────────────
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        kind, extra = decorator_kind(node)
        self.add(node, kind or "class", extra)
        self.scope.append(node.name)
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.visit(child)
        self.scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.function(node)

    def function(self, node) -> None:
        kind, extra = decorator_kind(node)
        self.add(node, kind or ("method" if self.scope else "function"), extra)
        self.scope.append(node.name)
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                target = self.resolve(child.func)
                if target:
                    self.edges.append((self.qualified(), target))
        self.scope.pop()

    def qualified(self) -> str:
        return f"{self.module}:{'.'.join(self.scope)}"

    def add(self, node, kind: str, extra: str) -> None:
        doc = ast.get_docstring(node) or ""
        self.symbols.append({
            "id": f"{self.module}:{'.'.join(self.scope + [node.name])}",
            "module": self.module,
            "name": node.name,
            "kind": kind,
            "extra": extra,
            "signature": signature(node),
            "line": node.lineno,
            "doc": doc.strip().split("\n")[0] if doc else "",
        })

    # ── 호출 대상 해석 ───────────────────────────────────────
    def resolve(self, func: ast.AST) -> str:
        if isinstance(func, ast.Name):
            return self.alias.get(func.id, "") or f"?{func.id}"
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            base = self.alias.get(func.value.id, func.value.id)
            return f"{base}.{func.attr}"
        return ""


def main() -> None:
    files: list[Path] = []
    for target in TARGETS:
        files += sorted((REPO / target).rglob("*.py"))
    for extra in EXTRA_FILES:
        if (REPO / extra).exists():
            files.append(REPO / extra)
    files = [f for f in files if "tests" not in f.parts and f.name != "__init__.py"]

    symbols: list[dict] = []
    raw_edges: list[tuple[str, str]] = []
    for path in files:
        module = module_name(path)
        source = path.read_text(encoding="utf-8")
        collector = Collector(module, source)
        collector.visit(ast.parse(source))
        symbols += collector.symbols
        raw_edges += collector.edges

    # 정규화된 경로 → 심볼 id
    index: dict[str, str] = {}
    for s in symbols:
        index[f"{s['module']}.{s['name']}"] = s["id"]
        index.setdefault(s["name"], s["id"])

    edges = []
    seen = set()
    for caller, target in raw_edges:
        callee = index.get(target) or index.get(target.lstrip("?"))
        if not callee or callee == caller:
            continue
        if not any(s["id"] == caller for s in symbols):
            continue
        if (caller, callee) in seen:
            continue
        seen.add((caller, callee))
        edges.append({"from": caller, "to": callee})

    modules = []
    for path in files:
        module = module_name(path)
        top = module.split(".")[0]
        modules.append({
            "module": module,
            "file": str(path.relative_to(REPO)),
            "layer": LAYER.get(top, "core"),
        })

    OUT.write_text(json.dumps({
        "repo": "week08-service-lab",
        "layers": LAYER_LABEL,
        "modules": modules,
        "symbols": symbols,
        "edges": edges,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"모듈 {len(modules)} · 심볼 {len(symbols)} · 호출 {len(edges)}")
    print(f"→ {OUT.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
