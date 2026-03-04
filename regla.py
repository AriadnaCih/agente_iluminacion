from dataclasses import dataclass, field
from typing import Callable
from percepcion import Percepcion
from accion import Accion

Condicion = Callable[[Percepcion], bool]
AccionFn = Callable[[Percepcion], Accion]

@dataclass
class Regla:
    nombre: str
    condicion: Condicion
    accion: AccionFn
    prioridad: int = field(default=0)

    def evaluar(self, p: Percepcion) -> Accion | None:
        if self.condicion(p):
            return self.accion(p)
        return None