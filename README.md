# Setup de Simulación y Caracterización de Amplificador Multietapa

Este repositorio contiene el entorno de simulación automatizada y procesamiento de datos desarrollado en **LTspice** y **Python** para la caracterización eléctrica de un amplificador de audio multietapa (BJT / MOSFET).

Este setup está diseñado para reproducir los ensayos presentados en el informe técnico del proyecto, así como para permitir la extensión y personalización de nuevas mediciones en el circuito.

---

## 📂 Estructura del Repositorio

```text
.
├── .gitignore                      # Filtro para excluir archivos temporales y binarios pesados
├── docs/                           # Resultados procesados y exportaciones (.xlsx)
│   └── Resultados_Simulacion.xlsx
├── ltspice/                        # Esquemático y archivos de simulación
│   ├── amplificador_tp2.asc        # Esquemático principal editable de LTspice
│   ├── amplificador_tp2.log        # Reporte de mediciones generado por LTspice
│   └── mediciones.txt              # Copia de respaldo con el bloque de directivas .meas
├── python/                         # Scripts de automatización
│   ├── run_simulations.py          # Ejecución de LTspice en modo Batch
│   ├── parse_log.py                # Visualizador de mediciones por consola/terminal
│   └── generate_sheets_tables.py   # Extractor de parámetros .meas a Excel en docs/
└── README.md                       # Manual de uso del repositorio
```

---

## 🛠️ Requisitos Previos

1. **LTspice** (XVII o v24+) instalado en el sistema.
2. **Python 3.8+** con las siguientes bibliotecas instaladas:

```bash
pip install PyLTSpice pandas openpyxl
```

---

## 🚀 Guía de Uso

### 1. Configurar la simulación en LTspice
Abrí el archivo `ltspice/amplificador_tp2.asc` en LTspice y dejá activa únicamente la directiva de análisis que desees ejecutar:
* `.op` para Punto de Operación CC y Potencias.
* `.ac` para Respuesta en Frecuencia e Impedancias.
* `.tran` para Análisis Transitorio y Distorsión (THD).
* `.noise` para Análisis de Ruido (PSD).

*(Las directivas inactivas deben estar comentadas con `;`).*

> **Nota sobre `mediciones.txt`:** Si en algún momento modificás o borrás sin querer las directivas `.meas` del esquemático en LTspice, podés abrir `ltspice/mediciones.txt` para copiar el bloque original de comandos y pegarlo nuevamente en la ventana de directivas de LTspice (`S`).

### 2. Ejecutar la simulación
Desde la terminal en la raíz del repositorio, ejecutá:

```bash
python python/run_simulations.py
```
Este script invoca el ejecutable de LTspice en modo *batch* (`-b`), ejecuta la simulación activa y actualiza el archivo de reporte `amplificador_tp2.log`.

### 3. Visualizar o Exportar Mediciones

* **Para ver los resultados rápido en la terminal:**
  ```bash
  python python/parse_log.py
  ```
  Este script lee `amplificador_tp2.log` e imprime una tabla resumida directamente en consola.

* **Para exportar a una planilla Excel:**
  ```bash
  python python/generate_sheets_tables.py
  ```
  El script leerá el archivo `.log` y creará/actualizará automáticamente el archivo `docs/Resultados_Simulacion.xlsx`.

---

## 🔧 Personalización y Extensión de Mediciones

### Agregar nuevas directivas `.meas`
Podés agregar nuevos comandos `.meas` directamente en el esquemático de LTspice (por ejemplo, para medir corrientes en ramas específicas, potencias de resistores o tensiones diferenciales):
```spice
.meas op IC_Q1 find I(Cc1)
.meas tran Vout_rms RMS V(vout)
```
Al volver a correr `parse_log.py` o `generate_sheets_tables.py`, los scripts detectarán automáticamente los nuevos parámetros.

### Barridos Paramétricos (`.step`)
Si agregás directivas de barrido paramétrico en LTspice (por ejemplo, `.step param RL list 4 8 16` o variación de temperatura `.step temp 0 50 25`), los scripts procesarán cada *step* de la simulación y mostrarán/exportarán una fila por cada iteración.
