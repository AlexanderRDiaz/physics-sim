def Clamp(value: int | float, minimum: int | float, maximum: int | float) -> int | float:
    if minimum == maximum:
        return minimum

    if minimum > maximum:
        raise RuntimeError('Minimum is greater than the maximum!')

    if value < minimum:
        return minimum

    if value > maximum:
        return maximum

    return value
