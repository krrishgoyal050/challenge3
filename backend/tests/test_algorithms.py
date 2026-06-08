from app.algorithms.activity_graph import DEFAULT_GRAPH, bfs, dfs, dijkstra
from app.algorithms.carbon_factors import CarbonFactorStore
from app.algorithms.planning import ActionOption, greedy_quick_wins, optimize_plan
from app.algorithms.recommendation_heap import RecommendationHeap
from app.algorithms.trends import detect_spikes, moving_average
from app.services.prediction import linear_regression_forecast


def test_hash_map_factor_lookup_and_cache():
    store = CarbonFactorStore()
    assert store.lookup("car", "km") == 0.192
    store.set_preference(1, "diet", "vegetarian")
    assert store.get_preference(1, "diet") == "vegetarian"


def test_heap_ranks_by_impact_effort():
    heap = RecommendationHeap()
    heap.push("small", "x", "energy", 2, 2)
    heap.push("large", "x", "shopping", 12, 1)
    assert heap.pop_top(1)[0].title == "large"


def test_graph_algorithms_find_paths():
    assert bfs(DEFAULT_GRAPH, "transport")[0] == "transport"
    assert dfs(DEFAULT_GRAPH, "transport")[0] == "transport"
    distance, path = dijkstra(DEFAULT_GRAPH, "transport", "waste")
    assert distance == 3.5
    assert path == ["transport", "energy", "waste"]


def test_dp_and_greedy_planning():
    options = [ActionOption("a", 5, 3), ActionOption("b", 4, 2), ActionOption("c", 2, 1)]
    assert [item.title for item in optimize_plan(options, 3)] == ["b", "c"]
    assert greedy_quick_wins(options, 1)[0].title == "b"


def test_sliding_window_spike_detection_and_prediction():
    assert moving_average([2, 4, 6], 2) == [2, 3, 5]
    assert detect_spikes([1, 1, 1, 5], 3) == [3]
    assert linear_regression_forecast([1, 2, 3], 2) == [4, 5]
