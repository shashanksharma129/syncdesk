// ABOUTME: Auth API: request OTP, verify OTP, get current user.
import { apiUrl } from "./api";

const TOKEN_KEY = "syncdesk_access_token";

export function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearStoredToken(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_KEY);
}

export async function requestOtp(phone: string): Promise<{ message: string }> {
  const res = await fetch(apiUrl("/auth/request-otp"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((data as { detail?: string }).detail || "Could not send code.");
  return data as { message: string };
}

export async function verifyOtp(phone: string, code: string): Promise<{ access_token: string }> {
  const res = await fetch(apiUrl("/auth/verify-otp"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone, code }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((data as { detail?: string }).detail || "Invalid or expired code.");
  const out = data as { access_token?: string };
  if (!out.access_token) throw new Error("Invalid response.");
  return { access_token: out.access_token };
}

export async function fetchMe(token: string): Promise<{ id: number; phone: string; role: string; school_id: number }> {
  const res = await fetch(apiUrl("/me"), {
    headers: { Authorization: `Bearer ${token}` },
    credentials: "include",
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((data as { detail?: string }).detail || "Session expired.");
  return data as { id: number; phone: string; role: string; school_id: number };
}
