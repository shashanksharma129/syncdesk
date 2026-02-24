// ABOUTME: Ticket detail for parent: thread, no internal notes.
"use client";

import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import Link from "next/link";
import { CATEGORY_LABELS } from "@/lib/mock-data";
import { fetchTicket } from "@/services/tickets";
import { fetchStudents } from "@/services/students";
import type { Ticket } from "@/lib/types";
import type { Student } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import styles from "@/styles/TicketDetail.module.css";

function formatDateTime(iso: string) {
  return new Date(iso).toLocaleString();
}

export default function TicketDetailPage() {
  const params = useParams();
  const id = params?.id as string;
  const [ticket, setTicket] = useState<Ticket | null | undefined>(undefined);
  const [students, setStudents] = useState<Student[]>([]);

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
        <Link href="/tickets">Back to tickets</Link>
      </div>
    );
  }
  const studentNames = ticket.student_ids.map((sid) => students.find((s) => s.id === sid)?.name).filter(Boolean).join(", ");
  const publicMessages = ticket.messages.filter((m) => !m.is_internal_note);
  return (
    <div className={styles.wrapper}>
      <Link href="/tickets" className={styles.back}>Back to tickets</Link>
      <header className={styles.header}>
        <h1 className={styles.title}>{ticket.title}</h1>
        <div className={styles.badges}>
          <Badge variant="neutral">{CATEGORY_LABELS[ticket.category] ?? ticket.category}</Badge>
          <Badge variant={ticket.status === "resolved" ? "resolved" : ticket.status === "in_progress" ? "in_progress" : "pending"}>{ticket.status.replace("_", " ")}</Badge>
          {ticket.urgency === "urgent" && <Badge variant="urgent">Urgent</Badge>}
        </div>
        {ticket.assigned_role && <p className={styles.assigned}>Assigned to: {ticket.assigned_role}</p>}
        {studentNames && <p className={styles.students}>Regarding: {studentNames}</p>}
        {ticket.known_issue && (
          <p className={styles.footer} style={{ marginTop: "0.5rem", fontSize: "0.875rem", fontStyle: "italic", color: "var(--color-text-muted)" }}>
            No action required from parents.
          </p>
        )}
      </header>
      <section className={styles.thread}>
        <h2 className={styles.threadTitle}>Messages</h2>
        {publicMessages.map((m) => (
          <div key={m.id} className={m.is_staff ? styles.msgStaff : styles.msgParent}>
            <p className={styles.msgMeta}>{m.is_staff ? "Staff" : "You"} - {formatDateTime(m.created_at)}</p>
            <p className={styles.msgBody}>{m.body}</p>
          </div>
        ))}
      </section>
      {ticket.status === "resolved" && (
        <section className={styles.actions}>
          <p>Was this resolved to your satisfaction?</p>
          <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
            <Link href={`/tickets/${id}/satisfied`}><Button variant="primary">Yes, resolved</Button></Link>
            <Link href={`/tickets/${id}/reopen`}><Button variant="secondary">Request reopen</Button></Link>
          </div>
        </section>
      )}
    </div>
  );
}
