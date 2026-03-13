from strands import tool


@tool
def estimar_costo_lambda(invocaciones: int, duracion_ms: int, memoria_mb: int) -> dict:
    """
    Calcula el costo mensual estimado de AWS Lambda.
    
    Args:
        invocaciones: Número de invocaciones mensuales
        duracion_ms: Duración promedio de cada invocación en milisegundos
        memoria_mb: Memoria asignada en MB
    
    Returns:
        Diccionario con el desglose de costos
    """
    # Precios AWS Lambda (us-east-1, 2024)
    precio_por_invocacion = 0.0000002  # $0.20 por millón
    precio_por_gb_segundo = 0.0000166667  # $0.0000166667 por GB-segundo
    
    # Cálculo
    costo_invocaciones = invocaciones * precio_por_invocacion
    gb_memoria = memoria_mb / 1024
    segundos_compute = (duracion_ms / 1000) * invocaciones
    costo_compute = gb_memoria * segundos_compute * precio_por_gb_segundo
    costo_total = costo_invocaciones + costo_compute
    
    return {
        "invocaciones_mensuales": invocaciones,
        "duracion_ms": duracion_ms,
        "memoria_mb": memoria_mb,
        "costo_invocaciones_usd": round(costo_invocaciones, 4),
        "costo_compute_usd": round(costo_compute, 4),
        "costo_total_mensual_usd": round(costo_total, 2)
    }


@tool
def recomendar_arquitectura(caso_uso: str) -> dict:
    """
    Recomienda una arquitectura AWS según el caso de uso.
    
    Args:
        caso_uso: Tipo de aplicación (api_rest, streaming, ml_inference, static_web, batch)
    
    Returns:
        Diccionario con la arquitectura recomendada
    """
    arquitecturas = {
        "api_rest": {
            "servicios": ["API Gateway", "Lambda", "DynamoDB", "CloudWatch"],
            "descripcion": "API serverless escalable con baja latencia",
            "patron": "API Gateway -> Lambda -> DynamoDB"
        },
        "streaming": {
            "servicios": ["Kinesis Data Streams", "Lambda", "S3", "Kinesis Firehose"],
            "descripcion": "Procesamiento de datos en tiempo real",
            "patron": "Kinesis Streams -> Lambda -> S3/Firehose"
        },
        "ml_inference": {
            "servicios": ["SageMaker", "Lambda", "API Gateway", "S3"],
            "descripcion": "Inferencia de modelos ML con endpoints escalables",
            "patron": "API Gateway -> Lambda -> SageMaker Endpoint"
        },
        "static_web": {
            "servicios": ["S3", "CloudFront", "Route 53", "Certificate Manager"],
            "descripcion": "Hosting de sitio estático con CDN global",
            "patron": "S3 -> CloudFront -> Route 53"
        },
        "batch": {
            "servicios": ["EventBridge", "Lambda", "Step Functions", "S3"],
            "descripcion": "Procesamiento por lotes programado",
            "patron": "EventBridge -> Step Functions -> Lambda -> S3"
        }
    }
    
    if caso_uso not in arquitecturas:
        return {
            "error": f"Caso de uso '{caso_uso}' no reconocido",
            "casos_validos": list(arquitecturas.keys())
        }
    
    return {
        "caso_uso": caso_uso,
        **arquitecturas[caso_uso]
    }


@tool
def buscar_servicio_aws(categoria: str) -> dict:
    """
    Lista servicios AWS por categoría.
    
    Args:
        categoria: Categoría de servicios (compute, storage, database, ai, networking)
    
    Returns:
        Diccionario con servicios de la categoría
    """
    servicios = {
        "compute": [
            {"nombre": "Lambda", "descripcion": "Funciones serverless"},
            {"nombre": "EC2", "descripcion": "Servidores virtuales"},
            {"nombre": "ECS", "descripcion": "Contenedores Docker"},
            {"nombre": "Fargate", "descripcion": "Contenedores serverless"}
        ],
        "storage": [
            {"nombre": "S3", "descripcion": "Object storage"},
            {"nombre": "EBS", "descripcion": "Block storage para EC2"},
            {"nombre": "EFS", "descripcion": "File storage compartido"},
            {"nombre": "Glacier", "descripcion": "Archivado de largo plazo"}
        ],
        "database": [
            {"nombre": "DynamoDB", "descripcion": "NoSQL serverless"},
            {"nombre": "RDS", "descripcion": "Bases de datos relacionales"},
            {"nombre": "Aurora", "descripcion": "MySQL/PostgreSQL optimizado"},
            {"nombre": "DocumentDB", "descripcion": "Compatible con MongoDB"}
        ],
        "ai": [
            {"nombre": "SageMaker", "descripcion": "Machine learning end-to-end"},
            {"nombre": "Bedrock", "descripcion": "Modelos fundacionales (LLMs)"},
            {"nombre": "Rekognition", "descripcion": "Análisis de imágenes/video"},
            {"nombre": "Comprehend", "descripcion": "Procesamiento de lenguaje natural"}
        ],
        "networking": [
            {"nombre": "VPC", "descripcion": "Red virtual privada"},
            {"nombre": "CloudFront", "descripcion": "CDN global"},
            {"nombre": "Route 53", "descripcion": "DNS y registro de dominios"},
            {"nombre": "API Gateway", "descripcion": "Gestión de APIs"}
        ]
    }
    
    if categoria not in servicios:
        return {
            "error": f"Categoría '{categoria}' no reconocida",
            "categorias_validas": list(servicios.keys())
        }
    
    return {
        "categoria": categoria,
        "servicios": servicios[categoria],
        "total": len(servicios[categoria])
    }


@tool
def comparar_instancias_ec2(instancia1: str, instancia2: str) -> dict:
    """
    Compara dos tipos de instancias EC2 mostrando sus características principales.
    
    Args:
        instancia1: Tipo de instancia EC2 (ej: t3.micro, t3.small)
        instancia2: Tipo de instancia EC2 para comparar
    
    Returns:
        Diccionario con la comparación de características
    """
    # Base de datos simplificada de instancias EC2
    instancias = {
        "t3.micro": {"vcpus": 2, "ram_gb": 1, "precio_hora_usd": 0.0104},
        "t3.small": {"vcpus": 2, "ram_gb": 2, "precio_hora_usd": 0.0208},
        "t3.medium": {"vcpus": 2, "ram_gb": 4, "precio_hora_usd": 0.0416},
        "t3.large": {"vcpus": 2, "ram_gb": 8, "precio_hora_usd": 0.0832},
        "t3.xlarge": {"vcpus": 4, "ram_gb": 16, "precio_hora_usd": 0.1664},
        "m5.large": {"vcpus": 2, "ram_gb": 8, "precio_hora_usd": 0.096},
        "m5.xlarge": {"vcpus": 4, "ram_gb": 16, "precio_hora_usd": 0.192},
        "c5.large": {"vcpus": 2, "ram_gb": 4, "precio_hora_usd": 0.085},
        "c5.xlarge": {"vcpus": 4, "ram_gb": 8, "precio_hora_usd": 0.17},
        "r5.large": {"vcpus": 2, "ram_gb": 16, "precio_hora_usd": 0.126},
    }
    
    if instancia1 not in instancias:
        return {
            "error": f"Instancia '{instancia1}' no encontrada",
            "instancias_disponibles": list(instancias.keys())
        }
    
    if instancia2 not in instancias:
        return {
            "error": f"Instancia '{instancia2}' no encontrada",
            "instancias_disponibles": list(instancias.keys())
        }
    
    info1 = instancias[instancia1]
    info2 = instancias[instancia2]
    
    return {
        "comparacion": {
            instancia1: {
                "vcpus": info1["vcpus"],
                "ram_gb": info1["ram_gb"],
                "precio_hora_usd": info1["precio_hora_usd"],
                "precio_mensual_usd": round(info1["precio_hora_usd"] * 730, 2)
            },
            instancia2: {
                "vcpus": info2["vcpus"],
                "ram_gb": info2["ram_gb"],
                "precio_hora_usd": info2["precio_hora_usd"],
                "precio_mensual_usd": round(info2["precio_hora_usd"] * 730, 2)
            }
        },
        "diferencias": {
            "vcpus": info2["vcpus"] - info1["vcpus"],
            "ram_gb": info2["ram_gb"] - info1["ram_gb"],
            "precio_hora_usd": round(info2["precio_hora_usd"] - info1["precio_hora_usd"], 4),
            "precio_mensual_usd": round((info2["precio_hora_usd"] - info1["precio_hora_usd"]) * 730, 2)
        }
    }
