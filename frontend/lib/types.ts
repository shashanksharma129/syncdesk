// ABOUTME: Shared types for tickets, students, announcements (align with backend).

export type TicketStatus = "pending" | "in_progress" | "resolved";
export type TicketCategory = "academic" | "transport" | "health_safety" | "other" | string;
export type TicketUrgency = "normal" | "urgent";

export interface Student {
  id: string;
  name: string;
  grade?: string;
  school_id: string;
}

export interface Ticket {
  id: string;
  category: TicketCategory;
  status: TicketStatus;
  urgency: TicketUrgency;
  title: string;
  created_at: string;
  updated_at: string;
  assigned_role?: string;
  student_ids: string[];
  messages: TicketMessage[];
  known_issue?: boolean;
}

export interface TicketMessage {
  id: string;
  body: string;
  created_at: string;
  is_staff: boolean;
  is_internal_note?: boolean;
}

export interface Announcement {
  id: string;
  title: string;
  body: string;
  created_at: string;
  audience: "parents" | "staff" | "both";
  has_attachment?: boolean;
  read_at?: string | null;
}
