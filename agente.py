from percepcion import Percepcion
from accion import Accion
from regla import Regla
from motor_inferencia import MotorInferencia

class AgenteIluminacion:
    def __init__(self) -> None:
        self.motor = MotorInferencia()

    def decidir_accion(self, p: Percepcion) -> Accion:
        return self.motor.evaluar(p)