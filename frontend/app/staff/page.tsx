// ABOUTME: Staff dashboard: ticket inbox.
"use client";

import { TicketCard } from "@/components/TicketCard";
import { Select } from "@/components/ui/Select";
import { fetchTickets } from "@/services/tickets";
import { useState, useMemo, useEffect } from "react";

const STATUS_OPTIONS = [
  { value: "", label: "All" },
  { value: "pending", label: "Pending" },
  { value: "in_progress", label: "In progress" },
  { value: "resolved", label: "Resolved" },
];

export default function StaffDashboardPage() {
  const [tickets, setTickets] = useState<Awaited<ReturnType<typeof fetchTickets>>>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState("");
  const filtered = useMemo(() => {
    if (!statusFilter) return tickets;
    return tickets.filter((t) => t.status === statusFilter);
  }, [tickets, statusFilter]);

  useEffect(() => {
    fetchTickets()
      .then(setTickets)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p style={{ color: "var(--color-text-muted)" }}>Loading…</p>;
  if (error) return <p style={{ color: "var(--color-error)" }}>{error}</p>;
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <h1>Staff – Ticket inbox</h1>
      <Select id="staff-status" label="Status" options={STATUS_OPTIONS} value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} />
      {filtered.length === 0 ? (
        <p style={{ color: "var(--color-text-muted)" }}>No tickets.</p>
      ) : (
        filtered.map((t) => (
          <TicketCard key={t.id} ticket={t} basePath="/staff/tickets" />
        ))
      )}
    </div>
  );
}
