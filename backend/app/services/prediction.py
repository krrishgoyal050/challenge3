def linear_regression_forecast(values: list[float], horizon: int = 7) -> list[float]:
    if not values:
        return [0.0] * horizon
    if len(values) == 1:
        return [round(values[0], 2)] * horizon

    n = len(values)
    xs = list(range(n))
    x_mean = sum(xs) / n
    y_mean = sum(values) / n
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, values))
    denominator = sum((x - x_mean) ** 2 for x in xs) or 1
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    return [round(max(0.0, intercept + slope * (n + i)), 2) for i in range(horizon)]


def forecast_goal_completion(current: float, target: float, days_elapsed: int, days_total: int) -> float:
    if target <= 0:
        return 100.0
    if days_elapsed <= 0:
        projected = current
    else:
        projected = (current / days_elapsed) * max(days_total, 1)
    return round(min(100.0, projected / target * 100), 2)
