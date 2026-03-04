from dataclasses import dataclass

@dataclass(frozen=True)
class Accion:
    tipo: str
    intensidad: int = 0
    delay: int = 0  # segundos

    def ejecutar(self) -> None:
        if self.delay > 0:
            mins = self.delay // 60
            secs = self.delay % 60
            if mins > 0 and secs == 0:
                print(f"Acción: {self.tipo} después de {mins} min -> {self.intensidad}%")
            else:
                print(f"Acción: {self.tipo} después de {self.delay} s -> {self.intensidad}%")
        else:
            print(f"Acción: {self.tipo} -> {self.intensidad}%")