// ABOUTME: Create ticket flow: form, confirmation, success.
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import { Select } from "@/components/ui/Select";
import { StudentSelector } from "@/components/StudentSelector";
import { Alert } from "@/components/ui/Alert";
import { GuardrailBanner } from "@/components/GuardrailBanner";
import { CATEGORY_LABELS } from "@/lib/mock-data";
import { fetchStudents } from "@/services/students";
import { createTicket } from "@/services/tickets";
import type { Student } from "@/lib/types";
import type { TicketCategory, TicketUrgency } from "@/lib/types";

function categoryToBackend(c: string): string {
  if (c === "academic") return "academic_teaching";
  return c;
}

const CATEGORY_OPTIONS: { value: TicketCategory; label: string }[] = [
  { value: "academic", label: "Academic" },
  { value: "transport", label: "Transport" },
  { value: "health_safety", label: "Health & Safety" },
  { value: "other", label: "Other" },
];
const URGENCY_OPTIONS: { value: TicketUrgency; label: string }[] = [
  { value: "normal", label: "Normal" },
  { value: "urgent", label: "Urgent" },
];

export default function NewTicketPage() {
  const router = useRouter();
  const [students, setStudents] = useState<Student[]>([]);
  const [step, setStep] = useState<"form" | "confirm" | "success">("form");
  const [category, setCategory] = useState<TicketCategory>("academic");
  const [selectedStudentIds, setSelectedStudentIds] = useState<string[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [urgency, setUrgency] = useState<TicketUrgency>("normal");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const guardrail = { blocked: false };

  useEffect(() => {
    fetchStudents().then(setStudents).catch(() => setStudents([]));
  }, []);

  const canUrgent = category === "transport" || category === "health_safety";
  const handleSubmitForm = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!title.trim()) { setError("Please enter a title."); return; }
    if (selectedStudentIds.length === 0) { setError("Please select at least one child."); return; }
    setStep("confirm");
  };
  const handleConfirm = async () => {
    setError("");
    setSubmitting(true);
    try {
      await createTicket({
        student_ids: selectedStudentIds.map(Number),
        category: categoryToBackend(category),
        title: title.trim() || null,
        description: description.trim() || null,
        urgency: urgency === "urgent",
      });
      setStep("success");
      setTimeout(() => router.push("/tickets"), 2000);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create ticket.");
    } finally {
      setSubmitting(false);
    }
  };

  if (step === "success") {
    return (
      <div>
        <Alert variant="success" title="Ticket created">Your request has been submitted. We will get back to you soon.</Alert>
        <Link href="/tickets"><Button variant="primary">View tickets</Button></Link>
      </div>
    );
  }
  if (step === "confirm") {
    const names = students.filter((s) => selectedStudentIds.includes(s.id)).map((s) => s.name).join(", ");
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <h2>Confirm</h2>
        <p>This ticket is about: <strong>{names}</strong></p>
        <p>Category: {CATEGORY_LABELS[category] ?? category}. Title: {title}</p>
        <p>{description || "(No description)"}</p>
        {error && <Alert variant="error">{error}</Alert>}
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <Button variant="secondary" onClick={() => setStep("form")} disabled={submitting}>Back</Button>
          <Button variant="primary" onClick={handleConfirm} disabled={submitting}>{submitting ? "Submitting…" : "Submit"}</Button>
        </div>
      </div>
    );
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <h1>Create ticket</h1>
      <Alert variant="info">Outside office hours. We will respond when we can.</Alert>
      {guardrail.blocked && <GuardrailBanner state={guardrail} />}
      {error && <Alert variant="error">{error}</Alert>}
      <form onSubmit={handleSubmitForm} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <Select id="category" label="Category" options={CATEGORY_OPTIONS} value={category} onChange={(e) => setCategory(e.target.value as TicketCategory)} />
        {category === "academic" && <Alert variant="info">Policy or promotion concerns go to school administration.</Alert>}
        <StudentSelector students={students} selectedIds={selectedStudentIds} onChange={setSelectedStudentIds} label="Which child(ren) is this about?" />
        <Input id="title" label="Title" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Short summary" required />
        <Textarea id="desc" label="Description" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Details..." rows={4} />
        {canUrgent && <Select id="urgency" label="Urgency" options={URGENCY_OPTIONS} value={urgency} onChange={(e) => setUrgency(e.target.value as TicketUrgency)} />}
        <p style={{ fontSize: "0.875rem", color: "var(--color-text-muted)" }}>Attachment upload (coming soon)</p>
        <Button type="submit" variant="primary" disabled={guardrail.blocked}>Continue</Button>
      </form>
    </div>
  );
}
