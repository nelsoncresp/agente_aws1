# CloudArquitecto - AWS Agent

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
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Configura tu `.env` basándote en `.env.example`.

## Uso

### Versión oficial
Para ejecutar el agente conectado a AWS Bedrock:
```bash
python agent.py
```
## Herramientas disponibles

### estimar_costo_lambda
Calcula el costo mensual estimado de AWS Lambda.

**Parámetros:**
- `invocaciones` (int)
- `duracion_ms` (int)
- `memoria_mb` (int)

**Retorna:** `dict`

### recomendar_arquitectura
Recomienda una arquitectura AWS según el caso de uso.

**Parámetros:**
- `caso_uso` (str)

**Retorna:** `dict`

### buscar_servicio_aws
Lista servicios AWS por categoría.

**Parámetros:**
- `categoria` (str)

**Retorna:** `dict`

### comparar_instancias_ec2
Compara dos tipos de instancias EC2 mostrando sus características principales.

**Parámetros:**
- `instancia1` (str)
- `instancia2` (str)

**Retorna:** `dict`

## Ejemplos de preguntas

Puedes usar las siguientes preguntas para activar cada herramienta:

### estimar_costo_lambda
1. ¿Cuánto costaría ejecutar 1 millón de invocaciones de Lambda con 256MB de memoria y 100ms de duración?
2. Necesito calcular el costo mensual de mi función Lambda que se ejecuta 500k veces con 512MB y 200ms
3. ¿Cuál es el costo estimado para 10M invocaciones con 1GB de memoria?

### recomendar_arquitectura
1. ¿Qué arquitectura recomiendas para una API REST escalable?
2. Necesito una solución para streaming de datos en tiempo real
3. ¿Cómo estructuraría una aplicación de machine learning en AWS?
4. Recomiéndame una arquitectura para hosting de sitio estático
5. ¿Qué patrón usar para procesamiento por lotes programado?

### buscar_servicio_aws
1. ¿Qué servicios de AWS existen para compute?
2. Lista los servicios de storage disponibles
3. ¿Qué opciones hay para bases de datos NoSQL?
4. ¿Qué herramientas de AWS ofrece para machine learning?
5. Necesito información sobre servicios de networking

### comparar_instancias_ec2
1. Compara t3.micro con t3.small
2. ¿Cuál es la diferencia entre m5.large y c5.large?
3. ¿Cuánto cuesta más una t3.large vs t3.medium?
4. Compara dos instancias EC2 para mí

## Configuración de AWS

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

