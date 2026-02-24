// ABOUTME: Announcements list with cards (title, date, attachment).
"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { fetchAnnouncements } from "@/services/announcements";
import type { Announcement } from "@/lib/types";
import styles from "@/styles/AnnouncementCard.module.css";

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString();
}

export default function AnnouncementsPage() {
  const [list, setList] = useState<Announcement[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnnouncements()
      .then(setList)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p style={{ color: "var(--color-text-muted)" }}>Loading…</p>;
  if (error) return <p style={{ color: "var(--color-error)" }}>{error}</p>;
  if (list.length === 0) {
    return (
      <div>
        <h1>Announcements</h1>
        <p style={{ color: "var(--color-text-muted)" }}>No announcements yet.</p>
      </div>
    );
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
      <h1>Announcements</h1>
      {list.map((a) => (
        <Link key={a.id} href={`/announcements/${a.id}`} className={styles.card}>
          <span className={styles.title}>{a.title}</span>
          <span className={styles.date}>{formatDate(a.created_at)}</span>
          {a.has_attachment && <span className={styles.attach} aria-hidden>📎</span>}
        </Link>
      ))}
    </div>
  );
}
