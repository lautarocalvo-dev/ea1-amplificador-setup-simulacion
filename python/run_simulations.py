import os
import subprocess
import shutil

# Rutas relativas dinámicas basadas en la carpeta del repositorio
script_dir = os.path.dirname(os.path.abspath(__file__))
ltspice_dir = os.path.abspath(os.path.join(script_dir, '..', 'ltspice'))
netlist_path = os.path.join(ltspice_dir, 'amplificador_tp2.asc')

def find_ltspice():
    """Busca el ejecutable de LTspice en las ubicaciones habituales de Windows."""
    # 1. Buscar si está declarado en las variables del sistema (PATH)
    for exe_name in ['LTspice', 'XVIIexecutable', 'LTspiceXVII']:
        path = shutil.which(exe_name)
        if path:
            return path
            
    # 2. Rutas por defecto en Windows (LTspice 17+ y XVII, en Program Files y AppData)
    user_home = os.path.expanduser("~")
    standard_paths = [
        r"C:\Program Files\ADI\LTspice\LTspice.exe",
        r"C:\Program Files\LTC\LTspiceXVII\XVIIexecutable.exe",
        os.path.join(user_home, r"AppData\Local\Programs\ADI\LTspice\LTspice.exe"),
        os.path.join(user_home, r"AppData\Local\LTspice\LTspice.exe")
    ]
    
    for path in standard_paths:
        if os.path.exists(path):
            return path
            
    return None

ltspice_exe = find_ltspice()

if not ltspice_exe:
    print("Error: No se encontró LTspice instalado en la máquina.")
else:
    print(f"Ejecutable detectado: {ltspice_exe}")
    print(f"Ejecutando simulación para: {netlist_path}")
    
    cmd = [ltspice_exe, "-b", netlist_path]
    try:
        subprocess.run(cmd, check=True)
        print("¡Simulación completada con éxito! Archivo .log actualizado.")
    except Exception as e:
        print(f"Error al ejecutar la simulación: {e}")