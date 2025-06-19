# different context extraction strategies
import ast
import re


def extract_content(content: str, language: str, strategy: str = "trimmed") -> str:
    if language == "Python":
        return {
            "trimmed": _python_trimmed,
            "declarations": _python_declarations,
            "docstrings": _python_docstrings_only,
        }.get(strategy, _python_trimmed)(content)
    return content if strategy == "raw" else _default_trim(content)

def _python_trimmed(content: str) -> str:
    return "\n".join(
        line for line in content.splitlines()
        if line.strip() and not line.strip().startswith("#")
    )[:30000]

def _python_declarations(content: str) -> str:
    try:
        tree = ast.parse(content)
        return "\n".join(
            _ast_node_signature(n) for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Assign))
        )
    except Exception:
        return ""

def _ast_node_signature(node):
    if isinstance(node, ast.FunctionDef):
        return f"def {node.name}({', '.join(arg.arg for arg in node.args.args)}):"
    elif isinstance(node, ast.ClassDef):
        return f"class {node.name}:"
    elif isinstance(node, ast.Assign):
        return ", ".join(t.id for t in node.targets if isinstance(t, ast.Name))
    return ""

def _python_docstrings_only(content: str) -> str:
    try:
        tree = ast.parse(content)
        return ast.get_docstring(tree) or ""
    except Exception:
        return ""

def _default_trim(content: str) -> str:
    return "\n".join(content.strip().splitlines()[:300])
