"""
Guardians of the Ancient Kingdom - Sistema de combate por turnos.

Este módulo define SOLO las clases del sistema:
    Personaje (abstracta), Guerrero, Mago, Arquero y Combate.

No ejecuta nada al importarse: la creación de objetos y las pruebas
están en main.py.
"""

from abc import ABC, abstractmethod


class AtaqueInvalidoError(Exception):
    """Se intentó un ataque que rompe las reglas del juego
    (atacante derrotado, objetivo derrotado, auto-ataque...)."""


def _es_entero(valor):
    """True si el valor es un int 'real' (bool también es int en Python, se excluye)."""
    return isinstance(valor, int) and not isinstance(valor, bool)


# ----------------------------------------------------------------------
# Clase abstracta
# ----------------------------------------------------------------------
class Personaje(ABC):
    """Clase base abstracta de todos los guardianes.

    Centraliza los atributos comunes (nombre, vida, ataque, defensa),
    sus validaciones y los comportamientos que no cambian entre tipos
    de personaje. Obliga a las subclases a implementar `atacar()`.
    """

    VIDA_MAXIMA = 100

    def __init__(self, nombre, vida, ataque, defensa):
        # Se asigna mediante los setters para reutilizar las validaciones.
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa

    # ---------------- Encapsulamiento: getters y setters ----------------
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            raise TypeError("El nombre debe ser un texto.")
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, valor):
        if not _es_entero(valor):
            raise TypeError("La vida debe ser un número entero.")
        if not 0 <= valor <= self.VIDA_MAXIMA:
            raise ValueError(
                f"La vida debe estar entre 0 y {self.VIDA_MAXIMA} (recibido: {valor})."
            )
        self._vida = valor

    @property
    def ataque(self):
        return self._ataque

    @ataque.setter
    def ataque(self, valor):
        if not _es_entero(valor):
            raise TypeError("El ataque debe ser un número entero.")
        if valor <= 0:
            raise ValueError(f"El ataque debe ser positivo (recibido: {valor}).")
        self._ataque = valor

    @property
    def defensa(self):
        return self._defensa

    @defensa.setter
    def defensa(self, valor):
        if not _es_entero(valor):
            raise TypeError("La defensa debe ser un número entero.")
        if valor < 0:
            raise ValueError(f"La defensa no puede ser negativa (recibido: {valor}).")
        self._defensa = valor

    # ---------------- Métodos comunes ----------------
    def recibir_danio(self, cantidad):
        """Resta vida y devuelve el daño efectivamente recibido.

        El daño llega ya calculado (la defensa NO se descuenta aquí).
        La vida nunca baja de cero.
        """
        if not _es_entero(cantidad):
            raise TypeError("El daño debe ser un número entero.")
        if cantidad < 0:
            raise ValueError("No se acepta daño negativo.")
        recibido = min(cantidad, self._vida)
        self._vida -= recibido
        return recibido

    def esta_vivo(self):
        return self._vida > 0

    def mostrar_estado(self):
        """Devuelve (como texto) la información actual del personaje."""
        estado = "vivo" if self.esta_vivo() else "derrotado"
        return (
            f"{self._nombre} ({type(self).__name__}) | "
            f"Vida: {self._vida}/{self.VIDA_MAXIMA} | "
            f"Ataque: {self._ataque} | Defensa: {self._defensa} | {estado}"
        )

    def _validar_ataque(self, objetivo):
        """Validaciones comunes a todos los ataques (las usan las subclases)."""
        if not isinstance(objetivo, Personaje):
            raise TypeError("El objetivo debe ser un Personaje.")
        if objetivo is self:
            raise AtaqueInvalidoError(f"{self._nombre} no puede atacarse a sí mismo.")
        if not self.esta_vivo():
            raise AtaqueInvalidoError(
                f"{self._nombre} está derrotado y no puede atacar."
            )
        if not objetivo.esta_vivo():
            raise AtaqueInvalidoError(
                f"{objetivo.nombre} ya está derrotado y no puede ser atacado."
            )

    @abstractmethod
    def atacar(self, objetivo):
        """Ataca al objetivo y devuelve el daño efectivamente causado.
        Cada tipo de personaje define su propia forma de atacar."""


# ----------------------------------------------------------------------
# Subclases
# ----------------------------------------------------------------------
class Guerrero(Personaje):
    """Golpe poderoso: ataque +20 % antes de descontar la defensa."""

    def atacar(self, objetivo):
        self._validar_ataque(objetivo)
        # ataque * 1.20 con enteros (//) -> redondeo hacia abajo sin errores de float
        ataque_potenciado = self.ataque * 120 // 100
        danio = max(0, ataque_potenciado - objetivo.defensa)
        return objetivo.recibir_danio(danio)


class Mago(Personaje):
    """Hechizo penetrante: ignora por completo la defensa del objetivo."""

    def atacar(self, objetivo):
        self._validar_ataque(objetivo)
        danio = self.ataque
        return objetivo.recibir_danio(danio)


class Arquero(Personaje):
    """Disparo crítico: si su ataque supera la defensa, duplica el daño."""

    def atacar(self, objetivo):
        self._validar_ataque(objetivo)
        danio_base = max(0, self.ataque - objetivo.defensa)
        danio = danio_base * 2 if self.ataque > objetivo.defensa else 0
        return objetivo.recibir_danio(danio)


# ----------------------------------------------------------------------
# Combate
# ----------------------------------------------------------------------
class Combate:
    """Administra un enfrentamiento por turnos entre dos personajes.

    Agregación: los personajes se crean fuera y llegan ya construidos;
    Combate los administra pero no los crea ni los posee.
    Solo usa atacar(), esta_vivo() y mostrar_estado() (polimorfismo):
    nunca pregunta si un personaje es Guerrero, Mago o Arquero.
    """

    MAX_RONDAS = 50

    VICTORIA = "victoria"
    EMPATE_TECNICO = "empate técnico"
    EMPATE_RONDAS = "empate por límite de rondas"

    def __init__(self, personaje1, personaje2, mostrar_mensajes=True):
        for p in (personaje1, personaje2):
            if not isinstance(p, Personaje):
                raise TypeError("Los participantes deben ser Personajes.")
        if personaje1 is personaje2:
            raise ValueError("Un personaje no puede combatir contra sí mismo.")
        if not (personaje1.esta_vivo() and personaje2.esta_vivo()):
            raise ValueError("Ambos participantes deben estar vivos para combatir.")

        self._participantes = [personaje1, personaje2]
        self._turno = 0             # índice de quien ataca ahora
        self._turnos_jugados = 0
        self._rondas = 0            # rondas completas (ambos atacaron)
        self._danio_ronda = 0       # daño causado en la ronda en curso
        self._resultado = None
        self._ganador = None
        self._mostrar = mostrar_mensajes

    # ---- consultas ----
    @property
    def ganador(self):
        return self._ganador

    @property
    def resultado(self):
        return self._resultado

    @property
    def rondas(self):
        return self._rondas

    def _log(self, texto=""):
        if self._mostrar:
            print(texto)

    def _mostrar_estados(self):
        for p in self._participantes:
            self._log(f"    {p.mostrar_estado()}")

    # ---- métodos requeridos ----
    def cambiar_turno(self):
        """Alterna el personaje que debe atacar y lo devuelve."""
        self._turno = 1 - self._turno
        return self._participantes[self._turno]

    def verificar_ganador(self):
        """Devuelve al vencedor si el otro llegó a cero de vida; si no, None."""
        a, b = self._participantes
        if a.esta_vivo() and not b.esta_vivo():
            return a
        if b.esta_vivo() and not a.esta_vivo():
            return b
        return None

    def iniciar(self):
        """Ejecuta el combate completo y devuelve el ganador (None si hay empate)."""
        if self._resultado is not None:
            raise RuntimeError("Este combate ya finalizó.")

        a, b = self._participantes
        self._log(f"=== COMBATE: {a.nombre} vs {b.nombre} ===")
        self._mostrar_estados()

        while self._resultado is None:
            atacante = self._participantes[self._turno]
            objetivo = self._participantes[1 - self._turno]

            danio = atacante.atacar(objetivo)      # polimorfismo
            self._danio_ronda += danio
            self._turnos_jugados += 1

            self._log(
                f"\nTurno {self._turnos_jugados} (ronda {self._rondas + 1}): "
                f"{atacante.nombre} ataca a {objetivo.nombre} -> daño efectivo {danio}"
            )
            self._mostrar_estados()

            ganador = self.verificar_ganador()
            if ganador is not None:
                self._ganador = ganador
                self._resultado = self.VICTORIA
                break

            self.cambiar_turno()

            if self._turno == 0:  # se completó una ronda
                self._rondas += 1
                if self._danio_ronda == 0:
                    self._resultado = self.EMPATE_TECNICO
                elif self._rondas >= self.MAX_RONDAS:
                    self._resultado = self.EMPATE_RONDAS
                self._danio_ronda = 0

        self.mostrar_resultado()
        return self._ganador

    def mostrar_resultado(self):
        """Presenta el resultado final y lo devuelve como texto."""
        if self._resultado is None:
            texto = "El combate aún no ha finalizado."
        elif self._resultado == self.VICTORIA:
            texto = f"Ganador: {self._ganador.nombre}"
        else:
            texto = f"Resultado: {self._resultado} tras {self._rondas} ronda(s)."
        self._log(f"\n*** {texto} ***")
        return texto
