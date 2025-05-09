import json
from typing import Dict


def load_patterns(config_path: str = "sensitive_data_detector/config.json") -> Dict[str, str]:
    """Load sensitive information patterns from config file.
    and return a dictionary of patterns"""
    with open(config_path, "r") as f:
        config = json.load(f)
    return config["sensitive_info"]  # {return dictionary of patterns}
