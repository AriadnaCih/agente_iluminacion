from dataclasses import dataclass

@dataclass(frozen=True)
class Percepcion:
    luz_natural: int
    presencia: bool
    hora_tipo: str
    intensidad_actual: int

    def es_valida(self) -> bool:

        if self.luz_natural < 0:
            print("[ERROR] La luz natural no puede ser negativa.")
            return False

        if self.hora_tipo.strip().lower() not in ("diurna", "nocturna"):
            print("[ERROR] hora_tipo debe ser 'diurna' o 'nocturna'.")
            return False

        if not (0 <= self.intensidad_actual <= 100):
            print("[ERROR] intensidad_actual debe estar entre 0 y 100.")
            return False

        return True