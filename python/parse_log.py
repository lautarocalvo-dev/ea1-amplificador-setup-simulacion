import os
from PyLTSpice import LTSpiceLogReader

script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.abspath(os.path.join(script_dir, '..', 'ltspice', 'amplificador_tp2.log'))

print("=== EXTRACCIÓN AUTOMÁTICA DE RESULTADOS (.LOG) ===\n")

if not os.path.exists(log_path):
    print(f"No se encontró el archivo: {log_path}")
else:
    log = LTSpiceLogReader(log_path)
    measures = log.get_measure_names()
    
    print(f"{'PARÁMETRO (.meas)':<25} | {'STEP / ITERACIÓN':<18} | {'VALOR OBTENIDO':<25}")
    print("-" * 72)
    
    # Obtener la cantidad total de pasos simulados
    step_count = log.step_count if hasattr(log, 'step_count') and log.step_count > 0 else 1
    
    for measure in measures:
        if step_count > 1:
            for step_idx in range(step_count):
                try:
                    val = log.get_measure_value(measure, step=step_idx)
                    print(f"{measure:<25} | Step {step_idx + 1:<13} | {val}")
                except Exception as e:
                    print(f"{measure:<25} | Step {step_idx + 1:<13} | Error: {e}")
        else:
            try:
                val = log.get_measure_value(measure)
                print(f"{measure:<25} | N/A                | {val}")
            except Exception:
                val = log.get_measure_value(measure, step=0)
                print(f"{measure:<25} | Step 1             | {val}")