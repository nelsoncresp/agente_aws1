#!/usr/bin/env python3
"""Genera el README.md actualizado basado en las herramientas de tools.py"""

import ast
import re
from pathlib import Path


def extract_tools_info(filepath="tools.py"):
    """Extrae información de las funciones decoradas con @tool."""
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    
    tree = ast.parse(source)
    tools = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            has_tool_decorator = False
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name) and decorator.id == "tool":
                    has_tool_decorator = True
                    break
            
            if not has_tool_decorator:
                continue
            
            func_name = node.name
            docstring = ast.get_docstring(node)
            
            # Extraer parámetros y sus type hints
            params = []
            for arg in node.args.args:
                param_info = {
                    "name": arg.arg,
                    "type": ast.unparse(arg.annotation) if arg.annotation else "sin tipo"
                }
                params.append(param_info)
            
            # Extraer return type hint
            return_type = ast.unparse(node.returns) if node.returns else "sin tipo"
            
            tools.append({
                "name": func_name,
                "docstring": docstring,
                "params": params,
                "return_type": return_type
            })
    
    return tools


def generate_examples(tool_name, params):
    """Genera ejemplos de preguntas para activar una herramienta."""
    examples = []
    
    if tool_name == "estimar_costo_lambda":
        examples.extend([
            "¿Cuánto costaría ejecutar 1 millón de invocaciones de Lambda con 256MB de memoria y 100ms de duración?",
            "Necesito calcular el costo mensual de mi función Lambda que se ejecuta 500k veces con 512MB y 200ms",
            "¿Cuál es el costo estimado para 10M invocaciones con 1GB de memoria?"
        ])
    elif tool_name == "recomendar_arquitectura":
        examples.extend([
            "¿Qué arquitectura recomiendas para una API REST escalable?",
            "Necesito una solución para streaming de datos en tiempo real",
            "¿Cómo estructuraría una aplicación de machine learning en AWS?",
            "Recomiéndame una arquitectura para hosting de sitio estático",
            "¿Qué patrón usar para procesamiento por lotes programado?"
        ])
    elif tool_name == "buscar_servicio_aws":
        examples.extend([
            "¿Qué servicios de AWS existen para compute?",
            "Lista los servicios de storage disponibles",
            "¿Qué opciones hay para bases de datos NoSQL?",
            "¿Qué herramientas de AWS ofrece para machine learning?",
            "Necesito información sobre servicios de networking"
        ])
    elif tool_name == "comparar_instancias_ec2":
        examples.extend([
            "Compara t3.micro con t3.small",
            "¿Cuál es la diferencia entre m5.large y c5.large?",
            "¿Cuánto cuesta más una t3.large vs t3.medium?",
            "Compara dos instancias EC2 para mí"
        ])
    elif tool_name == "calculator":
        examples.extend([
            "Calcula 1234 * 5678",
            "¿Cuánto es 256 dividido entre 16?",
            "Suma 1500 + 2300 + 3200"
        ])
    elif tool_name == "current_time":
        examples.extend([
            "¿Qué hora es ahora?",
            "Dime la fecha y hora actual",
            "¿Cuándo es la fecha actual?"
        ])
    
    return examples


def generate_readme():
    """Genera el contenido completo del README.md."""
    tools = extract_tools_info()
    
    # Sección 1: Introducción y requisitos
    intro = """# CloudArquitecto - AWS Agent

Este proyecto implementa un agente inteligente experto en AWS utilizando **Strands Agents**.

## Requisitos

- Python 3.9+
- Credenciales de AWS (Bedrock habilitado)
- Virtual Environment (recomendado)

## Instalación

1. Clona el repositorio.
2. Crea e instala las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: .\\venv\\Scripts\\activate
   pip install -r requirements.txt
   ```
3. Configura tu `.env` basándote en `.env.example`.

## Uso

### Versión oficial
Para ejecutar el agente conectado a AWS Bedrock:
```bash
python agent.py
```

### Versión Demo (Evidencia)
Si tienes problemas de cuota o throttling con Bedrock, usa la versión demo para pruebas locales rápidas:
```bash
python agent_demo.py
```

## Herramientas disponibles

"""
    
    # Sección 2: Lista de herramientas con descripciones
    tools_section = ""
    for tool in tools:
        docstring = tool["docstring"] or "Sin descripción disponible"
        # Extraer solo la primera línea del docstring como descripción breve
        brief_desc = docstring.split("\n")[0] if docstring else "Sin descripción"
        
        tools_section += f"### {tool['name']}\n"
        tools_section += f"{brief_desc}\n\n"
        tools_section += f"**Parámetros:**\n"
        for param in tool["params"]:
            tools_section += f"- `{param['name']}` ({param['type']})\n"
        tools_section += f"\n**Retorna:** `{tool['return_type']}`\n\n"
    
    # Sección 3: Ejemplos de preguntas por herramienta
    examples_section = "## Ejemplos de preguntas\n\n"
    examples_section += "Puedes usar las siguientes preguntas para activar cada herramienta:\n\n"
    
    for tool in tools:
        examples = generate_examples(tool["name"], tool["params"])
        examples_section += f"### {tool['name']}\n"
        for i, example in enumerate(examples, 1):
            examples_section += f"{i}. {example}\n"
        examples_section += "\n"
    
    # Sección 4: Instrucciones adicionales
    instructions = """## Configuración de AWS

Asegúrate de tener configuradas tus credenciales de AWS antes de ejecutar el agente:

```bash
aws configure
```

O configura las variables de entorno:
```bash
export AWS_ACCESS_KEY_ID=tu_access_key
export AWS_SECRET_ACCESS_KEY=tu_secret_key
export AWS_DEFAULT_REGION=us-west-2
```

## Solución de problemas

- **Error de cuota (ThrottlingException):** El agente intenta automáticamente con modelos alternativos.
- **Problemas de conexión:** Verifica tus credenciales de AWS y que Bedrock esté habilitado en tu región.
- **Modo debug:** Ejecuta `python agent.py` y usa el comando `debug on` para ver información detallada.

"""

    return intro + tools_section + examples_section + instructions


if __name__ == "__main__":
    readme_content = generate_readme()
    Path("README.md").write_text(readme_content, encoding="utf-8")
    print("✓ README.md actualizado correctamente")
