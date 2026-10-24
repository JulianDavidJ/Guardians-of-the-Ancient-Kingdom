# Guardians of the Ancient Kingdom
## Proyecto integrador — Sistema de combate por turnos

**Asignatura:** Programación Orientada a Objetos con Python  
**Temas:** Abstracción, herencia, polimorfismo, encapsulamiento, métodos, validaciones y relaciones entre clases.  
**Nivel:** Intermedio

---

# 1. Contexto del problema

En el antiguo reino de Eldoria existen tres órdenes de guardianes: Guerreros, Magos y Arqueros.

Cada orden tiene habilidades diferentes, pero todos los personajes comparten ciertas características: nombre, vida, ataque y defensa.

El reino necesita desarrollar un sistema de combate por turnos que permita enfrentar a dos guardianes y determinar automáticamente cuál resulta vencedor.

El programa deberá aplicar las reglas de combate de cada personaje, controlar los turnos, actualizar la vida y finalizar los enfrentamientos cuando corresponda.

# 2. Analicemos el problema antes de programar

Antes de escribir código, debemos identificar qué elementos existen y cómo se relacionan.

## ¿Qué tienen en común los personajes?

Todos deben tener nombre, vida, ataque y defensa.

¿Sería conveniente repetir estos atributos en cada clase?

Podemos utilizar una clase base `Personaje` para centralizar las características comunes.

Aquí aparece la **herencia**.

## ¿Todos atacan de la misma manera?

No.

- El Guerrero incrementa su ataque utilizando su fuerza.
- El Mago utiliza hechizos que ignoran la defensa.
- El Arquero aprovecha los puntos débiles del enemigo para duplicar el daño.

Todos deben atacar, pero cada uno implementa esa operación de una forma diferente.

Aquí podemos utilizar una **clase abstracta** que obligue a sus subclases a implementar `atacar()`.

Y cuando el sistema invoque esa operación sobre distintos personajes, estaremos aplicando **polimorfismo**.

## ¿Puede un personaje tener vida negativa?

Supongamos que un personaje tiene 20 puntos de vida y recibe 50 puntos de daño.

¿Su vida debería quedar en -30?

No. Necesitamos controlar los valores permitidos mediante **encapsulamiento y validaciones**.

Los atributos deberán protegerse y modificarse mediante métodos apropiados.

## ¿Quién controla los combates?

Los personajes deben responsabilizarse de sus propias acciones.

Pero alguien debe controlar los turnos, identificar al ganador y finalizar el combate.

Por eso necesitaremos una clase `Combate` independiente de los personajes.

Un combate **tiene participantes**, mientras que un Guerrero **es un Personaje**.

Estas dos expresiones nos ayudan a identificar relaciones diferentes: agregación y herencia.

---

# 3. Requerimientos del sistema

## 3.1. Clase abstracta `Personaje`

Desarrollar una clase abstracta utilizando `ABC` y `@abstractmethod`.

Esta clase debe contener las características y comportamientos comunes de todos los personajes.

### Atributos encapsulados

| Atributo | Condición |
|---|---|
| nombre | Texto no vacío |
| vida | Entero entre 0 y 100 |
| ataque | Entero positivo |
| defensa | Entero no negativo |

El constructor deberá recibir los valores iniciales y comprobar que sean válidos.

Implementar getters y setters para consultar y modificar los atributos, respetando sus restricciones.

Los datos inválidos deberán producir excepciones apropiadas.

### Métodos comunes

**`recibir_danio(cantidad)`**

Debe actualizar la vida del personaje.

- No se aceptan cantidades negativas.
- La vida nunca puede quedar por debajo de cero.
- Debe devolver el daño efectivamente recibido.
- El daño recibido ya debe estar calculado; no se descontará la defensa nuevamente.

**`esta_vivo()`**

Debe devolver `True` cuando el personaje tenga vida y `False` cuando esté derrotado.

**`mostrar_estado()`**

Debe permitir consultar la información actual del personaje.

**`atacar(objetivo)`**

Debe ser un método abstracto que las clases hijas estén obligadas a implementar.

---

## 3.2. Clase `Guerrero`

Debe heredar de `Personaje`.

**Habilidad especial: Golpe poderoso**

Su ataque aumenta un 20 % antes de descontar la defensa enemiga.

**Daño = máximo(0, ataque × 1.20 − defensa del objetivo)**

Ejemplo:

- Ataque: 30.
- Defensa enemiga: 10.
- Ataque potenciado: 36.
- Daño final: 26.

Los resultados decimales se redondearán hacia abajo antes de aplicar el daño.

---

## 3.3. Clase `Mago`

Debe heredar de `Personaje`.

**Habilidad especial: Hechizo penetrante**

Sus ataques ignoran completamente la defensa del objetivo.

**Daño = ataque del Mago**

Ejemplo:

- Ataque: 40.
- Defensa enemiga: 20.
- Daño final: 40.

---

## 3.4. Clase `Arquero`

Debe heredar de `Personaje`.

**Habilidad especial: Disparo crítico**

Si su ataque supera la defensa del enemigo, duplica el daño convencional.

**Daño base = máximo(0, ataque − defensa del objetivo)**

**Daño final = daño base × 2**, cuando el ataque supera la defensa.

Ejemplo:

- Ataque: 35.
- Defensa enemiga: 15.
- Daño base: 20.
- Daño final: 40.

Si el ataque no supera la defensa, el daño será cero.

### Validaciones comunes de ataque

Las tres clases deberán comprobar que:

- El atacante está vivo.
- El objetivo está vivo.
- El objetivo es válido.
- El daño nunca sea negativo.
- La vida del objetivo nunca quede por debajo de cero.

---

# 4. Clase `Combate`

Crear una clase independiente que administre los enfrentamientos.

Debe recibir dos personajes previamente creados.

### Métodos requeridos

**`iniciar()`**: ejecuta el enfrentamiento por turnos.

**`cambiar_turno()`**: alterna el personaje que debe atacar.

**`verificar_ganador()`**: determina si existe un vencedor.

**`mostrar_resultado()`**: presenta el resultado final del combate.

### Reglas generales

1. Cada personaje realiza un ataque por turno.
2. Un personaje derrotado no puede atacar.
3. El combate termina cuando la vida de un participante llega a cero.
4. Después de cada ataque se muestra el estado de los participantes.
5. El combate debe utilizar polimorfismo, sin preguntar si el personaje es específicamente Guerrero, Mago o Arquero.
6. Si ambos personajes completan una ronda sin causarse daño, se declara empate técnico.
7. Si se completan 50 rondas sin ganador, el combate termina en empate.

---

# 5. Relaciones entre clases

El programa deberá evidenciar las siguientes relaciones:

**Herencia:** Guerrero, Mago y Arquero son tipos de Personaje.

**Asociación:** cuando un personaje ataca a otro, ambos objetos interactúan mediante sus métodos.

**Agregación:** Combate administra personajes que fueron creados independientemente de él.

Cada relación deberá poder explicarse a partir de las responsabilidades de los objetos.

---

# 6. Ejemplo de funcionamiento

Crear los siguientes personajes:

| Personaje | Tipo | Vida | Ataque | Defensa |
|---|---|---:|---:|---:|
| Arthas | Guerrero | 100 | 30 | 20 |
| Gandalf | Mago | 80 | 40 | 10 |

El programa deberá ejecutar un combate como el siguiente:

| Turno | Atacante | Daño | Vida Arthas | Vida Gandalf |
|---|---|---:|---:|---:|
| Inicio | — | — | 100 | 80 |
| 1 | Arthas | 26 | 100 | 54 |
| 2 | Gandalf | 40 | 60 | 54 |
| 3 | Arthas | 26 | 60 | 28 |
| 4 | Gandalf | 40 | 20 | 28 |
| 5 | Arthas | 26 | 20 | 2 |
| 6 | Gandalf | 20 efectivo | 0 | 2 |

**Ganador: Gandalf.**

---

# 7. Casos de prueba obligatorios

El programa debe demostrar que las validaciones y las reglas funcionan correctamente.

Se deberán comprobar, como mínimo:

1. Creación correcta de los tres tipos de personajes.
2. Rechazo de personajes con vida superior a 100 o negativa.
3. Rechazo de nombres vacíos.
4. Rechazo de ataques y defensas inválidos.
5. Aplicación correcta de la habilidad del Guerrero.
6. Aplicación correcta del ataque del Mago ignorando defensa.
7. Aplicación correcta del disparo crítico del Arquero.
8. Imposibilidad de tener vida negativa.
9. Imposibilidad de atacar estando derrotado.
10. Ejecución de un combate completo.
11. Identificación correcta del ganador.
12. Finalización de un combate sin daño mediante empate técnico.

Los casos de prueba deberán mostrar resultados que permitan comprobar el comportamiento esperado.

---

# 8. Entrega del proyecto

## 8.1. Medio de entrega

**La entrega se realizará exclusivamente mediante un repositorio público de GitHub.**

Cada estudiante deberá entregar el enlace de su repositorio, verificando que el contenido pueda consultarse y que el programa pueda ejecutarse.

## 8.2. Estructura obligatoria

El repositorio deberá contener **tres archivos principales**:

```text
Guardians-of-the-Ancient-Kingdom/
│
├── personajes.py
│
├── main.py
│
└── README.md
```

### Archivo 1 — `personajes.py`

En este archivo deberá encontrarse la implementación de las clases del sistema:

- `Personaje` (abstracta).
- `Guerrero`.
- `Mago`.
- `Arquero`.
- `Combate`.

Debe contener los constructores, atributos encapsulados, getters, setters, métodos, validaciones y lógica correspondiente.

**Este archivo define cómo funciona el sistema, pero no debe ejecutar automáticamente los casos de prueba al importarse.**

### Archivo 2 — `main.py`

Este archivo estará dedicado a la creación de objetos, la ejecución del programa y los casos de prueba.

Deberá:

- Importar las clases definidas en `personajes.py`.
- Crear instancias de distintos personajes.
- Ejecutar ataques y combates.
- Comprobar las habilidades especiales.
- Demostrar las validaciones y el manejo de errores.
- Mostrar los resultados de los casos de prueba.

No se debe repetir aquí la implementación de las clases.

La intención es separar **la definición de las clases** de **su utilización y comprobación**.

### Archivo 3 — `README.md`

El README será la documentación del proyecto.

Deberá explicar, con palabras propias:

**1. Descripción:** ¿En qué consiste Guardians of the Ancient Kingdom y qué problema resuelve?

**2. Estructura:** ¿Qué contiene cada archivo y para qué se utiliza?

**3. Clases:** ¿Qué responsabilidad tiene `Personaje`, cada subclase y `Combate`?

**4. Relaciones:** ¿Cuáles son las relaciones de herencia, asociación y agregación? ¿Por qué se utilizaron?

**5. Conceptos de POO:** ¿Dónde se aplican la abstracción, el encapsulamiento, la herencia y el polimorfismo?

**6. Lógica del combate:** ¿Cómo se calcula el daño y cómo se administran los turnos?

**7. Ejecución:** ¿Qué debe hacer otra persona para descargar y ejecutar el programa?

**8. Pruebas:** ¿Qué casos fueron comprobados y cuáles fueron los resultados?

El README no debe limitarse a copiar definiciones teóricas. Debe explicar cómo se aplican los conceptos en el programa desarrollado.

---

# 9. Retos para alcanzar la calificación máxima

Además del cumplimiento de los requerimientos obligatorios, se proponen tres retos de profundización.

**Los tres retos otorgan puntos adicionales y permitirán aspirar a la calificación máxima de 5.0.**

No es suficiente mencionar las herramientas o los conceptos: cada reto debe tener una evidencia clara de su realización.

## Reto extra 1 — Investiga y construye un diagrama de clases UML

**Tema: diseño y arquitectura de software.**

Investiga qué es un **diagrama de clases UML** y cómo se utiliza para representar sistemas orientados a objetos.

Construye un diagrama que represente la arquitectura de tu programa.

El diagrama deberá mostrar:

- Las clases principales.
- Sus atributos.
- Sus métodos más importantes.
- Las relaciones de herencia.
- Las relaciones de asociación y agregación.
- La clase abstracta y su método abstracto.

El diagrama podrá elaborarse con una herramienta de diagramación o mediante una representación textual compatible con UML.

**Evidencia:** incluir el diagrama en el `README.md`, acompañado de una breve explicación.

Este reto busca comprobar que el estudiante puede representar y explicar visualmente las relaciones del sistema, no solamente programarlas.

## Reto extra 2 — Automatiza las pruebas utilizando Pytest

**Tema: pruebas automatizadas de software.**

Investiga qué es **Pytest**, para qué se utiliza y cómo permite comprobar automáticamente el funcionamiento de un programa Python.

En lugar de limitarse a ejecutar el programa y revisar visualmente los mensajes, desarrolla pruebas automatizadas que verifiquen las reglas del sistema.

Como mínimo, las pruebas automatizadas deberán comprobar:

- La creación de personajes válidos.
- El rechazo de valores incorrectos.
- El cálculo del daño de cada clase.
- Que la vida nunca sea negativa.
- Que un personaje derrotado no pueda atacar.
- Que un combate determine correctamente su resultado.

**Evidencia:** mostrar en el README cómo ejecutar las pruebas con Pytest e incluir el resultado de su ejecución.

Para conservar los tres archivos obligatorios, se permite incorporar las pruebas de Pytest dentro de `main.py` y ejecutarlas indicando explícitamente ese archivo. También se acepta un archivo adicional `test_personajes.py` cuando el estudiante decida separar profesionalmente sus pruebas automatizadas.

Este reto busca introducir una práctica fundamental del desarrollo profesional: **demostrar mediante pruebas repetibles que el código cumple sus reglas**.

## Reto extra 3 — Resuelve el desafío de abstracción

**Tema: razonamiento y diseño orientado a objetos.**

Responde la siguiente pregunta:

### ¿Por qué `atacar()` debe ser abstracto, pero `recibir_danio()` puede estar implementado en la clase base?

No se aceptará como respuesta únicamente que uno utiliza `@abstractmethod` y el otro no.

La explicación deberá abordar:

- Qué responsabilidad corresponde a la clase `Personaje`.
- Qué comportamientos comparten todos los personajes.
- Por qué cada clase hija necesita una implementación diferente de `atacar()`.
- Por qué la lógica general de `recibir_danio()` puede reutilizarse.
- Cómo se relaciona esta decisión con la abstracción, la herencia y el polimorfismo.

El estudiante deberá justificar su respuesta utilizando ejemplos de su propio programa.

**Evidencia:** incluir en el README una sección llamada **Reto de abstracción**, con una explicación argumentada.

Este reto busca evaluar la comprensión del diseño del sistema, no la memorización de conceptos.

---

# 10. Condiciones para la calificación máxima

Para aspirar a la nota máxima, el proyecto deberá cumplir dos condiciones:

**Primera: desarrollar correctamente el proyecto principal.**

El sistema deberá funcionar, aplicar las reglas de combate, contener las validaciones solicitadas y demostrar la utilización de los conceptos de POO.

**Segunda: completar y evidenciar los tres retos adicionales.**

| Reto | Evidencia esperada |
|---|---|
| UML | Diagrama de clases incluido y explicado en el README |
| Pytest | Pruebas automatizadas funcionales y documentadas |
| Abstracción | Respuesta argumentada sobre `atacar()` y `recibir_danio()` |

Los retos son oportunidades de profundización y reconocimiento adicional, pero no sustituyen los requerimientos principales.

**Importante:** presentar los tres retos no garantiza automáticamente el 5.0. Para obtenerlo, deben estar correctamente desarrollados y el proyecto principal debe funcionar.

---

# 11. Reflexión final

Al terminar el proyecto, el estudiante debería poder explicar:

- Por qué el sistema necesita una clase abstracta.
- Cómo se reutilizan atributos y métodos mediante herencia.
- Cómo cada personaje ejecuta diferentes ataques utilizando polimorfismo.
- Por qué los atributos necesitan encapsulamiento y validaciones.
- Cómo interactúan las clases durante un combate.
- Por qué el administrador del combate no necesita conocer las implementaciones específicas de cada personaje.
- Cómo podría añadirse un nuevo guardián sin modificar la lógica general de combate.

**Objetivo final:** desarrollar un sistema orientado a objetos organizado, extensible y verificable, demostrando no solo la capacidad de escribir código Python, sino también la capacidad de analizar un problema, diseñar relaciones entre clases y justificar las decisiones de programación.