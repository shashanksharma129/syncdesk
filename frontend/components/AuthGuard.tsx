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

  const isStaffPath = pathname?.startsWith("/staff") ?? false;

  useEffect(() => {
    if (loading) return;
    if (!user && !isPublic) {
      router.replace("/login");
      return;
    }
    if (user && isStaffPath && user.role !== "staff") {
      router.replace("/");
      return;
    }
  }, [user, loading, isPublic, isStaffPath, router]);

  if (loading) {
    return (
      <div style={{ padding: "2rem", textAlign: "center" }}>Loading…</div>
    );
  }
  if (!user && !isPublic) {
    return null;
  }
  if (user && isStaffPath && user.role !== "staff") {
    return null;
  }
  if (isPublic) {
    return <>{children}</>;
  }
  return <AppShell>{children}</AppShell>;
}
