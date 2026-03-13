#!/usr/bin/env python3
"""Genera test_agent.py con pruebas unitarias para las herramientas."""

import ast
import re


def extract_tools_info(filepath="tools.py"):
    """Extrae información de las herramientas del archivo tools.py."""
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    
    tree = ast.parse(source)
    tools_info = []
    
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
            params = []
            
            for arg in node.args.args:
                param_name = arg.arg
                param_type = "Any"
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        param_type = arg.annotation.id
                    elif isinstance(arg.annotation, ast.Constant):
                        param_type = arg.annotation.value
                params.append({"name": param_name, "type": param_type})
            
            return_type = "Any"
            if node.returns:
                if isinstance(node.returns, ast.Name):
                    return_type = node.returns.id
                elif isinstance(node.returns, ast.Constant):
                    return_type = node.returns.value
            
            tools_info.append({
                "name": func_name,
                "params": params,
                "return_type": return_type
            })
    
    return tools_info


def generate_tests(tools_info):
    """Genera el contenido del archivo de pruebas."""
    imports = '''import pytest
from tools import (
    estimar_costo_lambda,
    recomendar_arquitectura,
    buscar_servicio_aws,
    comparar_instancias_ec2
)
'''
    
    test_functions = []
    
    for tool in tools_info:
        func_name = tool["name"]
        params = tool["params"]
        return_type = tool["return_type"]
        
        # Generar test para valores válidos
        valid_test = f'''
def test_{func_name}_valid_input():
    """Prueba {func_name} con entradas válidas."""
    '''
        
        if params:
            param_values = []
            for p in params:
                if p["name"] == "instancia1" or p["name"] == "instancia2":
                    param_values.append(f'"{p["name"]}"')
                elif p["name"] == "caso_uso":
                    param_values.append('"api_rest"')
                elif p["name"] == "categoria":
                    param_values.append('"compute"')
                elif p["name"] == "invocaciones":
                    param_values.append("1000")
                elif p["name"] == "duracion_ms":
                    param_values.append("100")
                elif p["name"] == "memoria_mb":
                    param_values.append("256")
                else:
                    param_values.append(f'"{p["name"]}"')
            
            valid_test += f"    result = {func_name}({', '.join(param_values)})\n"
        else:
            valid_test += f"    result = {func_name}()\n"
        
        valid_test += f'''    assert result is not None
    assert isinstance(result, dict)
'''
        
        # Generar test para valores inválidos
        invalid_test = f'''
def test_{func_name}_invalid_input():
    """Prueba {func_name} con entradas inválidas."""
    '''
        
        if func_name == "comparar_instancias_ec2":
            invalid_test += f'''    with pytest.raises(Exception):
        {func_name}("instancia_invalida", "t3.micro")
'''
        elif func_name == "recomendar_arquitectura":
            invalid_test += f'''    result = {func_name}("caso_invalido")
    assert "error" in result
'''
        elif func_name == "buscar_servicio_aws":
            invalid_test += f'''    result = {func_name}("categoria_invalida")
    assert "error" in result
'''
        else:
            invalid_test += f'''    # Prueba con valores negativos (si aplica)
    try:
        result = {func_name}(-1, -1, -1)
    except:
        pass  # Se espera que falle o maneje el error
'''
        
        test_functions.append(valid_test)
        test_functions.append(invalid_test)
    
    return imports + "\n".join(test_functions)


def main():
    """Genera el archivo test_agent.py."""
    tools_info = extract_tools_info()
    tests_content = generate_tests(tools_info)
    
    with open("test_agent.py", "w", encoding="utf-8") as f:
        f.write(tests_content)
    
    print(f"✓ test_agent.py generado con {len(tools_info)} herramientas")
    for tool in tools_info:
        print(f"  - {tool['name']}")


if __name__ == "__main__":
    main()
