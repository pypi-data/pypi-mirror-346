import re
from typing import Dict, List


def analyze_content(content: str, patterns: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Analyze content for sensitive information using provided patterns.
    Returns a dictionary with pattern types and their matches.
    """
    results = {}
    for pattern_name, pattern in patterns.items():
        matches = re.finditer(pattern, content)
        found_matches = [match.group(0) for match in matches]
        if found_matches:
            results[pattern_name] = found_matches
    return results
