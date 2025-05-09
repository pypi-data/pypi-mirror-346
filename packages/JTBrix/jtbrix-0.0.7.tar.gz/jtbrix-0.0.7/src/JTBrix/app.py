import os
import time
import threading
import webbrowser
from pathlib import Path
from typing import Tuple

from flask import Flask, request, jsonify

import JTBrix
from JTBrix import screen_config
from JTBrix.screen_config import flow_config
from JTBrix.ui.main import ui, submitted_results
from JTBrix.questionnaire.screens import screens
from JTBrix.utils import find_free_port 
from JTBrix import  detect_environment

from JTBrix.utils.config import read_experiment_config
from JTBrix.utils.results import build_full_structured_result, get_combined_results
from JTBrix.io.saving import save_structured_output
from JTBrix.experiment.run_experiment import  run_test_local #, run_test_colab

from JTBrix.utils.paths import get_project_paths
paths = get_project_paths()
template_path = paths["template_path"]
config_path = paths["config_path"]
static_path = paths["static_path"]
results_path = paths["results_path"]




def run():
    sys = detect_environment()
    print (f"Detected environment: {sys}")

    config, order = read_experiment_config(config_path)
    print("CONFIG:\n", config)
    print("\nSELECTED ORDER:", order)

    # Set up global config
    from JTBrix import screen_config
    screen_config.flow_config = config
    submitted_results.clear()

    # Create the app
    app = Flask(__name__, static_folder=static_path, template_folder=template_path)
    app.register_blueprint(ui)
    app.register_blueprint(screens)

    if sys in ("macOS", "Windows"):
        run_test_local(app,config, order, timeout=600)

    # elif sys == "Google Colab":
    #    run_test_colab(app,config, order, timeout=600)


if __name__ == "__main__": 
    run()





