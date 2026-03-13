#!/usr/bin/env python3
"""Valida que las funciones decoradas con @tool en tools.py tengan docstrings y type hints completos."""

import ast
import sys


def validate_tools_file(filepath="tools.py"):
    """Valida el archivo tools.py."""
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    
    tree = ast.parse(source)
    issues = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Verificar si tiene el decorador @tool
            has_tool_decorator = False
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name) and decorator.id == "tool":
                    has_tool_decorator = True
                    break
            
            if not has_tool_decorator:
                continue
            
            func_name = node.name
            
            # Verificar docstring
            if not (ast.get_docstring(node) or 
                    (node.body and isinstance(node.body[0], ast.Expr) and 
                     isinstance(node.body[0].value, (ast.Str, ast.Constant)))): 
                issues.append(f"{func_name}: FALTA docstring con descripción clara")
            
            # Verificar type hints en parámetros
            for arg in node.args.args:
                if arg.annotation is None:
                    issues.append(f"{func_name}: FALTA type hint en parámetro '{arg.arg}'")
            
            # Verificar type hint de retorno
            if node.returns is None:
                issues.append(f"{func_name}: FALTA type hint en valor de retorno")
    
    if issues:
        print("=== ADVERTENCIAS EN tools.py ===")
        for issue in issues:
            print(f"⚠️  {issue}")
        print(f"\nTotal: {len(issues)} problema(s) encontrado(s)")
        return 1
    else:
        print("✓ tools.py: Todas las funciones @tool tienen docstring y type hints completos")
        return 0


if __name__ == "__main__":
    sys.exit(validate_tools_file())
