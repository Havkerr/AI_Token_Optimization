import type { ModelRunResult, Rating } from "../types";

interface Props {
  result: ModelRunResult;
  rating: Rating | null;
  onRate: (modelRunId: number, rating: Rating) => void;
}

export function ResultCard({ result, rating, onRate }: Props) {
  return (
    <div className="result-card">
      <h3>{result.model_name}</h3>

      {result.status === "error" ? (
        <p className="error">Error: {result.error_message}</p>
      ) : (
        <p className="response-text">{result.response_text}</p>
      )}

      <dl>
        <dt>Input tokens</dt>
        <dd>{result.input_tokens}</dd>
        <dt>Output tokens</dt>
        <dd>{result.output_tokens}</dd>
        <dt>Total tokens</dt>
        <dd>{result.total_tokens}</dd>
        <dt>Estimated cost</dt>
        <dd>${result.estimated_cost.toFixed(6)}</dd>
        <dt>Latency</dt>
        <dd>{result.latency_ms.toFixed(0)} ms</dd>
      </dl>

      {result.status === "success" && (
        <div className="rating">
          <button
            className={rating === "good" ? "active" : ""}
            onClick={() => onRate(result.model_run_id, "good")}
          >
            Good
          </button>
          <button
            className={rating === "bad" ? "active" : ""}
            onClick={() => onRate(result.model_run_id, "bad")}
          >
            Bad
          </button>
        </div>
      )}
    </div>
  );
}
