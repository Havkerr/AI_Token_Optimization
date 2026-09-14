import { useEffect, useState } from "react";
import { getDashboardHistory, getDashboardSummary } from "../api/client";
import { DashboardSummary } from "../components/DashboardSummary";
import { HistoryTable } from "../components/HistoryTable";
import type { DashboardSummary as DashboardSummaryType, HistoryEntry } from "../types";

export function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummaryType | null>(null);
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([getDashboardSummary(), getDashboardHistory()])
      .then(([summaryData, historyData]) => {
        setSummary(summaryData);
        setHistory(historyData);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load dashboard"));
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      {error && <p className="error">{error}</p>}
      {summary && <DashboardSummary summary={summary} />}
      <h2>History</h2>
      <HistoryTable entries={history} />
    </div>
  );
}
