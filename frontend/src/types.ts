export type Rating = "good" | "bad";

export interface ModelRunResult {
  model_run_id: number;
  model_name: string;
  response_text: string | null;
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
  latency_ms: number;
  estimated_cost: number;
  status: "success" | "error";
  error_message: string | null;
}

export interface ComparisonResponse {
  prompt_id: number;
  prompt_text: string;
  runs: ModelRunResult[];
}

export interface DashboardSummary {
  total_prompts: number;
  total_model_runs: number;
  total_estimated_cost: number;
  average_latency_ms: number;
  average_total_tokens: number;
  good_percentage: number;
  bad_percentage: number;
}

export interface HistoryRunSummary {
  model_name: string;
  estimated_cost: number;
  status: string;
  rating: Rating | null;
}

export interface HistoryEntry {
  prompt_id: number;
  prompt_text: string;
  created_at: string;
  runs: HistoryRunSummary[];
}
