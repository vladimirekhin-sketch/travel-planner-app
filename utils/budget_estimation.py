from __future__ import annotations
import math
from typing import List, Dict, Any

# Budget estimation utilities for travel planning
# (Copied from OSU-NLP-Group/TravelPlanner utils/budget_estimation.py)

class BudgetEstimator:
    def __init__(self, base_daily_cost: float = 100.0):
        self.base_daily_cost = base_daily_cost

    def estimate_trip_cost(self, days: int, city_multiplier: float = 1.0, travelers: int = 1, extras: Dict[str, float] | None = None) -> float:
        if days <= 0 or travelers <= 0:
            return 0.0
        extras_total = sum(extras.values()) if extras else 0.0
        return (self.base_daily_cost * city_multiplier * days * travelers) + extras_total

    def breakdown(self, days: int, city_multiplier: float = 1.0, travelers: int = 1, hotel_per_night: float | None = None, food_per_day: float | None = None, transport_total: float | None = None) -> Dict[str, float]:
        hotel = (hotel_per_night if hotel_per_night is not None else 70.0 * city_multiplier) * days
        food = (food_per_day if food_per_day is not None else 30.0 * city_multiplier) * days * travelers
        transport = transport_total if transport_total is not None else 50.0 * city_multiplier
        misc = max(0.1 * (hotel + food + transport), 15.0)
        return {
            'hotel': hotel,
            'food': food,
            'transport': transport,
            'misc': misc,
            'total': hotel + food + transport + misc
        }


def suggest_budget_tiers(total: float) -> Dict[str, float]:
    # Provide simple tier suggestions around the total estimate
    return {
        'conservative': max(total * 0.85, total - 200),
        'recommended': total,
        'comfortable': total * 1.25
    }


def per_person(total: float, travelers: int) -> float:
    return total / travelers if travelers > 0 else 0.0
