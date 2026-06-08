import heapq
from dataclasses import dataclass, field


@dataclass(order=True)
class RankedRecommendation:
    rank: float
    title: str = field(compare=False)
    description: str = field(compare=False)
    category: str = field(compare=False)
    impact_kg: float = field(compare=False)
    effort: float = field(compare=False)

    @property
    def priority_score(self) -> float:
        return -self.rank


class RecommendationHeap:
    """Max-priority queue implemented with heapq and negated ranks."""

    def __init__(self) -> None:
        self._items: list[RankedRecommendation] = []

    def push(self, title: str, description: str, category: str, impact_kg: float, effort: float) -> None:
        score = impact_kg / max(effort, 0.1)
        heapq.heappush(self._items, RankedRecommendation(-score, title, description, category, impact_kg, effort))

    def pop_top(self, limit: int) -> list[RankedRecommendation]:
        return [heapq.heappop(self._items) for _ in range(min(limit, len(self._items)))]
