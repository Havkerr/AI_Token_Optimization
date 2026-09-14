import type { ModelRunResult, Rating } from "../types";

interface Props {
  results: ModelRunResult[];
  ratings: Record<number, Rating>;
}

function cheapestVsMostExpensive(successful: ModelRunResult[]): string | null {
  if (successful.length < 2) return null;
  const sorted = [...successful].sort((a, b) => a.estimated_cost - b.estimated_cost);
  const cheapest = sorted[0];
  const priciest = sorted[sorted.length - 1];
  if (priciest.estimated_cost === 0) return null;
  const pctCheaper = ((priciest.estimated_cost - cheapest.estimated_cost) / priciest.estimated_cost) * 100;
  return `${cheapest.model_name} was ${pctCheaper.toFixed(0)}% cheaper than ${priciest.model_name}.`;
}

export function ComparisonSummary({ results, ratings }: Props) {
  const successful = results.filter((r) => r.status === "success");
  if (successful.length === 0) return null;

  const cheapest = [...successful].sort((a, b) => a.estimated_cost - b.estimated_cost)[0];
  const fastest = [...successful].sort((a, b) => a.latency_ms - b.latency_ms)[0];
  const lowestTokens = [...successful].sort((a, b) => a.total_tokens - b.total_tokens)[0];

  const goodCounts = successful.reduce<Record<string, number>>((acc, r) => {
    if (ratings[r.model_run_id] === "good") {
      acc[r.model_name] = (acc[r.model_name] ?? 0) + 1;
    }
    return acc;
  }, {});
  const preferredEntry = Object.entries(goodCounts).sort((a, b) => b[1] - a[1])[0];

  const observation = cheapestVsMostExpensive(successful);

  return (
    <div className="comparison-summary">
      <h2>Summary</h2>
      <ul>
        <li>Cheapest model: {cheapest.model_name}</li>
        <li>Fastest model: {fastest.model_name}</li>
        <li>Lowest token usage: {lowestTokens.model_name}</li>
        <li>User-preferred model: {preferredEntry ? preferredEntry[0] : "Not rated yet"}</li>
      </ul>
      {observation && <p>{observation}</p>}
    </div>
  );
}
