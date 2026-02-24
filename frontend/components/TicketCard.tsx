// ABOUTME: Ticket list card: category, status, last updated, urgent indicator.
import Link from "next/link";
import type { Ticket } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";
import { CATEGORY_LABELS } from "@/lib/mock-data";
import styles from "@/styles/TicketCard.module.css";

function formatDate(iso: string) {
  const d = new Date(iso);
  const now = new Date();
  const sameDay = d.toDateString() === now.toDateString();
  return sameDay ? d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : d.toLocaleDateString();
}

export function TicketCard({ ticket, basePath = "/tickets" }: { ticket: Ticket; basePath?: string }) {
  const statusVariant = ticket.status === "resolved" ? "resolved" : ticket.status === "in_progress" ? "in_progress" : "pending";
  return (
    <Link href={`${basePath}/${ticket.id}`} className={styles.card}>
      <div className={styles.row}>
        <span className={styles.title}>{ticket.title}</span>
        {ticket.urgency === "urgent" && <Badge variant="urgent">Urgent</Badge>}
      </div>
      <div className={styles.meta}>
        <Badge variant="neutral">{CATEGORY_LABELS[ticket.category] ?? ticket.category}</Badge>
        <Badge variant={statusVariant}>{ticket.status.replace("_", " ")}</Badge>
        <span className={styles.updated}>Updated {formatDate(ticket.updated_at)}</span>
      </div>
    </Link>
  );
}
