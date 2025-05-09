import json
import os
from typing import Dict, Optional


def load_patterns(config_path: Optional[str] = None) -> Dict[str, str]:
    """Load sensitive information patterns from config file.
    and return a dictionary of patterns"""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r") as f:
        config = json.load(f)
    return config["sensitive_info"]  # {return dictionary of patterns}
