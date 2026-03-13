from typing import List
from percepcion import Percepcion
from accion import Accion
from regla import Regla

class MotorInferencia:
    def __init__(self) -> None:
        self.reglas: List[Regla] = []
        self._cargar_reglas()

    def agregar_regla(self, regla: Regla) -> None:
        self.reglas.append(regla)

    def _cargar_reglas(self) -> None:
        # Percepción inválida (máxima prioridad)
        self.agregar_regla(Regla(
            nombre="Percepcion invalida",
            condicion=lambda p: (not hasattr(p, "es_valida")) or (not p.es_valida()),
            accion=lambda p: Accion("MANTENER", getattr(p, "intensidad_actual", 0)),
            prioridad=10
        ))

        # Sin presencia -> apagar tras 5 min (300s)
        self.agregar_regla(Regla(
            nombre="Sin presencia, apagar tras 5 min",
            condicion=lambda p: (not p.presencia) and (p.intensidad_actual > 0),
            accion=lambda p: Accion("APAGAR", 0, delay=300),
            prioridad=9
        ))

        # Luz alta + diurna + presencia -> apagar
        self.agregar_regla(Regla(
            nombre="Luz alta + diurna + presencia -> apagar",
            condicion=lambda p: (p.luz_natural > 500) and p.presencia and (p.hora_tipo.strip().lower() == "diurna"),
            accion=lambda p: Accion("APAGAR", 0),
            prioridad=8
        ))

        # Muy baja + nocturna -> 100%
        self.agregar_regla(Regla(
            nombre="Muy baja + nocturna -> 100%",
            condicion=lambda p: (p.luz_natural < 50) and p.presencia and (p.hora_tipo.strip().lower() == "nocturna") and (p.intensidad_actual < 100),
            accion=lambda p: Accion("ENCENDER", 100),
            prioridad=7
        ))

        # Baja + nocturna -> 80%
        self.agregar_regla(Regla(
            nombre="Baja + nocturna -> ajustar 80%",
            condicion=lambda p: (p.luz_natural < 200) and p.presencia and (p.hora_tipo.strip().lower() == "nocturna") and (p.intensidad_actual < 80),
            accion=lambda p: Accion("AJUSTAR", 80),
            prioridad=6
        ))

        # Baja + diurna -> 60%
        self.agregar_regla(Regla(
            nombre="Baja + diurna -> ajustar 60%",
            condicion=lambda p: (p.luz_natural < 200) and p.presencia and (p.hora_tipo.strip().lower() == "diurna") and (p.intensidad_actual < 60),
            accion=lambda p: Accion("AJUSTAR", 60),
            prioridad=5
        ))

        # Media + nocturna -> 50%
        self.agregar_regla(Regla(
            nombre="Media + nocturna -> ajustar 50%",
            condicion=lambda p: (200 <= p.luz_natural <= 500) and p.presencia and (p.hora_tipo.strip().lower() == "nocturna") and (p.intensidad_actual < 50),
            accion=lambda p: Accion("AJUSTAR", 50),
            prioridad=3
        ))

        # Media + diurna -> 30%
        self.agregar_regla(Regla(
            nombre="Media + diurna -> ajustar 30%",
            condicion=lambda p: (200 <= p.luz_natural <= 500) and p.presencia and (p.hora_tipo.strip().lower() == "diurna") and (p.intensidad_actual < 30),
            accion=lambda p: Accion("AJUSTAR", 30),
            prioridad=2
        ))

    def listar_reglas(self) -> None:
        """Imprime todas las reglas ordenadas por prioridad."""
        print(f"\n{'='*60}")
        print(f"TOTAL DE REGLAS: {len(self.reglas)}")
        print(f"{'='*60}")
        
        # Ordenar reglas por prioridad (mayor primero)
        reglas_ordenadas = sorted(self.reglas, key=lambda r: r.prioridad, reverse=True)
        
        for idx, regla in enumerate(reglas_ordenadas, 1):
            print(f"{idx}. [{regla.prioridad}/10] {regla.nombre}")
        print(f"{'='*60}\n")

        # Devolver la lista ordenada para usos posteriores
        return reglas_ordenadas

    def obtener_reglas_ordenadas(self) -> List[Regla]:
        """Retorna las reglas ordenadas por prioridad (mayor primero)."""
        return sorted(self.reglas, key=lambda r: r.prioridad, reverse=True)

    def eliminar_regla_por_indice(self, indice: int) -> bool:
        """Elimina la regla en la posición (1-based) según la lista ordenada.

        Retorna True si se eliminó correctamente, False si el índice no es válido.
        """
        reglas_ordenadas = self.obtener_reglas_ordenadas()
        if indice < 1 or indice > len(reglas_ordenadas):
            return False

        regla_a_eliminar = reglas_ordenadas[indice - 1]
        self.reglas = [r for r in self.reglas if r is not regla_a_eliminar]
        return True

    def eliminar_regla_por_nombre(self, nombre: str) -> bool:
        """Elimina la primera regla que coincida exactamente con el nombre dado."""
        for regla in self.reglas:
            if regla.nombre == nombre:
                self.reglas.remove(regla)
                return True
        return False

    def evaluar(self, p: Percepcion) -> Accion:

        if p is None or not hasattr(p, "intensidad_actual"):
            return Accion("MANTENER", 0)

        # Ordenar reglas por prioridad (mayor prioridad primero)
        reglas_ordenadas = sorted(self.reglas, key=lambda r: r.prioridad, reverse=True)

        for regla in reglas_ordenadas:
            try:
                accion = regla.evaluar(p)
            except Exception as e:
              
                print(f"[WARN] Error evaluando regla '{regla.nombre}': {e}. Se ignora.")
                accion = None

            if accion is not None:
                return accion

       
        intensidad = getattr(p, "intensidad_actual", 0)
        return Accion("MANTENER", intensidad if isinstance(intensidad, int) else 0) 