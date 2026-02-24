// ABOUTME: Ticket API client: list, get, create.
import { fetchApi } from "./api";
import type { Ticket } from "@/lib/types";

export interface TicketApi {
  id: number;
  category: string;
  status: string;
  urgency: boolean;
  title: string | null;
  created_at: string;
  updated_at: string;
  assigned_to_id: number | null;
  student_ids: number[];
  messages: { id: number; body: string; created_at: string; is_staff: boolean }[];
  known_issue?: boolean;
}

function toTicket(t: TicketApi): Ticket {
  return {
    id: String(t.id),
    category: t.category,
    status: t.status as Ticket["status"],
    urgency: t.urgency ? "urgent" : "normal",
    title: t.title ?? "",
    created_at: t.created_at,
    updated_at: t.updated_at,
    assigned_role: undefined,
    student_ids: t.student_ids.map(String),
    messages: t.messages.map((m) => ({
      id: String(m.id),
      body: m.body,
      created_at: m.created_at,
      is_staff: m.is_staff,
    })),
    known_issue: t.known_issue,
  };
}

export async function fetchTickets(): Promise<Ticket[]> {
  const list = (await fetchApi<TicketApi[]>("/tickets")) ?? [];
  return list.map(toTicket);
}

export async function fetchTicket(id: string): Promise<Ticket | null> {
  try {
    const t = await fetchApi<TicketApi>(`/tickets/${id}`);
    return toTicket(t);
  } catch {
    return null;
  }
}

export interface CreateTicketBody {
  student_ids: number[];
  category: string;
  title: string | null;
  description: string | null;
  urgency: boolean;
}

export async function createTicket(body: CreateTicketBody): Promise<Ticket> {
  const t = await fetchApi<TicketApi>("/tickets", {
    method: "POST",
    body: JSON.stringify(body),
  });
  return toTicket(t);
}

export async function replyToTicket(ticketId: string, body: string): Promise<Ticket> {
  const t = await fetchApi<TicketApi>(`/tickets/${ticketId}/reply`, {
    method: "POST",
    body: JSON.stringify({ body }),
  });
  return toTicket(t);
}

export async function updateTicketStatus(ticketId: string, status: "in_progress" | "resolved"): Promise<Ticket> {
  const t = await fetchApi<TicketApi>(`/tickets/${ticketId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
  return toTicket(t);
}

export async function addInternalNote(ticketId: string, body: string): Promise<void> {
  await fetchApi<{ message?: string }>(`/tickets/${ticketId}/internal-notes`, {
    method: "POST",
    body: JSON.stringify({ body }),
  });
}
