"""Top-level package for JTBrix."""

__author__ = """Amid Nayerhoda"""
__email__ = 'Nayerhoda@infn.it'
__version__ = '0.0.6'


# Import core functionality to the top level
  # Example: if you have a main entry point
from JTBrix.questionnaire import screens   # Example: expose a core class
from JTBrix.ui import main  # Example: if you have a UI component
from JTBrix.screen_config import flow_config  # Example: if you have a configuration module
from JTBrix.utils.env_info import detect_environment
from JTBrix.utils import port  # Example: utility functions


from JTBrix.io import saving



__all__ = [
    "screens",
    "detect_environment",
    "port",
    "main",
    "flow_config",

]