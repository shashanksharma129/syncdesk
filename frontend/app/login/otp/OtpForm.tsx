// ABOUTME: OTP verification form; mock success/failure.
"use client";

import { useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Alert } from "@/components/ui/Alert";
import { useAuth } from "@/lib/auth-context";
import { verifyOtp, fetchMe } from "@/services/auth";

function OtpFormInner() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login } = useAuth();
  const phone = searchParams.get("phone") || "";
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    const form = e.currentTarget;
    const input = form.querySelector<HTMLInputElement>('input[name="otp"], input#otp');
    const value = (input?.value ?? code).replace(/\D/g, "");
    if (value.length !== 6) {
      setError("Please enter the 6-digit code we sent you.");
      return;
    }
    setLoading(true);
    try {
      const { access_token } = await verifyOtp(phone, value);
      const me = await fetchMe(access_token);
      login(
        { id: String(me.id), phone: me.phone, role: me.role === "parent" ? "parent" : "staff" },
        access_token
      );
      router.push("/");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "That code is incorrect. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem", maxWidth: "20rem" }}>
      <h1 style={{ fontSize: "1.5rem", fontWeight: 600 }}>Check your phone</h1>
      <p style={{ color: "var(--color-text-muted)" }}>
        We sent a code to {phone || "your number"}. Enter it below.
      </p>
      <Input
        id="otp"
        label="Verification code"
        type="text"
        inputMode="numeric"
        placeholder="000000"
        value={code}
        onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
        maxLength={6}
        error={error}
        disabled={loading}
        autoComplete="one-time-code"
      />
      <Button type="submit" variant="primary" disabled={loading}>
        {loading ? "Verifying…" : "Verify"}
      </Button>
      {error && <Alert variant="error">{error}</Alert>}
    </form>
  );
}

export function OtpForm() {
  return (
    <Suspense fallback={<p>Loading…</p>}>
      <OtpFormInner />
    </Suspense>
  );
}
