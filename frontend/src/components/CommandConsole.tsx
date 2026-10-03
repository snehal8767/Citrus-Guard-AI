// Command Console panel: sends text commands to POST /commands.
import { useState } from "react";
import { api } from "../api/client";
import type { CommandResponse } from "../types";

const EXAMPLES = ["run scan", "show zone B risk", "list alerts", "show sensors for zone B", "help"];

export default function CommandConsole({ orchardId = 1 }: { orchardId?: number }) {
  const [input, setInput] = useState("");
  const [responses, setResponses] = useState<CommandResponse[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const send = async (cmd: string) => {
    const command = cmd.trim();
    if (!command || busy) return;
    setBusy(true);
    setError(null);
    try {
      const res = await api.runCommand(command, orchardId);
      setResponses((r) => [{ ...res, message: `> ${command}\n${res.message}` }, ...r].slice(0, 20));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Command failed");
    } finally {
      setBusy(false);
      setInput("");
    }
  };

  return (
    <div className="card" data-testid="command-console">
      <div className="section-title">Command Console</div>
      <p className="mt-1 text-xs text-gray-500">
        Rule-based commands mapped to real backend services (not an LLM).
      </p>
      <div className="mt-3 flex gap-2">
        <input
          className="input"
          placeholder='Type a command, e.g. "run scan"'
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send(input)}
          disabled={busy}
        />
        <button className="btn-primary" onClick={() => send(input)} disabled={busy || !input.trim()}>
          {busy ? "…" : "Send"}
        </button>
      </div>
      <div className="mt-2 flex flex-wrap gap-1.5">
        {EXAMPLES.map((ex) => (
          <button key={ex} className="rounded-full bg-leaf-100 px-2.5 py-1 text-xs font-medium text-leaf-800 hover:bg-leaf-200" onClick={() => send(ex)}>
            {ex}
          </button>
        ))}
      </div>
      {error && <div className="mt-3 text-sm text-red-700">{error}</div>}
      <div className="mt-3 max-h-72 space-y-2 overflow-y-auto">
        {responses.map((r, i) => (
          <div key={i} className="rounded-lg bg-leaf-950 p-3 font-mono text-xs text-green-200">
            <div className="whitespace-pre-wrap">{r.message}</div>
            <div className="mt-1 text-[10px] uppercase tracking-wide text-green-400">intent: {r.intent}</div>
          </div>
        ))}
        {responses.length === 0 && <div className="text-xs text-gray-400">No commands run yet.</div>}
      </div>
    </div>
  );
}
