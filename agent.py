from strands import Agent
from strands_tools import calculator, current_time
from tools import estimar_costo_lambda, recomendar_arquitectura, buscar_servicio_aws, comparar_instancias_ec2
import json
from datetime import datetime
from pathlib import Path
import time

SYSTEM_PROMPT = """
Eres CloudArquitecto, un experto en Amazon Web Services.
Cuentas con las siguientes herramientas para ayudar al usuario:
1. estimar_costo_lambda: Para calcular costos mensuales de funciones serverless.
2. recomendar_arquitectura: Para sugerir patrones de AWS segun el caso de uso.
3. buscar_servicio_aws: Para listar servicios por categorias tecnicas.
4. comparar_instancias_ec2: Para comparar dos tipos de instancias EC2.
5. calculator: Para realizar calculos matematicos precisos.
6. current_time: Para conocer la fecha y hora actual.

Respondes de forma concisa y practica, siempre en espanol. Cuando usas una herramienta, explicas brevemente el resultado.
"""

HISTORIAL_FILE = "historial.json"
DEBUG_MODE = False

# Lista de modelos para fallback (si uno falla por cuota, se intenta el siguiente)
MODELOS = [
    "anthropic.claude-3-haiku-20240307-v1:0",
    "amazon.titan-text-premier-v1:0",
    "anthropic.claude-3-5-haiku-20241022-v1:0"
]

TOOLS = [
    estimar_costo_lambda,
    recomendar_arquitectura,
    buscar_servicio_aws,
    comparar_instancias_ec2,
    calculator,
    current_time
]


def cargar_historial():
    """Carga el historial desde el archivo JSON."""
    if Path(HISTORIAL_FILE).exists():
        with open(HISTORIAL_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def guardar_historial(historial):
    """Guarda el historial en el archivo JSON."""
    with open(HISTORIAL_FILE, 'w', encoding='utf-8') as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)


def agregar_entrada(historial, pregunta, respuesta):
    """Agrega una nueva entrada al historial."""
    entrada = {
        "timestamp": datetime.now().isoformat(),
        "pregunta": pregunta,
        "respuesta": respuesta
    }
    historial.append(entrada)
    guardar_historial(historial)


def mostrar_resumen_historial(historial):
    """Muestra un resumen del historial existente."""
    if not historial:
        print("No hay historial previo.\n")
        return
    
    print(f"Historial cargado: {len(historial)} conversaciones previas")
    if len(historial) > 0:
        ultima = historial[-1]
        print(f"Última conversación: {ultima['timestamp']}")
    print()

def obtener_respuesta(user_input):
    """Intenta obtener respuesta de la IA probando diferentes modelos si hay errores de cuota."""
    global DEBUG_MODE
    debug_info = []
    tool_calls = []
    
    for model_id in MODELOS:
        try:
            # Creamos el agente con el modelo actual
            agent = Agent(
                model=model_id,
                system_prompt=SYSTEM_PROMPT,
                tools=TOOLS
            )
            
            inicio = time.time()
            result = agent(user_input)
            tiempo_total = time.time() - inicio
            
            if DEBUG_MODE:
                debug_info.append({
                    "tiempo_total_segundos": round(tiempo_total, 3),
                    "modelo_usado": model_id,
                    "tool_calls": tool_calls
                })
            
            return result, debug_info if DEBUG_MODE else None
        except Exception as e:
            # Si es un error de cuota/throttling, probamos el siguiente modelo
            if "ThrottlingException" in str(e) or "Too many tokens" in str(e):
                continue
            else:
                raise e
    raise Exception("Todos los modelos de IA estan fuera de cuota.")

if __name__ == "__main__":
    historial = cargar_historial()
    
    print("=== CloudArquitecto listo (Modo IA) ===")
    mostrar_resumen_historial(historial)
    print("Comandos especiales: 'debug on', 'debug off', 'salir'")
    print()

    while True:
        user_input = input("Nelson: ").strip()
        
        if not user_input:
            continue
        
        # Comandos especiales
        if user_input.lower() == "debug on":
            DEBUG_MODE = True
            print("\n[Modo debug activado]\n")
            continue
        
        if user_input.lower() == "debug off":
            DEBUG_MODE = False
            print("\n[Modo debug desactivado]\n")
            continue
            
        if user_input.lower() == "salir":
            print("Hasta luego!")
            break
        
        print("\nagent: ", end="", flush=True)
        try:
            result, debug_info = obtener_respuesta(user_input)
            print(result)
            
            if DEBUG_MODE and debug_info:
                print("\n--- DEBUG INFO ---")
                for info in debug_info:
                    print(f"Modelo: {info['modelo_usado']}")
                    print(f"Tiempo total: {info['tiempo_total_segundos']}s")
                print("------------------")
            
            agregar_entrada(historial, user_input, result)
        except Exception as e:
            print(f"\n[Error]: {e}")
            print("Pista: Prueba 'python agent_demo.py' si necesitas una respuesta inmediata ahora mismo.")
        print("\n")
