// ABOUTME: Header with logout; client component.
"use client";

import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import styles from "@/styles/AppShell.module.css";

export function HeaderWithLogout() {
  const router = useRouter();
  const { logout } = useAuth();
  const handleLogout = () => {
    logout();
    router.push("/login");
    router.refresh();
  };
  return (
    <header className={styles.header} role="banner">
      <span className={styles.headerTitle}>School Helpdesk</span>
      <button type="button" onClick={handleLogout} className={styles.logoutBtn}>Log out</button>
    </header>
  );
}
