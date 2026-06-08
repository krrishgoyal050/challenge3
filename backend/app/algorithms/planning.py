from dataclasses import dataclass


@dataclass(frozen=True)
class ActionOption:
    title: str
    carbon_saving_kg: float
    effort_hours: int


def optimize_plan(options: list[ActionOption], effort_budget_hours: int) -> list[ActionOption]:
    """0/1 knapsack DP for weekly or monthly sustainability plan optimization."""
    n = len(options)
    dp = [[0.0] * (effort_budget_hours + 1) for _ in range(n + 1)]

    for i, option in enumerate(options, start=1):
        for budget in range(effort_budget_hours + 1):
            dp[i][budget] = dp[i - 1][budget]
            if option.effort_hours <= budget:
                dp[i][budget] = max(
                    dp[i][budget],
                    dp[i - 1][budget - option.effort_hours] + option.carbon_saving_kg,
                )

    chosen: list[ActionOption] = []
    budget = effort_budget_hours
    for i in range(n, 0, -1):
        if dp[i][budget] != dp[i - 1][budget]:
            option = options[i - 1]
            chosen.append(option)
            budget -= option.effort_hours
    return list(reversed(chosen))


def greedy_quick_wins(options: list[ActionOption], limit: int = 3) -> list[ActionOption]:
    return sorted(options, key=lambda option: option.carbon_saving_kg / max(option.effort_hours, 1), reverse=True)[:limit]
