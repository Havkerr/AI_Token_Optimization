import type {
  ComparisonResponse,
  DashboardSummary,
  HistoryEntry,
  Rating,
} from "../types";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`${response.status} ${response.statusText}: ${body}`);
  }
  return response.json() as Promise<T>;
}

export function runComparison(
  prompt: string,
  models: string[],
): Promise<ComparisonResponse> {
  return request("/api/comparisons", {
    method: "POST",
    body: JSON.stringify({ prompt, models }),
  });
}

export function submitFeedback(
  modelRunId: number,
  rating: Rating,
): Promise<void> {
  return request("/api/feedback", {
    method: "POST",
    body: JSON.stringify({ model_run_id: modelRunId, rating }),
  });
}

export function getDashboardSummary(): Promise<DashboardSummary> {
  return request("/api/dashboard/summary");
}

export function getDashboardHistory(): Promise<HistoryEntry[]> {
  return request("/api/dashboard/history");
}
