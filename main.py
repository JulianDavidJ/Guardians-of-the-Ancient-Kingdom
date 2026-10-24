"""
main.py - Creación de objetos, ejecución del programa y casos de prueba
de Guardians of the Ancient Kingdom.

Las clases NO se definen aquí: se importan de personajes.py.
Ejecutar con:  python main.py
"""

from personajes import (
    Personaje,
    Guerrero,
    Mago,
    Arquero,
    Combate,
    AtaqueInvalidoError,
)

resultados = []


def comprobar(descripcion, condicion):
    """Registra e imprime si una comprobación se cumplió."""
    resultados.append(bool(condicion))
    print(f"   [{'OK' if condicion else 'FALLO'}] {descripcion}")


def lanza(excepcion, funcion, *args):
    """True si funcion(*args) lanza la excepción esperada."""
    try:
        funcion(*args)
    except excepcion:
        return True
    except Exception:
        return False
    return False


def titulo(texto):
    print(f"\n--- {texto} ---")


def caso_1_creacion():
    titulo("Caso 1: creación correcta de los tres tipos de personajes")
    g = Guerrero("Arthas", 100, 30, 20)
    m = Mago("Gandalf", 80, 40, 10)
    a = Arquero("Legolas", 90, 35, 15)
    for p in (g, m, a):
        print("   ", p.mostrar_estado())
    comprobar("Guerrero, Mago y Arquero son Personaje",
              all(isinstance(p, Personaje) for p in (g, m, a)))
    comprobar("Atributos guardados correctamente",
              (g.nombre, g.vida, g.ataque, g.defensa) == ("Arthas", 100, 30, 20))
    comprobar("Personaje es abstracta (no se puede instanciar)",
              lanza(TypeError, Personaje, "X", 10, 10, 10))


def caso_2_vida_invalida():
    titulo("Caso 2: rechazo de vida superior a 100 o negativa")
    comprobar("Vida 101 rechazada", lanza(ValueError, Guerrero, "A", 101, 10, 5))
    comprobar("Vida -1 rechazada", lanza(ValueError, Mago, "B", -1, 10, 5))
    comprobar("Vida de tipo texto rechazada", lanza(TypeError, Arquero, "C", "50", 10, 5))
    p = Guerrero("D", 50, 10, 5)
    comprobar("Setter también rechaza vida 150", lanza(ValueError, setattr, p, "vida", 150))


def caso_3_nombre_vacio():
    titulo("Caso 3: rechazo de nombres vacíos")
    comprobar("Nombre '' rechazado", lanza(ValueError, Guerrero, "", 50, 10, 5))
    comprobar("Nombre '   ' rechazado", lanza(ValueError, Mago, "   ", 50, 10, 5))
    comprobar("Nombre no textual rechazado", lanza(TypeError, Arquero, 123, 50, 10, 5))


def caso_4_ataque_defensa_invalidos():
    titulo("Caso 4: rechazo de ataques y defensas inválidos")
    comprobar("Ataque 0 rechazado", lanza(ValueError, Guerrero, "A", 50, 0, 5))
    comprobar("Ataque negativo rechazado", lanza(ValueError, Guerrero, "A", 50, -5, 5))
    comprobar("Ataque decimal rechazado", lanza(TypeError, Guerrero, "A", 50, 3.5, 5))
    comprobar("Defensa negativa rechazada", lanza(ValueError, Mago, "B", 50, 10, -1))
    comprobar("Defensa 0 es válida", Mago("B", 50, 10, 0).defensa == 0)


def caso_5_guerrero():
    titulo("Caso 5: habilidad del Guerrero (ataque x1.20 - defensa)")
    g = Guerrero("Guerrero", 100, 30, 5)
    objetivo = Mago("Objetivo", 100, 10, 10)
    danio = g.atacar(objetivo)
    print(f"    Ataque 30, defensa enemiga 10 -> daño {danio}")
    comprobar("Daño = 26", danio == 26)
    comprobar("Vida del objetivo = 74", objetivo.vida == 74)
    fuerte = Arquero("Muralla", 100, 10, 50)
    comprobar("Con defensa muy alta el daño es 0, nunca negativo", g.atacar(fuerte) == 0)


def caso_6_mago():
    titulo("Caso 6: hechizo del Mago ignora la defensa")
    m = Mago("Mago", 100, 40, 5)
    objetivo = Guerrero("Objetivo", 100, 10, 20)
    danio = m.atacar(objetivo)
    print(f"    Ataque 40, defensa enemiga 20 -> daño {danio}")
    comprobar("Daño = 40 (defensa ignorada)", danio == 40)
    comprobar("Vida del objetivo = 60", objetivo.vida == 60)


def caso_7_arquero():
    titulo("Caso 7: disparo crítico del Arquero")
    a = Arquero("Arquero", 100, 35, 5)
    objetivo = Guerrero("Objetivo", 100, 10, 15)
    danio = a.atacar(objetivo)
    print(f"    Ataque 35, defensa enemiga 15 -> daño {danio}")
    comprobar("Daño = 40 ((35-15) x 2)", danio == 40)
    roca = Guerrero("Roca", 100, 10, 35)
    comprobar("Ataque igual a la defensa -> daño 0", a.atacar(roca) == 0)
    muro = Guerrero("Muro", 100, 10, 80)
    comprobar("Ataque menor que la defensa -> daño 0", a.atacar(muro) == 0)


def caso_8_vida_no_negativa():
    titulo("Caso 8: imposibilidad de tener vida negativa")
    p = Guerrero("Debil", 20, 10, 5)
    recibido = p.recibir_danio(50)
    print(f"    Vida 20, daño 50 -> daño efectivo {recibido}, vida {p.vida}")
    comprobar("La vida queda en 0 (no en -30)", p.vida == 0)
    comprobar("Devuelve el daño efectivo (20)", recibido == 20)
    comprobar("Ya no está vivo", not p.esta_vivo())
    comprobar("Daño negativo rechazado", lanza(ValueError, p.recibir_danio, -5))


def caso_9_derrotado_no_ataca():
    titulo("Caso 9: un personaje derrotado no puede atacar")
    caido = Mago("Caido", 10, 40, 5)
    caido.recibir_danio(10)
    sano = Guerrero("Sano", 100, 10, 5)
    comprobar("Derrotado no puede atacar", lanza(AtaqueInvalidoError, caido.atacar, sano))
    comprobar("No se puede atacar a un derrotado", lanza(AtaqueInvalidoError, sano.atacar, caido))
    comprobar("Objetivo inválido (None) rechazado", lanza(TypeError, sano.atacar, None))
    comprobar("Auto-ataque rechazado", lanza(AtaqueInvalidoError, sano.atacar, sano))


def caso_10_11_combate_completo():
    titulo("Casos 10 y 11: combate completo Arthas vs Gandalf e identificación del ganador")
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)
    combate = Combate(arthas, gandalf)   # agregación: los personajes ya existían
    ganador = combate.iniciar()
    print("\n   Comprobaciones:")
    comprobar("Resultado = victoria", combate.resultado == Combate.VICTORIA)
    comprobar("El ganador es Gandalf", ganador is gandalf)
    comprobar("Arthas quedó en 0 de vida", arthas.vida == 0)
    comprobar("Gandalf terminó con 2 de vida", gandalf.vida == 2)


def caso_12_empate_tecnico():
    titulo("Caso 12: combate sin daño -> empate técnico")
    a1 = Arquero("Arquero 1", 100, 10, 50)
    a2 = Arquero("Arquero 2", 100, 10, 50)
    combate = Combate(a1, a2)
    ganador = combate.iniciar()
    print("\n   Comprobaciones:")
    comprobar("Resultado = empate técnico", combate.resultado == Combate.EMPATE_TECNICO)
    comprobar("No hay ganador", ganador is None)
    comprobar("Ambos conservan la vida", a1.vida == 100 and a2.vida == 100)


def caso_extra_empate_50_rondas():
    titulo("Caso extra: 50 rondas sin ganador -> empate")
    g1 = Guerrero("Guerrero 1", 100, 1, 0)
    g2 = Guerrero("Guerrero 2", 100, 1, 0)
    combate = Combate(g1, g2, mostrar_mensajes=False)
    combate.iniciar()
    print(f"    Rondas jugadas: {combate.rondas} | vidas: {g1.vida} y {g2.vida}")
    comprobar("Resultado = empate por límite de rondas",
              combate.resultado == Combate.EMPATE_RONDAS)
    comprobar("Se jugaron exactamente 50 rondas", combate.rondas == 50)


def caso_extra_polimorfismo():
    titulo("Caso extra: polimorfismo (misma llamada, distinto comportamiento)")
    for guardian in (Guerrero("G", 100, 30, 5), Mago("M", 100, 30, 5), Arquero("A", 100, 30, 5)):
        victima = Guerrero("Victima", 100, 10, 10)
        print(f"    {type(guardian).__name__:8} ataca (30) a defensa 10 -> {guardian.atacar(victima)}")
    comprobar("Se ejecutó atacar() en las tres clases sin preguntar el tipo", True)


def main():
    print("=" * 62)
    print(" GUARDIANS OF THE ANCIENT KINGDOM - Casos de prueba")
    print("=" * 62)

    caso_1_creacion()
    caso_2_vida_invalida()
    caso_3_nombre_vacio()
    caso_4_ataque_defensa_invalidos()
    caso_5_guerrero()
    caso_6_mago()
    caso_7_arquero()
    caso_8_vida_no_negativa()
    caso_9_derrotado_no_ataca()
    caso_10_11_combate_completo()
    caso_12_empate_tecnico()
    caso_extra_empate_50_rondas()
    caso_extra_polimorfismo()

    print("\n" + "=" * 62)
    print(f" RESUMEN: {sum(resultados)} de {len(resultados)} comprobaciones correctas")
    print("=" * 62)


if __name__ == "__main__":
    main()
