// ABOUTME: Mobile-first app shell with top header and bottom navigation.
// ABOUTME: Wraps all pages; no backend calls.

import Link from "next/link";
import { HeaderWithLogout } from "@/components/HeaderWithLogout";
import styles from "@/styles/AppShell.module.css";

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className={styles.shell}>
      <HeaderWithLogout />
      <main className={styles.main} id="main-content">
        {children}
      </main>
      <nav className={styles.bottomNav} aria-label="Main navigation">
        <Link href="/" className={styles.navItem} aria-current="page">
          Home
        </Link>
        <Link href="/tickets" className={styles.navItem}>
          Tickets
        </Link>
        <Link href="/announcements" className={styles.navItem}>
          Announcements
        </Link>
        <Link href="/profile" className={styles.navItem}>
          Profile
        </Link>
      </nav>
    </div>
  );
}
