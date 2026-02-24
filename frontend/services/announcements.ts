// ABOUTME: Announcements API: list and mark read.
import { fetchApi } from "./api";
import type { Announcement } from "@/lib/types";

export interface AnnouncementApi {
  id: number;
  title: string;
  content: string;
  target_audience: string;
  created_at: string;
  read: boolean;
}

function toAnnouncement(a: AnnouncementApi): Announcement {
  return {
    id: String(a.id),
    title: a.title,
    body: a.content,
    created_at: a.created_at,
    audience: a.target_audience as Announcement["audience"],
    has_attachment: false,
    read_at: a.read ? a.created_at : null,
  };
}

export async function fetchAnnouncements(): Promise<Announcement[]> {
  const list = (await fetchApi<AnnouncementApi[]>("/announcements")) ?? [];
  return list.map(toAnnouncement);
}

export async function markAnnouncementRead(id: string): Promise<void> {
  await fetchApi<{ message: string }>(`/announcements/${id}/read`, { method: "POST" });
}
