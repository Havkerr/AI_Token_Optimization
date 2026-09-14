import { useState } from "react";

const AVAILABLE_MODELS = [
  "claude-haiku-4-5-20251001",
  "claude-sonnet-5",
  "claude-opus-5",
];

interface Props {
  onRun: (prompt: string, models: string[]) => void;
  isRunning: boolean;
}

export function PromptForm({ onRun, isRunning }: Props) {
  const [prompt, setPrompt] = useState("");
  const [selectedModels, setSelectedModels] = useState<string[]>(AVAILABLE_MODELS);

  function toggleModel(model: string) {
    setSelectedModels((prev) =>
      prev.includes(model) ? prev.filter((m) => m !== model) : [...prev, model],
    );
  }

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!prompt.trim() || selectedModels.length === 0) return;
    onRun(prompt, selectedModels);
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="prompt">Prompt</label>
      <textarea
        id="prompt"
        rows={4}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Explain recursion to a beginner with an example."
      />

      <fieldset>
        <legend>Models</legend>
        {AVAILABLE_MODELS.map((model) => (
          <label key={model}>
            <input
              type="checkbox"
              checked={selectedModels.includes(model)}
              onChange={() => toggleModel(model)}
            />
            {model}
          </label>
        ))}
      </fieldset>

      <button type="submit" disabled={isRunning}>
        {isRunning ? "Running..." : "Run Comparison"}
      </button>
    </form>
  );
}
