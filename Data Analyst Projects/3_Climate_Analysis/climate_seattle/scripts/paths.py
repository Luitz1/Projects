# scripts/paths.py
from pathlib import Path

class Paths:
    """Rutas del proyecto organizadas desde la raíz"""

    # Principal
    ROOT_DIR = Path(__file__).resolve().parents[1]

    # Subfolder
    DATA = ROOT_DIR / "data"
    DATA_RAW = DATA / "raw"
    DATA_PROCESSED = DATA / "processed"
    DATA_EXTERNAL = DATA / "external"

    # Notebooks, scripts and model paths
    NOTEBOOKS_DIR = ROOT_DIR / "notebooks"
    MODELS_DIR = ROOT_DIR / "models"
    SCRIPTS_DIR = ROOT_DIR / "scripts"
    TOOLS_DIR = SCRIPTS_DIR / "py_tools"

    #Outputs paths
    OUT_DIR = ROOT_DIR / "outputs"
    OUT_FIGURES = OUT_DIR / "figures"
    OUT_REPORTS = OUT_DIR / "reports"

    # Otros Directorios
    README = ROOT_DIR / "README.md"
    REQUIREMENTS = ROOT_DIR / "requeriments.txt"


    @classmethod
    def summary(cls):
        """Devuelve un resumen de todas las rutas declaradas"""
        return {
            attr: getattr(cls, attr)
            for attr in dir(cls)
            if not attr.startswith("__") and isinstance(getattr(cls, attr), Path)
        }

    @classmethod
    def print_summary(cls):
        """Imprime todas las rutas disponibles"""
        for name, path in cls.summary().items():
            print(f"{name:15}: {path}")