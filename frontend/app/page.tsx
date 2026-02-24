// ABOUTME: Home page for School Communication & Helpdesk OS.
// ABOUTME: Staff get CTA to Staff inbox; parents get generic copy.

"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import styles from "./page.module.css";

export default function Home() {
  const { user } = useAuth();
  const isStaff = user?.role === "staff";

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Welcome</h1>
      <p className={styles.lead}>
        Use the menu below to open tickets, read announcements, or manage your
        profile.
      </p>
      {isStaff && (
        <p className={styles.lead}>
          <Link href="/staff" style={{ color: "var(--color-primary)", fontWeight: 600 }}>Go to Staff inbox</Link> to handle tickets.
        </p>
      )}
    </div>
  );
}
