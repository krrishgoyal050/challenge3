from functools import lru_cache


class CarbonFactorStore:
    """Hash-map based O(1) carbon factor lookup and preference cache."""

    def __init__(self) -> None:
        self._factors: dict[str, float] = {
            "car:km": 0.192,
            "bus:km": 0.089,
            "train:km": 0.041,
            "flight:km": 0.255,
            "electricity:kwh": 0.475,
            "natural_gas:kwh": 0.184,
            "beef:kg": 27.0,
            "chicken:kg": 6.9,
            "vegetarian_meal:serving": 1.7,
            "vegan_meal:serving": 1.0,
            "clothing:item": 25.0,
            "electronics:item": 120.0,
            "landfill_waste:kg": 0.57,
            "recycled_waste:kg": 0.05,
        }
        self._preference_cache: dict[int, dict[str, str | float | bool]] = {}

    def lookup(self, activity_type: str, unit: str) -> float:
        return self._factors.get(f"{activity_type.lower()}:{unit.lower()}", 1.0)

    def set_preference(self, user_id: int, key: str, value: str | float | bool) -> None:
        self._preference_cache.setdefault(user_id, {})[key] = value

    def get_preference(self, user_id: int, key: str) -> str | float | bool | None:
        return self._preference_cache.get(user_id, {}).get(key)


@lru_cache
def get_factor_store() -> CarbonFactorStore:
    return CarbonFactorStore()
