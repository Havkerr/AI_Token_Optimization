import type { HistoryEntry } from "../types";

interface Props {
  entries: HistoryEntry[];
}

export function HistoryTable({ entries }: Props) {
  return (
    <table>
      <thead>
        <tr>
          <th>Prompt</th>
          <th>Date</th>
          <th>Models tested</th>
          <th>Cost</th>
          <th>Ratings</th>
        </tr>
      </thead>
      <tbody>
        {entries.map((entry) => {
          const totalCost = entry.runs.reduce((sum, r) => sum + r.estimated_cost, 0);
          return (
            <tr key={entry.prompt_id}>
              <td>{entry.prompt_text}</td>
              <td>{new Date(entry.created_at).toLocaleString()}</td>
              <td>{entry.runs.map((r) => r.model_name).join(", ")}</td>
              <td>${totalCost.toFixed(4)}</td>
              <td>
                {entry.runs
                  .map((r) => `${r.model_name}: ${r.rating ?? "unrated"}`)
                  .join(", ")}
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
