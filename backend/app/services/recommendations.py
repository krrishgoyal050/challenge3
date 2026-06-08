from app.algorithms.activity_graph import DEFAULT_GRAPH, bfs, dfs, dijkstra
from app.algorithms.planning import ActionOption, greedy_quick_wins, optimize_plan
from app.algorithms.recommendation_heap import RecommendationHeap, RankedRecommendation


def build_recommendations(breakdown: dict[str, float], limit: int = 5) -> list[RankedRecommendation]:
    heap = RecommendationHeap()
    if breakdown.get("transport", 0) > 0:
        heap.push("Swap two car trips", "Use transit, cycling, or trip chaining twice this week.", "transport", 8.5, 2)
    if breakdown.get("energy", 0) > 0:
        heap.push("Shift peak electricity use", "Run heavy appliances off peak and reduce thermostat load.", "energy", 6.0, 1.5)
    if breakdown.get("food", 0) > 0:
        heap.push("Plan three plant-forward meals", "Replace high-carbon meals with legumes, grains, and seasonal produce.", "food", 10.0, 2)
    if breakdown.get("shopping", 0) > 0:
        heap.push("Pause non-essential purchases", "Apply a 7-day cooling period and buy used where possible.", "shopping", 12.0, 1)
    if breakdown.get("waste", 0) > 0:
        heap.push("Separate recycling and compost", "Divert organics and recyclables from landfill streams.", "waste", 4.0, 1)
    heap.push("Quick home energy audit", "Find standby loads and seal the easiest leaks.", "energy", 5.0, 1)
    return heap.pop_top(limit)


def build_sustainability_plan() -> dict[str, object]:
    options = [
        ActionOption("Meal prep plant-forward lunches", 7.0, 2),
        ActionOption("Replace short car trips", 9.0, 3),
        ActionOption("Cold-water laundry", 2.5, 1),
        ActionOption("Repair before replacing", 11.0, 4),
        ActionOption("Compost food scraps", 3.5, 1),
    ]
    return {
        "weekly_plan": optimize_plan(options, effort_budget_hours=5),
        "quick_wins": greedy_quick_wins(options),
        "activity_bfs": bfs(DEFAULT_GRAPH, "transport"),
        "activity_dfs": dfs(DEFAULT_GRAPH, "transport"),
        "best_reduction_path": dijkstra(DEFAULT_GRAPH, "transport", "waste")[1],
    }
