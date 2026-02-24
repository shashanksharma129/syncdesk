// ABOUTME: Satisfaction confirmation; calls POST /tickets/{id}/satisfied on open.
"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { markSatisfied } from "@/services/tickets";

export default function SatisfiedPage() {
  const params = useParams();
  const id = params?.id as string;
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (!id) return;
    markSatisfied(id)
      .then(() => setStatus("success"))
      .catch((err) => {
        setStatus("error");
        setErrorMessage(err instanceof Error ? err.message : "Could not mark as satisfied.");
      });
  }, [id]);

  if (status === "loading") return <p style={{ color: "var(--color-text-muted)" }}>Loading…</p>;
  if (status === "error") {
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <Alert variant="error" title="Error">{errorMessage}</Alert>
        <Link href={"/tickets/" + id}><Button variant="primary">Back to ticket</Button></Link>
      </div>
    );
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <Alert variant="success" title="Thank you">We have marked this ticket as resolved to your satisfaction.</Alert>
      <Link href={"/tickets/" + id}><Button variant="secondary">Back to ticket</Button></Link>
      <Link href="/tickets"><Button variant="primary">View all tickets</Button></Link>
    </div>
  );
}
