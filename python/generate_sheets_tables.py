import os
import pandas as pd
from PyLTSpice import LTSpiceLogReader

# 1. Rutas del proyecto
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.abspath(os.path.join(script_dir, '..', 'ltspice', 'amplificador_tp2.log'))

# Definir la carpeta de salida en 'docs/' en la raíz del repositorio
docs_dir = os.path.abspath(os.path.join(script_dir, '..', 'docs'))
os.makedirs(docs_dir, exist_ok=True)  # Crea la carpeta 'docs' automáticamente si no existe

excel_path = os.path.join(docs_dir, 'Resultados_Simulacion.xlsx')

print("=== EXTRACCIÓN SIMPLE DE MEDICIONES (.LOG) A EXCEL ===\n")

if not os.path.exists(log_path):
    print(f"Error: No se encontró el archivo .log en: {log_path}")
    print("Asegurate de haber ejecutado la simulación primero en LTspice o con run_simulations.py")
    exit(1)

try:
    log = LTSpiceLogReader(log_path)
    measures = log.get_measure_names()
    
    records = []
    step_count = log.step_count if hasattr(log, 'step_count') and log.step_count > 0 else 1

    for measure in measures:
        if step_count > 1:
            for step_idx in range(step_count):
                try:
                    val = log.get_measure_value(measure, step=step_idx)
                    records.append({
                        "Parametro (.meas)": measure,
                        "Step / Iteracion": step_idx + 1,
                        "Valor Simulado": val
                    })
                except Exception as e:
                    records.append({
                        "Parametro (.meas)": measure,
                        "Step / Iteracion": step_idx + 1,
                        "Valor Simulado": f"Error: {e}"
                    })
        else:
            try:
                val = log.get_measure_value(measure)
                records.append({
                    "Parametro (.meas)": measure,
                    "Step / Iteracion": "N/A",
                    "Valor Simulado": val
                })
            except Exception:
                val = log.get_measure_value(measure, step=0)
                records.append({
                    "Parametro (.meas)": measure,
                    "Step / Iteracion": "1",
                    "Valor Simulado": val
                })

    # Crear DataFrame
    df = pd.DataFrame(records)

    # Imprimir en consola
    print(df.to_string(index=False))

    # Exportar a Excel
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Mediciones_Log", index=False)

    print(f"\n¡Mediciones exportadas con éxito a Excel! -> {excel_path}")
    print("Podés abrir este archivo o copiar su contenido a Google Sheets directamente.")

except Exception as e:
    print(f"Error al procesar el log: {e}")
