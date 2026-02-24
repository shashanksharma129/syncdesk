// ABOUTME: Redirects to login when unauthenticated; hides shell on auth pages.
"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";
import { useAuth } from "@/lib/auth-context";
import { AppShell } from "@/components/AppShell";

const PUBLIC_PATHS = ["/login", "/login/otp", "/ui-preview"];

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, loading } = useAuth();
  const isPublic = PUBLIC_PATHS.some((p) => pathname?.startsWith(p));

  useEffect(() => {
    if (loading) return;
    if (!user && !isPublic) {
      router.replace("/login");
      return;
    }
  }, [user, loading, isPublic, router]);

  if (loading) {
    return (
      <div style={{ padding: "2rem", textAlign: "center" }}>Loading…</div>
    );
  }
  if (!user && !isPublic) {
    return null;
  }
  if (isPublic) {
    return <>{children}</>;
  }
  return <AppShell>{children}</AppShell>;
}
