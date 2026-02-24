// ABOUTME: Displays guardrail messages (max tickets, cooldown, weekly cap); calm copy.
"use client";
import { useState, useEffect } from "react";
import { Alert } from "@/components/ui/Alert";

export type GuardrailState = {
  blocked: boolean;
  reason?: "max_open" | "cooldown" | "weekly_cap" | "other";
  blockUntil?: string; // ISO date for countdown
};

const MESSAGES: Record<string, string> = {
  max_open: "You already have 3 open tickets. Please wait until one is resolved before creating another.",
  cooldown: "Please wait 30 minutes before creating another request.",
  weekly_cap: "You have reached the limit of 5 tickets in the last 7 days. You can create more next week.",
  other: "Ticket creation is temporarily unavailable. Please try again later.",
};

export function GuardrailBanner({ state }: { state: GuardrailState }) {
  if (!state.blocked) return null;
  const msg = state.reason ? MESSAGES[state.reason] ?? MESSAGES.other : MESSAGES.other;
  return (
    <Alert variant="warning" title="Unable to create ticket">
      {msg}
      {state.blockUntil && (
        <Countdown until={state.blockUntil} />
      )}
    </Alert>
  );
}

function Countdown({ until }: { until: string }) {
  const [left, setLeft] = useState("");
  useEffect(() => {
    const update = () => {
      const end = new Date(until).getTime();
      const now = Date.now();
      if (now >= end) {
        setLeft("You can create a ticket now.");
        return;
      }
      const m = Math.floor((end - now) / 60000);
      setLeft(`You can create another ticket in about ${m} minute${m !== 1 ? "s" : ""}.`);
    };
    update();
    const t = setInterval(update, 60000);
    return () => clearInterval(t);
  }, [until]);
  return <p style={{ marginTop: "0.25rem", fontSize: "0.875rem" }}>{left}</p>;
}

