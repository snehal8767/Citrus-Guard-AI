// Command Console full page.
import CommandConsole from "../components/CommandConsole";
import { PageHeader } from "../components/ui";

export default function ConsolePage() {
  return (
    <div>
      <PageHeader title="Command Console" subtitle="Text commands for the orchard system. Deterministic rule-based parser — not an LLM." />
      <CommandConsole orchardId={1} />
    </div>
  );
}
