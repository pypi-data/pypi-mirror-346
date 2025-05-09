import os
import time
import threading
import webbrowser
from pathlib import Path
from typing import Tuple

from JTBrix.screen_config import flow_config
from JTBrix.ui.main import ui, submitted_results
from JTBrix.utils.config import read_experiment_config
from JTBrix.utils import find_free_port 
from JTBrix.utils.results import build_full_structured_result, get_combined_results
from JTBrix.io.saving import save_structured_output
from JTBrix.utils.paths import get_project_paths

paths = get_project_paths()
template_path = paths["template_path"]
config_path = paths["config_path"]
static_path = paths["static_path"]
results_path = paths["results_path"]



def run_test_local(app, config, order, timeout= 600 ) :
    def run_app():
        app.run(port=port, debug=False, use_reloader=False)
    
    port = find_free_port()
    print ("Running on local machine")
    thread = threading.Thread(target=run_app)
    thread.daemon = True
    thread.start()
    start_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    webbrowser.open(f"http://127.0.0.1:{port}/experiment")
    print("Waiting for experiment to finish...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        if any(entry.get("finished") for entry in submitted_results):
            break
        time.sleep(1)
            # Collect and return
    duration_seconds = int(time.time() - start_time)
    results = get_combined_results(submitted_results)
    results["experiment_start"] = start_timestamp
    results["experiment_duration_sec"] = duration_seconds

    
    print("Combined results:", results)
    print("Execution order:", order)

    structured_output = build_full_structured_result(results, config_path, execution_order=order)
    print ("Structured output:", structured_output)
    print("Structured output keys:", structured_output.keys())
    print("Structured output values:", structured_output.values())
    save_structured_output(structured_output, save_path=results_path, name="Test_data")


# def run_test_colab(app, config, order, timeout= 600 ):
#     """
#     Runs the experiment in a Google Colab environment using ngrok to expose the Flask app.
#     """
#     port = find_free_port()
#     print ("Running on Google Colab")
#     from pyngrok import ngrok
#     ngrok.set_auth_token("2wjfqkOLdNnNEdW3TogJZxdKLNA_82gyNo4zcMGMUnTrFGnQP")
#     public_url = ngrok.connect(port)
#     print(f"🌍 App is publicly available at: {public_url}/experiment")

#     def run_app():
#         app.run(port=port, debug=False, use_reloader=False)

#     thread = threading.Thread(target=run_app)
#     thread.daemon = True
#     thread.start()
#     start_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
#     print("Waiting for experiment to finish...")
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         if any(entry.get("finished") for entry in submitted_results):
#             break
#         time.sleep(1)
#             # Collect and return
#     duration_seconds = int(time.time() - start_time)
#     results = get_combined_results(submitted_results)
#     results["experiment_start"] = start_timestamp
#     results["experiment_duration_sec"] = duration_seconds

    
#     print("Combined results:", results)
#     print("Execution order:", order)

#     structured_output = build_full_structured_result(results, config_path, execution_order=order)
#     print ("Structured output:", structured_output)
#     print("Structured output keys:", structured_output.keys())
#     print("Structured output values:", structured_output.values())
#     save_structured_output(structured_output, save_path=results_path, name="Test_data")
