def moving_average(values: list[float], window: int) -> list[float]:
    if window <= 0:
        raise ValueError("window must be positive")
    totals: list[float] = []
    current = 0.0
    for idx, value in enumerate(values):
        current += value
        if idx >= window:
            current -= values[idx - window]
        totals.append(current / min(idx + 1, window))
    return totals


def detect_spikes(values: list[float], window: int = 7, threshold_multiplier: float = 1.5) -> list[int]:
    averages = moving_average(values, window)
    return [
        idx
        for idx, value in enumerate(values)
        if idx > 0 and averages[idx - 1] > 0 and value > averages[idx - 1] * threshold_multiplier
    ]
