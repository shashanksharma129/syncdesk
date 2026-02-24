// ABOUTME: Login form (phone) with validation and mock submit.
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { requestOtp } from "@/services/auth";

export function LoginForm() {
  const router = useRouter();
  const [phone, setPhone] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    const digits = phone.replace(/\D/g, "");
    if (digits.length < 10) {
      setError("Please enter a valid phone number.");
      return;
    }
    setLoading(true);
    try {
      await requestOtp(phone);
      router.push("/login/otp?phone=" + encodeURIComponent(phone));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not send code. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem", maxWidth: "20rem" }}>
      <h1 style={{ fontSize: "1.5rem", fontWeight: 600 }}>Sign in</h1>
      <p style={{ color: "var(--color-text-muted)" }}>Enter your phone number to receive a code.</p>
      <Input id="phone" label="Phone number" type="tel" placeholder="+1 555 000 0000" value={phone} onChange={(e) => setPhone(e.target.value)} error={error} disabled={loading} autoComplete="tel" />
      <Button type="submit" variant="primary" disabled={loading}>{loading ? "Sending…" : "Continue"}</Button>
    </form>
  );
}
