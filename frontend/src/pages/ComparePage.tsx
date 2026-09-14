import { useState } from "react";
import { runComparison, submitFeedback } from "../api/client";
import { ComparisonSummary } from "../components/ComparisonSummary";
import { PromptForm } from "../components/PromptForm";
import { ResultCard } from "../components/ResultCard";
import type { ComparisonResponse, Rating } from "../types";

export function ComparePage() {
  const [comparison, setComparison] = useState<ComparisonResponse | null>(null);
  const [ratings, setRatings] = useState<Record<number, Rating>>({});
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleRun(prompt: string, models: string[]) {
    setIsRunning(true);
    setError(null);
    try {
      const result = await runComparison(prompt, models);
      setComparison(result);
      setRatings({});
    } catch (err) {
      setError(err instanceof Error ? err.message : "Comparison failed");
    } finally {
      setIsRunning(false);
    }
  }

  async function handleRate(modelRunId: number, rating: Rating) {
    setRatings((prev) => ({ ...prev, [modelRunId]: rating }));
    try {
      await submitFeedback(modelRunId, rating);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save rating");
    }
  }

  return (
    <div>
      <h1>Compare AI Models</h1>
      <PromptForm onRun={handleRun} isRunning={isRunning} />

      {error && <p className="error">{error}</p>}

      {comparison && (
        <>
          <div className="results-grid">
            {comparison.runs.map((run) => (
              <ResultCard
                key={run.model_run_id}
                result={run}
                rating={ratings[run.model_run_id] ?? null}
                onRate={handleRate}
              />
            ))}
          </div>
          <ComparisonSummary results={comparison.runs} ratings={ratings} />
        </>
      )}
    </div>
  );
}
