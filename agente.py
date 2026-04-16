from percepcion import Percepcion
from accion import Accion
from regla import Regla
from motor_inferencia import MotorInferencia

# 🔥 NUEVO
from cpd import elegir_accion, convertir_percepcion


class AgenteIluminacion:
    def __init__(self) -> None:
        self.motor = MotorInferencia()

    def decidir_accion(self, p: Percepcion, usar_cpd_only: bool = False) -> Accion:
        if not usar_cpd_only:
            # 1. Intentar con reglas
            accion = self.motor.evaluar(p)
            if accion is not None:
                print("[INFO] Acción tomada por REGLAS")
                return accion
        else:
            print("[INFO] Saltando reglas y usando solo CPD")

        # 2. Usar CPD
        print("[INFO] Acción tomada por CPD (probabilístico)")
        presencia, luz, hora = convertir_percepcion(p)
        resultado = elegir_accion(presencia, luz, hora)

        # 3. Convertir resultado a objeto Accion
        if resultado == "Encender":
            return Accion("ENCENDER", 100, 0)

        elif resultado == "Ajustar":
            return Accion("AJUSTAR", 50, 0)

        elif resultado == "Apagar":
            return Accion("APAGAR", 0, 0)

        # Seguridad si la CPD no tiene la clave
        return Accion("MANTENER", p.intensidad_actual, 0)
