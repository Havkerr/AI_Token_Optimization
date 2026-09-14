import { useState } from "react";
import { ComparePage } from "./pages/ComparePage";
import { DashboardPage } from "./pages/DashboardPage";

type Tab = "compare" | "dashboard";

export function App() {
  const [tab, setTab] = useState<Tab>("compare");

  return (
    <div className="app">
      <nav>
        <button className={tab === "compare" ? "active" : ""} onClick={() => setTab("compare")}>
          Compare
        </button>
        <button className={tab === "dashboard" ? "active" : ""} onClick={() => setTab("dashboard")}>
          Dashboard
        </button>
      </nav>
      {tab === "compare" ? <ComparePage /> : <DashboardPage />}
    </div>
  );
}
