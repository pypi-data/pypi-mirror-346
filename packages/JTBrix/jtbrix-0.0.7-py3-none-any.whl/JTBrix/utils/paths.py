from JTBrix.utils.env_info import detect_environment
import JTBrix

from pathlib import Path
import platform

def get_project_paths():
    sys = detect_environment()

    if sys == "Google Colab":
        root = Path("/content/JTBrix/src/JTBrix/")  # Adjust as needed
    elif sys in ("macOS", "Windows", "Linux"):
        root = Path(JTBrix.__file__).parent
    else:
        raise RuntimeError(f"Unsupported operating system: {sys}")

    static = root / "data" / "static"
    templates = root / "templates"
    config = root / "data" / "config.yml"
    results = root / "data" / "results"

    for path_name, path in [("root", root), ("static", static), ("templates", templates), ("config", config), ("results", results)]:
        if not path.exists():
            raise RuntimeError(f"{path_name.capitalize()} path {path} does not exist.")

    return {
        "root": root,
        "static_path": static,
        "template_path": templates,
        "config_path": config,
        "results_path": results
    }