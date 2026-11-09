import re
from typing import Tuple, List

# Patterns matching sensitive secrets across source code and communications
SECRET_PATTERNS = [
    (r'(?i)(api[_-]?key\s*[:=]\s*["\']?)([\w\-]{20,})', "API_KEY"),
    (r'(?i)(bearer\s+)([a-zA-Z0-9_\-\.]{25,})', "BEARER_TOKEN"),
    (r'(?i)(ghp_[a-zA-Z0-9]{36})', "GITHUB_PAT"),
    (r'(?i)(password\s*[:=]\s*["\']?)([^"\'\s]{6,})', "PASSWORD"),
    (r'(?i)(secret[_-]?key\s*[:=]\s*["\']?)([\w\-]{16,})', "SECRET_KEY"),
    (r'(?i)(postgres(?:ql)?:\/\/[^:]+:)([^@]+)(@)', "DB_PASSWORD"),
    (r'(?i)(mongodb(?:\+srv)?:\/\/[^:]+:)([^@]+)(@)', "DB_PASSWORD"),
]

def sanitize_content(raw_text: str) -> Tuple[str, int, List[str]]:
    """
    Scans raw source text and replaces sensitive credentials with safe redaction tokens.
    Returns: (sanitized_text, count_of_redactions, list_of_redacted_types)
    """
    sanitized = raw_text
    total_redactions = 0
    detected_types = []

    for pattern, secret_type in SECRET_PATTERNS:
        matches = list(re.finditer(pattern, sanitized))
        if matches:
            total_redactions += len(matches)
            detected_types.append(secret_type)
            
            # Special replacement for DB connection strings to preserve the host/user format
            if secret_type == "DB_PASSWORD":
                sanitized = re.sub(pattern, r'\g<1>[REDACTED_DB_PASS]\g<3>', sanitized)
            elif secret_type == "GITHUB_PAT":
                sanitized = re.sub(pattern, f'[REDACTED_{secret_type}]', sanitized)
            else:
                sanitized = re.sub(pattern, rf'\g<1>[REDACTED_{secret_type}]', sanitized)

    return sanitized, total_redactions, list(set(detected_types))
