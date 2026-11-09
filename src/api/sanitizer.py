import json

SENSITIVE_KEYS = frozenset(
    {
        # Authentication / Credentials
        "password",
        "accessToken",
        "refreshToken",
        # Personal information (PII)
        "email",
        "firstName",
        "lastName",
        "address",
        "shippingFirstName",
        "shippingLastName",
        "shippingAddress",
        # Payment information (PCI)
        "cardNumber",
        "expiryDate",
        "cvv",
        "cardholderName",
        "paymentLastFour",
    }
)

_LOWER_SENSITIVE_KEYS = frozenset(key.lower() for key in SENSITIVE_KEYS)


def sanitize_response_body(body: str) -> str:
    """Mask sensitive values in a JSON response body.

    Keys are matched case-insensitively. Non-JSON and empty bodies are returned
    unchanged.
    """
    if not body:
        return body

    try:
        data = json.loads(body)
    except TypeError, ValueError:
        return body

    _mask_sensitive_data(data)

    return json.dumps(data)


def _mask_sensitive_data(data: object) -> None:
    """Recursively mask sensitive values in dictionaries and lists."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(key, str) and key.lower() in _LOWER_SENSITIVE_KEYS:
                data[key] = "****"
            else:
                _mask_sensitive_data(value)

    elif isinstance(data, list):
        for item in data:
            _mask_sensitive_data(item)
