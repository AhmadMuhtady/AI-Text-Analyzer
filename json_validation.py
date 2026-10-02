def json_validation(result: dict) -> dict:
    target_keys = {"title", "main_topic", "summary", "sentiment"}

    if not isinstance(result, dict):
        raise TypeError(f"Result must be a dict, got {type(result).__name__}")

    actual_keys = set(result.keys())

    if actual_keys != target_keys:
        missing = target_keys - actual_keys
        extra = actual_keys - target_keys
        errors = []
        if missing:
            errors.append(f"missing key(s): {', '.join(sorted(missing))}")
        if extra:
            errors.append(f"unexpected key(s): {', '.join(sorted(extra))}")
        raise KeyError(f"Invalid keys in result ({'; '.join(errors)})")


    cleaned = {}
    for key, value in result.items():
        if not isinstance(value, str):
            raise TypeError(f"Value for '{key}' must be a string, got {type(value).__name__}")
        
        stripped_val = value.strip()
        if not stripped_val:
            raise ValueError(f"Value for '{key}' cannot be empty or whitespace-only")
        
        cleaned[key] = stripped_val


    allowed_sentiments = {"positive", "negative", "neutral"}
    sentiment_lower = cleaned["sentiment"].lower()
    if sentiment_lower not in allowed_sentiments:
        raise ValueError(
            f"Invalid sentiment '{cleaned['sentiment']}'. Expected one of: {', '.join(sorted(allowed_sentiments))}"
        )
    cleaned["sentiment"] = sentiment_lower

    return cleaned