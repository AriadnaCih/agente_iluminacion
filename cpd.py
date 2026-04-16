import random

# =========================
# TABLA CPD
# =========================
import random

cpd = {
    ("Si", "Baja", "Nocturna"): {
        "Encender": 0.9,
        "Ajustar": 0.1,
        "Apagar": 0.0
    },
    ("Si", "Baja", "Diurna"): {
        "Encender": 0.7,
        "Ajustar": 0.2,
        "Apagar": 0.1
    },
    ("Si", "Media", "Nocturna"): {
        "Encender": 0.4,
        "Ajustar": 0.5,
        "Apagar": 0.1
    },
    ("Si", "Media", "Diurna"): {
        "Encender": 0.2,
        "Ajustar": 0.6,
        "Apagar": 0.2
    },
    ("No", "Alta", "Diurna"): {
        "Encender": 0.0,
        "Ajustar": 0.1,
        "Apagar": 0.9
    },
    ("No", "Media", "Diurna"): {
        "Encender": 0.0,
        "Ajustar": 0.2,
        "Apagar": 0.8
    },
    ("No", "Baja", "Nocturna"): {
        "Encender": 0.05,
        "Ajustar": 0.05,
        "Apagar": 0.9
    }
}

# =========================
# FUNCIÓN CPD
# =========================
def elegir_accion(presencia, luz, hora):
    clave = (presencia, luz, hora)

    if clave not in cpd:
        return None

    probabilidades = cpd[clave]

    acciones = list(probabilidades.keys())
    pesos = list(probabilidades.values())

    return random.choices(acciones, pesos)[0]


# =========================
# CONVERSIÓN DE PERCEPCIÓN
# =========================
def convertir_percepcion(p):
    # Presencia
    presencia = "Si" if p.presencia else "No"

    # Clasificación de luz (lux → categoría)
    if p.luz_natural < 300:
        luz = "Baja"
    elif p.luz_natural < 700:
        luz = "Media"
    else:
        luz = "Alta"

    # Hora
    hora = "Diurna" if p.hora_tipo.lower() == "diurna" else "Nocturna"

    return presencia, luz, hora