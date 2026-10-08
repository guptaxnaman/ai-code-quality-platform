import ast

BRANCH_NODES = (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.IfExp, ast.comprehension)

def _line_count(tree):
    lines = [getattr(node, "lineno", 0) for node in ast.walk(tree)]
    return max(lines) if lines else 0

def _function_lengths(tree):
    results = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end = getattr(node, "end_lineno", node.lineno)
            results.append((node.name, end - node.lineno + 1))
    return results

def analyze_code(code: str):
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Code cannot be empty.")
    if len(code) > 50000:
        raise ValueError("Please keep the submitted code under 50,000 characters.")
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return {
            "score": 0, "complexity": 0, "lines": 0, "functions": 0,
            "issues": [{"severity": "high", "title": "Syntax error", "detail": f"Line {exc.lineno or '?'}: {exc.msg}"}],
            "suggestions": ["Fix the syntax error first, then run the analysis again."],
        }

    issues, suggestions = [], []
    complexity = 1 + sum(isinstance(node, BRANCH_NODES) for node in ast.walk(tree))
    lines = _line_count(tree)
    functions = sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree))

    for name, length in _function_lengths(tree):
        if length > 40:
            issues.append({"severity": "medium", "title": "Long function", "detail": f"'{name}' is about {length} lines long."})
            suggestions.append(f"Consider splitting '{name}' into smaller functions with one clear responsibility.")

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append({"severity": "medium", "title": "Broad exception handling", "detail": "A bare except block can hide unexpected failures."})
            suggestions.append("Catch specific exception types and handle only expected failure cases.")
        if isinstance(node, ast.Global):
            issues.append({"severity": "low", "title": "Global state", "detail": "The function modifies module-level state."})
            suggestions.append("Prefer passing state explicitly or encapsulating it in a class.")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
            issues.append({"severity": "high", "title": "Use of eval()", "detail": "Dynamic evaluation can execute unintended code."})
            suggestions.append("Avoid eval() for untrusted or dynamic input; use explicit parsing instead.")

    if complexity > 10:
        issues.append({"severity": "medium", "title": "High branching complexity", "detail": f"Estimated complexity is {complexity}."})
        suggestions.append("Reduce nested branching where possible and extract independent logic.")
    if lines > 300:
        issues.append({"severity": "low", "title": "Large source file", "detail": f"The analyzed code is about {lines} lines."})
        suggestions.append("Consider separating unrelated responsibilities into smaller modules.")
    if not issues:
        suggestions.append("No major rule-based issues were detected. Add tests around important behavior and edge cases.")

    penalty = sum(25 if i["severity"] == "high" else 12 if i["severity"] == "medium" else 5 for i in issues)
    return {
        "score": max(0, min(100, 100 - penalty)),
        "complexity": complexity,
        "lines": lines,
        "functions": functions,
        "issues": issues,
        "suggestions": list(dict.fromkeys(suggestions))[:8],
    }
