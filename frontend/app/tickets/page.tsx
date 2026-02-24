// ABOUTME: Parent ticket list with filters and create CTA.
"use client";

import { useState, useMemo, useEffect } from "react";
import Link from "next/link";
import { TicketCard } from "@/components/TicketCard";
import { GuardrailBanner } from "@/components/GuardrailBanner";
import { Button } from "@/components/ui/Button";
import { Select } from "@/components/ui/Select";
import { fetchTickets } from "@/services/tickets";
import { fetchStudents } from "@/services/students";
import type { Ticket } from "@/lib/types";
import type { Student } from "@/lib/types";

const STATUS_OPTIONS: { value: string; label: string }[] = [
  { value: "", label: "All statuses" },
  { value: "pending", label: "Pending" },
  { value: "in_progress", label: "In progress" },
  { value: "resolved", label: "Resolved" },
];

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState("");
  const [childFilter, setChildFilter] = useState("");
  const guardrail = { blocked: false } as { blocked: boolean; reason?: "max_open" | "cooldown" | "weekly_cap"; blockUntil?: string };

  useEffect(() => {
    Promise.all([fetchTickets(), fetchStudents()])
      .then(([tList, sList]) => {
        setTickets(tList);
        setStudents(sList);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    let list = [...tickets];
    if (statusFilter) list = list.filter((t) => t.status === statusFilter);
    if (childFilter) list = list.filter((t) => t.student_ids.includes(childFilter));
    return list;
  }, [tickets, statusFilter, childFilter]);

  const childOptions = [
    { value: "", label: "All children" },
    ...students.map((s) => ({ value: s.id, label: s.name })),
  ];

  if (loading) return <p style={{ color: "var(--color-text-muted)" }}>Loading…</p>;
  if (error) return <p style={{ color: "var(--color-error)" }}>{error}</p>;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "0.5rem" }}>
        <h1>Tickets</h1>
        <Link href={guardrail.blocked ? "#" : "/tickets/new"}><Button variant="primary" disabled={guardrail.blocked}>Create ticket</Button></Link>
      </div>
      {guardrail.blocked && <GuardrailBanner state={guardrail} />}
      <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem", maxWidth: "18rem" }}>
        <Select id="status" label="Status" options={STATUS_OPTIONS} value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} />
        <Select id="child" label="Child" options={childOptions} value={childFilter} onChange={(e) => setChildFilter(e.target.value)} />
      </div>
      {filtered.length === 0 ? (
        <p style={{ color: "var(--color-text-muted)" }}>
          {!statusFilter && !childFilter
            ? "No tickets yet. Create one above when you need help."
            : "No tickets match your filters. You can create a new ticket above."}
        </p>
      ) : (
        <div>
          {filtered.map((t) => (
            <TicketCard key={t.id} ticket={t} />
          ))}
        </div>
      )}
    </div>
  );
}
