// ABOUTME: Announcement detail; auto-mark read after 3s.
"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { fetchAnnouncements, markAnnouncementRead } from "@/services/announcements";
import type { Announcement } from "@/lib/types";

function formatDateTime(iso: string) {
  return new Date(iso).toLocaleString();
}

export default function AnnouncementDetailPage() {
  const params = useParams();
  const id = params?.id as string;
  const [announcement, setAnnouncement] = useState<Announcement | null | undefined>(undefined);
  const [read, setRead] = useState(false);

  useEffect(() => {
    if (!id) return;
    fetchAnnouncements()
      .then((list) => list.find((a) => a.id === id) ?? null)
      .then(setAnnouncement)
      .catch(() => setAnnouncement(null));
  }, [id]);

  useEffect(() => {
    if (!announcement) return;
    const t = setTimeout(() => {
      markAnnouncementRead(announcement.id).catch(() => {});
      setRead(true);
    }, 3000);
    return () => clearTimeout(t);
  }, [announcement]);

  if (announcement === undefined) return <p style={{ color: "var(--color-text-muted)" }}>Loading…</p>;
  if (!announcement) {
    return (
      <div>
        <p>Announcement not found.</p>
        <Link href="/announcements">Back to announcements</Link>
      </div>
    );
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <Link href="/announcements" style={{ fontSize: "0.875rem", color: "var(--color-primary)" }}>← Back to announcements</Link>
      <h1>{announcement.title}</h1>
      <p style={{ fontSize: "0.875rem", color: "var(--color-text-muted)" }}>{formatDateTime(announcement.created_at)}</p>
      <div style={{ whiteSpace: "pre-wrap" }}>{announcement.body}</div>
      {announcement.has_attachment && <p style={{ fontSize: "0.875rem" }}>Attachment (download not implemented)</p>}
      {read && <p style={{ fontSize: "0.875rem", color: "var(--color-text-muted)" }}>Marked as read.</p>}
    </div>
  );
}
