// ABOUTME: Reopen request form (mock); reason input and submit.
"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Textarea } from "@/components/ui/Textarea";
import { Alert } from "@/components/ui/Alert";

export default function ReopenPage() {
  const params = useParams();
  const router = useRouter();
  const id = params?.id as string;
  const [reason, setReason] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!reason.trim()) {
      setError("Please give a brief reason for reopening.");
      return;
    }
    setSubmitted(true);
    setTimeout(() => router.push(`/tickets/${id}`), 1500);
  };

  if (submitted) {
    return (
      <div>
        <Alert variant="success">Your reopen request has been submitted. Staff will review it.</Alert>
        <Link href={`/tickets/${id}`}><Button variant="primary">Back to ticket</Button></Link>
      </div>
    );
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <h1>Request reopen</h1>
      <p style={{ color: "var(--color-text-muted)" }}>Explain why this ticket should be reopened. Staff will review your request.</p>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <Textarea id="reason" label="Reason" value={reason} onChange={(e) => setReason(e.target.value)} placeholder="e.g. The issue is still happening..." rows={4} />
        {error && <Alert variant="error">{error}</Alert>}
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <Link href={`/tickets/${id}`}><Button type="button" variant="secondary">Cancel</Button></Link>
          <Button type="submit" variant="primary">Submit request</Button>
        </div>
      </form>
    </div>
  );
}
