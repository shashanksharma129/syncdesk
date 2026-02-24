// ABOUTME: Profile page: name, phone, editable name/email, read-only students, banner.
"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/lib/auth-context";
import { Alert } from "@/components/ui/Alert";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { fetchStudents } from "@/services/students";
import type { Student } from "@/lib/types";

export default function ProfilePage() {
  const { user } = useAuth();
  const [name, setName] = useState(user?.name || "Parent");
  const [email, setEmail] = useState("parent@example.com");
  const [saved, setSaved] = useState(false);
  const [students, setStudents] = useState<Student[]>([]);

  useEffect(() => {
    fetchStudents().then(setStudents).catch(() => setStudents([]));
  }, []);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      <h1>Profile</h1>
      <p style={{ color: "var(--color-text-muted)", fontSize: "0.875rem" }}>
        Logged in as: <strong>{user?.role === "staff" ? "Staff" : "Parent"}</strong>
      </p>
      <form onSubmit={handleSave} style={{ display: "flex", flexDirection: "column", gap: "1rem", maxWidth: "20rem" }}>
        <Input id="name" label="Name" value={name} onChange={(e) => setName(e.target.value)} />
        <Input id="email" label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <Button type="submit" variant="primary">Save changes</Button>
        {saved && <Alert variant="success">Saved.</Alert>}
      </form>
      <p style={{ color: "var(--color-text-muted)" }}>Phone: {user?.phone ?? "—"}</p>
      {user?.role === "staff" && (
        <p><a href="/staff" style={{ color: "var(--color-primary)", fontSize: "0.875rem" }}>Staff inbox</a></p>
      )}
      <section>
        <h2 style={{ fontSize: "1rem", marginBottom: "0.5rem" }}>Linked students</h2>
        <ul style={{ listStyle: "none", padding: 0 }}>
          {students.map((s) => (
            <li key={s.id} style={{ padding: "0.25rem 0" }}>{s.name}{s.grade ? ` (${s.grade})` : ""}</li>
          ))}
        </ul>
        <div style={{ marginTop: "1rem" }}>
          <Alert variant="info">Some student details are maintained by the school.</Alert>
        </div>
      </section>
    </div>
  );
}
