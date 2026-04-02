"""Code execution tool (sandboxed)."""
import ast

CODE_DEFINITION = {"type": "object", "properties": {"code": {"type": "string", "description": "Python code to execute"}, "language": {"type": "string", "default": "python"}}, "required": ["code"]}

def execute_code(code: str, language: str = "python") -> dict:
    if language != "python": return {"error": f"Unsupported language: {language}"}
    try:
        tree = ast.parse(code)
        # Only allow expressions and simple statements
        result = eval(compile(ast.Expression(body=tree.body[-1].value) if isinstance(tree.body[-1], ast.Expr) else ast.parse("None", mode="eval"), "<agent>", "eval"), {"__builtins__": {"len": len, "sum": sum, "min": min, "max": max, "sorted": sorted, "range": range, "list": list, "dict": dict, "str": str, "int": int, "float": float, "abs": abs, "round": round}})
        return {"output": str(result), "language": language}
    except Exception as e:
        return {"error": str(e)}
