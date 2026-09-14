import type { DashboardSummary as DashboardSummaryType } from "../types";

interface Props {
  summary: DashboardSummaryType;
}

export function DashboardSummary({ summary }: Props) {
  return (
    <div className="dashboard-summary">
      <div>
        <span className="label">Total prompts</span>
        <span className="value">{summary.total_prompts}</span>
      </div>
      <div>
        <span className="label">Total model runs</span>
        <span className="value">{summary.total_model_runs}</span>
      </div>
      <div>
        <span className="label">Total estimated cost</span>
        <span className="value">${summary.total_estimated_cost.toFixed(4)}</span>
      </div>
      <div>
        <span className="label">Average latency</span>
        <span className="value">{summary.average_latency_ms.toFixed(0)} ms</span>
      </div>
      <div>
        <span className="label">Average tokens</span>
        <span className="value">{summary.average_total_tokens.toFixed(0)}</span>
      </div>
      <div>
        <span className="label">Good / Bad</span>
        <span className="value">
          {summary.good_percentage.toFixed(0)}% / {summary.bad_percentage.toFixed(0)}%
        </span>
      </div>
    </div>
  );
}
