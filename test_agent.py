import pytest
from tools import (
    estimar_costo_lambda,
    recomendar_arquitectura,
    buscar_servicio_aws,
    comparar_instancias_ec2
)

def test_estimar_costo_lambda_valid_input():
    """Prueba estimar_costo_lambda con entradas válidas."""
        result = estimar_costo_lambda(1000, 100, 256)
    assert result is not None
    assert isinstance(result, dict)


def test_estimar_costo_lambda_invalid_input():
    """Prueba estimar_costo_lambda con entradas inválidas."""
        # Prueba con valores negativos (si aplica)
    try:
        result = estimar_costo_lambda(-1, -1, -1)
    except:
        pass  # Se espera que falle o maneje el error


def test_recomendar_arquitectura_valid_input():
    """Prueba recomendar_arquitectura con entradas válidas."""
        result = recomendar_arquitectura("api_rest")
    assert result is not None
    assert isinstance(result, dict)


def test_recomendar_arquitectura_invalid_input():
    """Prueba recomendar_arquitectura con entradas inválidas."""
        result = recomendar_arquitectura("caso_invalido")
    assert "error" in result


def test_buscar_servicio_aws_valid_input():
    """Prueba buscar_servicio_aws con entradas válidas."""
        result = buscar_servicio_aws("compute")
    assert result is not None
    assert isinstance(result, dict)


def test_buscar_servicio_aws_invalid_input():
    """Prueba buscar_servicio_aws con entradas inválidas."""
        result = buscar_servicio_aws("categoria_invalida")
    assert "error" in result


def test_comparar_instancias_ec2_valid_input():
    """Prueba comparar_instancias_ec2 con entradas válidas."""
        result = comparar_instancias_ec2("instancia1", "instancia2")
    assert result is not None
    assert isinstance(result, dict)


def test_comparar_instancias_ec2_invalid_input():
    """Prueba comparar_instancias_ec2 con entradas inválidas."""
        with pytest.raises(Exception):
        comparar_instancias_ec2("instancia_invalida", "t3.micro")
