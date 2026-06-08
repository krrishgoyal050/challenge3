"use client";

import type React from "react";
import { useMemo, useState } from "react";
import { Activity, Award, BarChart3, Bot, CheckCircle2, Leaf, Send, Target, Zap } from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

import { apiFetch, demoDashboard, demoRecommendations, type Dashboard, type Recommendation } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

const palette = ["#236b4b", "#386fa4", "#8a6f2a", "#9b3d35", "#5a6670"];

export default function Home() {
  const [dashboard, setDashboard] = useState<Dashboard>(demoDashboard);
  const [recommendations, setRecommendations] = useState<Recommendation[]>(demoRecommendations);
  const [assistantAnswer, setAssistantAnswer] = useState(
    "Ask for a plan and I will combine your history, goals, and the ranked recommendation engine."
  );
  const [form, setForm] = useState({
    category: "transport",
    activity_type: "car",
    quantity: "30",
    unit: "km",
    occurred_on: new Date().toISOString().slice(0, 10)
  });

  const trendData = useMemo(
    () => dashboard.trend.map((value, index) => ({ day: index + 1, kg: value, spike: dashboard.spikes.includes(index) })),
    [dashboard]
  );

  async function refreshData() {
    try {
      const [nextDashboard, nextRecommendations] = await Promise.all([
        apiFetch<Dashboard>("/activities/dashboard"),
        apiFetch<Recommendation[]>("/recommendations")
      ]);
      setDashboard(nextDashboard);
      setRecommendations(nextRecommendations);
    } catch {
      setDashboard(demoDashboard);
      setRecommendations(demoRecommendations);
    }
  }

  async function submitActivity(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      await apiFetch("/activities", {
        method: "POST",
        body: JSON.stringify({ ...form, quantity: Number(form.quantity) })
      });
      await refreshData();
    } catch {
      const emission = Number(form.quantity) * 0.192;
      setDashboard((current) => ({
        ...current,
        total_kg: Number((current.total_kg + emission).toFixed(1)),
        carbon_score: Math.max(0, current.carbon_score - 1)
      }));
    }
  }

  async function askAssistant(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const message = String(data.get("message") ?? "");
    if (!message.trim()) return;
    try {
      const response = await apiFetch<{ answer: string; recommendations: Recommendation[] }>("/recommendations/assistant", {
        method: "POST",
        body: JSON.stringify({ message })
      });
      setAssistantAnswer(response.answer);
      setRecommendations(response.recommendations);
    } catch {
      setAssistantAnswer("Start with the highest savings per effort: reduce discretionary shopping, swap two car trips, and plan plant-forward meals this week.");
    }
    event.currentTarget.reset();
  }

  return (
    <main className="min-h-screen">
      <header className="border-b border-line bg-white">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-md bg-primary text-white">
              <Leaf aria-hidden="true" />
            </span>
            <div>
              <h1 className="text-xl font-bold">Carbon Footprint Awareness Platform</h1>
              <p className="text-sm text-slate-600">Track, predict, and reduce emissions with AI-guided plans.</p>
            </div>
          </div>
          <Button type="button" onClick={refreshData} aria-label="Refresh dashboard data">
            <Activity size={18} aria-hidden="true" /> Refresh
          </Button>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-5 px-4 py-6 sm:px-6 lg:grid-cols-[1.35fr_0.65fr] lg:px-8">
        <section className="space-y-5" aria-label="Carbon analytics dashboard">
          <div className="grid gap-4 md:grid-cols-4">
            <Metric icon={<BarChart3 />} label="Carbon score" value={`${dashboard.carbon_score}/100`} />
            <Metric icon={<Zap />} label="Total emissions" value={`${dashboard.total_kg} kg`} />
            <Metric icon={<Target />} label="Forecast trend" value={`${dashboard.forecast_next_7_days.at(-1)} kg/day`} />
            <Metric icon={<Award />} label="Current level" value="Carbon Cutter" />
          </div>

          <Card>
            <div className="mb-4 flex items-center justify-between gap-3">
              <h2 className="text-lg font-semibold">30-Day Emission Trend</h2>
              <span className="rounded-md bg-[#fff7df] px-3 py-1 text-sm text-[#6f4c00]">{dashboard.spikes.length} spikes detected</span>
            </div>
            <div className="h-72" role="img" aria-label="Area chart showing the last 30 days of carbon emissions">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trendData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#d9e2da" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Area type="monotone" dataKey="kg" stroke="#236b4b" fill="#9fd0b4" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </Card>

          <div className="grid gap-5 lg:grid-cols-2">
            <Card>
              <h2 className="mb-4 text-lg font-semibold">Emission Breakdown</h2>
              <div className="h-72" role="img" aria-label="Bar chart showing emissions by category">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={dashboard.breakdown}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#d9e2da" />
                    <XAxis dataKey="category" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="emission_kg">
                      {dashboard.breakdown.map((entry, index) => (
                        <Cell key={entry.category} fill={palette[index % palette.length]} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>

            <Card>
              <h2 className="mb-4 text-lg font-semibold">Carbon Calculator</h2>
              <form className="grid gap-3" onSubmit={submitActivity}>
                <label className="grid gap-1 text-sm font-medium">
                  Category
                  <select
                    className="min-h-10 rounded-md border border-line px-3"
                    value={form.category}
                    onChange={(event) => setForm({ ...form, category: event.target.value })}
                  >
                    <option value="transport">Transport</option>
                    <option value="energy">Energy</option>
                    <option value="food">Food</option>
                    <option value="shopping">Shopping</option>
                    <option value="waste">Waste</option>
                  </select>
                </label>
                <label className="grid gap-1 text-sm font-medium">
                  Activity type
                  <Input value={form.activity_type} onChange={(event) => setForm({ ...form, activity_type: event.target.value })} />
                </label>
                <div className="grid gap-3 sm:grid-cols-3">
                  <label className="grid gap-1 text-sm font-medium">
                    Quantity
                    <Input type="number" min="0.1" step="0.1" value={form.quantity} onChange={(event) => setForm({ ...form, quantity: event.target.value })} />
                  </label>
                  <label className="grid gap-1 text-sm font-medium">
                    Unit
                    <Input value={form.unit} onChange={(event) => setForm({ ...form, unit: event.target.value })} />
                  </label>
                  <label className="grid gap-1 text-sm font-medium">
                    Date
                    <Input type="date" value={form.occurred_on} onChange={(event) => setForm({ ...form, occurred_on: event.target.value })} />
                  </label>
                </div>
                <Button type="submit">
                  <CheckCircle2 size={18} aria-hidden="true" /> Log activity
                </Button>
              </form>
            </Card>
          </div>
        </section>

        <aside className="space-y-5" aria-label="AI recommendations and goals">
          <Card>
            <h2 className="mb-3 flex items-center gap-2 text-lg font-semibold">
              <Bot size={20} aria-hidden="true" /> AI Sustainability Assistant
            </h2>
            <p className="mb-4 rounded-md bg-[#eef5f8] p-3 text-sm leading-6 text-slate-700" aria-live="polite">
              {assistantAnswer}
            </p>
            <form className="flex gap-2" onSubmit={askAssistant}>
              <Input name="message" aria-label="Message for assistant" placeholder="Create a weekly reduction plan" />
              <Button type="submit" aria-label="Send message">
                <Send size={18} aria-hidden="true" />
              </Button>
            </form>
          </Card>

          <Card>
            <h2 className="mb-4 text-lg font-semibold">Ranked Recommendations</h2>
            <div className="space-y-3">
              {recommendations.map((item) => (
                <article key={item.title} className="rounded-md border border-line p-3">
                  <div className="flex items-start justify-between gap-3">
                    <h3 className="font-semibold">{item.title}</h3>
                    <span className="rounded-md bg-[#e6f1eb] px-2 py-1 text-xs font-semibold text-primary">{item.impact_kg} kg</span>
                  </div>
                  <p className="mt-1 text-sm leading-6 text-slate-600">{item.description}</p>
                </article>
              ))}
            </div>
          </Card>

          <Card>
            <h2 className="mb-4 text-lg font-semibold">Goals & Challenges</h2>
            <div className="space-y-4">
              <Progress title="Monthly reduction goal" value={68} />
              <Progress title="Low-carbon commute week" value={60} />
              <Progress title="Plant-forward dinners" value={33} />
            </div>
          </Card>
        </aside>
      </div>
    </main>
  );
}

function Metric({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <Card className="p-4">
      <div className="mb-3 text-primary" aria-hidden="true">
        {icon}
      </div>
      <p className="text-sm text-slate-600">{label}</p>
      <p className="mt-1 text-2xl font-bold">{value}</p>
    </Card>
  );
}

function Progress({ title, value }: { title: string; value: number }) {
  return (
    <div>
      <div className="mb-1 flex justify-between gap-3 text-sm">
        <span className="font-medium">{title}</span>
        <span>{value}%</span>
      </div>
      <div className="h-3 rounded-md bg-[#e8ece7]" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={value} aria-label={title}>
        <div className="h-3 rounded-md bg-accent" style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}
