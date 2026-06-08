export type Dashboard = {
  total_kg: number;
  carbon_score: number;
  breakdown: { category: string; emission_kg: number }[];
  trend: number[];
  spikes: number[];
  forecast_next_7_days: number[];
};

export type Recommendation = {
  title: string;
  description: string;
  category: string;
  impact_kg: number;
  effort: number;
  priority_score: number;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init?.headers
    }
  });
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json() as Promise<T>;
}

export const demoDashboard: Dashboard = {
  total_kg: 348.4,
  carbon_score: 82,
  breakdown: [
    { category: "transport", emission_kg: 116.2 },
    { category: "energy", emission_kg: 91.7 },
    { category: "food", emission_kg: 74.6 },
    { category: "shopping", emission_kg: 48.9 },
    { category: "waste", emission_kg: 17.0 }
  ],
  trend: [9, 8, 7, 11, 10, 8, 7, 9, 13, 8, 7, 6, 8, 9, 7, 6, 6, 10, 8, 7, 5, 6, 8, 7, 6, 5, 7, 6, 5, 4],
  spikes: [8, 17],
  forecast_next_7_days: [5.7, 5.5, 5.3, 5.1, 4.9, 4.7, 4.5]
};

export const demoRecommendations: Recommendation[] = [
  {
    title: "Pause non-essential purchases",
    description: "Use a 7-day cooling period and buy used where possible.",
    category: "shopping",
    impact_kg: 12,
    effort: 1,
    priority_score: 12
  },
  {
    title: "Plan three plant-forward meals",
    description: "Replace high-carbon meals with legumes, grains, and seasonal produce.",
    category: "food",
    impact_kg: 10,
    effort: 2,
    priority_score: 5
  },
  {
    title: "Swap two car trips",
    description: "Use transit, cycling, or trip chaining twice this week.",
    category: "transport",
    impact_kg: 8.5,
    effort: 2,
    priority_score: 4.25
  }
];
