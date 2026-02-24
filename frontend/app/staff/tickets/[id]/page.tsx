// ABOUTME: Staff ticket detail: reply, status, internal notes, warning.
"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { CATEGORY_LABELS } from "@/lib/mock-data";
import { fetchTicket, replyToTicket, updateTicketStatus, addInternalNote } from "@/services/tickets";
import { fetchStudents } from "@/services/students";
import type { Ticket } from "@/lib/types";
import type { Student } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Textarea } from "@/components/ui/Textarea";
import { Select } from "@/components/ui/Select";
import { Alert } from "@/components/ui/Alert";
import styles from "@/styles/TicketDetail.module.css";

function formatDateTime(iso: string) {
  return new Date(iso).toLocaleString();
}

const STATUS_OPTIONS = [
  { value: "pending", label: "Pending" },
  { value: "in_progress", label: "In progress" },
  { value: "resolved", label: "Resolved" },
];

export default function StaffTicketDetailPage() {
  const params = useParams();
  const id = params?.id as string;
  const [ticket, setTicket] = useState<Ticket | null | undefined>(undefined);
  const [students, setStudents] = useState<Student[]>([]);
  const [reply, setReply] = useState("");
  const [internalNote, setInternalNote] = useState("");
  const [sent, setSent] = useState(false);
  const [noteSent, setNoteSent] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!id) return;
    Promise.all([fetchTicket(id), fetchStudents()])
      .then(([t, sList]) => {
        setTicket(t ?? null);
        setStudents(sList);
      })
      .catch(() => setTicket(null));
  }, [id]);

  if (ticket === undefined) return <p style={{ color: "var(--color-text-muted)" }}>Loading…</p>;
  if (!ticket) {
    return (
      <div>
        <p>Ticket not found.</p>
        <Link href="/staff">Back to inbox</Link>
      </div>
    );
  }

  const studentNames = ticket.student_ids.map((sid) => students.find((s) => s.id === sid)?.name).filter(Boolean).join(", ");
  const allMessages = ticket.messages.filter((m) => !m.is_internal_note);

  const handleSendReply = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reply.trim()) return;
    setError("");
    try {
      const updated = await replyToTicket(id, reply.trim());
      setTicket(updated);
      setReply("");
      setSent(true);
      setTimeout(() => setSent(false), 3000);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to send reply.");
    }
  };
  const handleStatusChange = async (newStatus: "pending" | "in_progress" | "resolved") => {
    if (newStatus === "pending") return;
    setError("");
    try {
      const updated = await updateTicketStatus(id, newStatus);
      setTicket(updated);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to update status.");
    }
  };
  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!internalNote.trim()) return;
    setError("");
    try {
      await addInternalNote(id, internalNote.trim());
      setInternalNote("");
      setNoteSent(true);
      setTimeout(() => setNoteSent(false), 3000);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to add note.");
    }
  };
  return (
    <div className={styles.wrapper}>
      <Link href="/staff" className={styles.back}>← Back to inbox</Link>
      <header className={styles.header}>
        <h1 className={styles.title}>{ticket.title}</h1>
        <div className={styles.badges}>
          <Badge variant="neutral">{CATEGORY_LABELS[ticket.category] ?? ticket.category}</Badge>
          <Badge variant={ticket.status === "resolved" ? "resolved" : ticket.status === "in_progress" ? "in_progress" : "pending"}>{ticket.status.replace("_", " ")}</Badge>
          {ticket.urgency === "urgent" && <Badge variant="urgent">Urgent</Badge>}
        </div>
        {studentNames && <p className={styles.students}>Regarding: {studentNames}</p>}
      </header>
      <section className={styles.thread}>
        <h2 className={styles.threadTitle}>Messages</h2>
        {allMessages.map((m) => (
          <div key={m.id} className={m.is_staff ? styles.msgStaff : styles.msgParent}>
            <p className={styles.msgMeta}>{m.is_staff ? "Staff" : "Parent"} · {formatDateTime(m.created_at)}</p>
            <p className={styles.msgBody}>{m.body}</p>
          </div>
        ))}
      </section>
      <section style={{ marginTop: "1rem" }}>
        <h3 style={{ fontSize: "1rem", marginBottom: "0.5rem" }}>Reply to parent</h3>
        {error && <Alert variant="error">{error}</Alert>}
        <form onSubmit={handleSendReply} style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          <Textarea id="reply" label="Your reply" value={reply} onChange={(e) => setReply(e.target.value)} rows={3} />
          <p style={{ fontSize: "0.875rem", color: "var(--color-text-muted)" }}>Do you want to update the parent?</p>
          <Button type="submit" variant="primary" disabled={!reply.trim()}>Send reply</Button>
          {sent && <Alert variant="success">Reply sent.</Alert>}
        </form>
      </section>
      <section style={{ marginTop: "1rem" }}>
        <label htmlFor="status-select" style={{ fontSize: "0.875rem", fontWeight: 500 }}>Status</label>
        <Select id="status-select" label="Status" options={STATUS_OPTIONS} value={ticket.status} onChange={(e) => handleStatusChange(e.target.value as "pending" | "in_progress" | "resolved")} />
      </section>
      <section style={{ marginTop: "1rem", padding: "1rem", background: "var(--color-surface)", borderRadius: "var(--radius-md)" }}>
        <Alert variant="warning">Internal notes are part of permanent records.</Alert>
        <form onSubmit={handleAddNote} style={{ display: "flex", flexDirection: "column", gap: "0.5rem", marginTop: "0.5rem" }}>
          <Textarea id="note" label="Internal note" value={internalNote} onChange={(e) => setInternalNote(e.target.value)} rows={2} />
          <Button type="submit" variant="secondary" disabled={!internalNote.trim()}>Add note</Button>
          {noteSent && <Alert variant="success">Note added.</Alert>}
        </form>
      </section>
    </div>
  );
}
