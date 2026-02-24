// ABOUTME: Satisfaction confirmation (mock).
"use client";

import { useParams } from "next/navigation";
import Link from "next/link";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";

export default function SatisfiedPage() {
  const params = useParams();
  const id = params?.id as string;
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <Alert variant="success" title="Thank you">We have marked this ticket as resolved to your satisfaction.</Alert>
      <Link href={"/tickets/" + id}><Button variant="secondary">Back to ticket</Button></Link>
      <Link href="/tickets"><Button variant="primary">View all tickets</Button></Link>
    </div>
  );
}
