// ABOUTME: Mock data for tickets, students, announcements (replaced by API in Prompt 18).
import type { Ticket, Student, Announcement } from "./types";

export const MOCK_STUDENTS: Student[] = [
  { id: "s1", name: "Child A", grade: "Grade 5", school_id: "sc1" },
  { id: "s2", name: "Child B", grade: "Grade 3", school_id: "sc1" },
];

export const MOCK_TICKETS: Ticket[] = [
  {
    id: "t1",
    category: "transport",
    status: "in_progress",
    urgency: "normal",
    title: "Bus delay on Route 12",
    created_at: "2025-02-20T10:00:00Z",
    updated_at: "2025-02-21T14:00:00Z",
    assigned_role: "Transport",
    student_ids: ["s1"],
    messages: [
      { id: "m1", body: "Bus was 20 min late this morning.", created_at: "2025-02-20T10:00:00Z", is_staff: false },
      { id: "m2", body: "We have noted this and will inform the driver.", created_at: "2025-02-21T14:00:00Z", is_staff: true },
    ],
    known_issue: true,
  },
  {
    id: "t2",
    category: "academic",
    status: "resolved",
    urgency: "normal",
    title: "Question about homework",
    created_at: "2025-02-18T09:00:00Z",
    updated_at: "2025-02-19T11:00:00Z",
    assigned_role: "Teacher",
    student_ids: ["s2"],
    messages: [
      { id: "m3", body: "Where can we find the reading list?", created_at: "2025-02-18T09:00:00Z", is_staff: false },
      { id: "m4", body: "It is on the class portal under Resources.", created_at: "2025-02-19T11:00:00Z", is_staff: true },
    ],
  },
  {
    id: "t3",
    category: "health_safety",
    status: "pending",
    urgency: "urgent",
    title: "Allergy update",
    created_at: "2025-02-22T08:00:00Z",
    updated_at: "2025-02-22T08:00:00Z",
    assigned_role: undefined,
    student_ids: ["s1", "s2"],
    messages: [
      { id: "m5", body: "Child A has a new nut allergy. Please update records.", created_at: "2025-02-22T08:00:00Z", is_staff: false },
    ],
  },
];

export const MOCK_ANNOUNCEMENTS: Announcement[] = [
  { id: "a1", title: "School closed Monday", body: "The school will be closed on Monday for a staff development day.", created_at: "2025-02-20T07:00:00Z", audience: "both", has_attachment: false },
  { id: "a2", title: "Transport update", body: "New pickup times for Route 5 from next week.", created_at: "2025-02-19T12:00:00Z", audience: "parents", has_attachment: true },
];

export const CATEGORY_LABELS: Record<string, string> = {
  academic: "Academic",
  academic_teaching: "Academic",
  academic_exam_policy: "Exam policy",
  transport: "Transport",
  health_safety: "Health & Safety",
  other: "Other",
  discipline: "Discipline",
  attendance_leave: "Attendance & leave",
  fee_accounts: "Fee & accounts",
  cleanliness_infra: "Cleanliness & infra",
  documents: "Documents",
};
