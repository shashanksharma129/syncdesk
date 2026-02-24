// ABOUTME: Mobile-first app shell with top header and bottom navigation.
// ABOUTME: Staff get Staff nav item; current route highlights via pathname.

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { HeaderWithLogout } from "@/components/HeaderWithLogout";
import { useAuth } from "@/lib/auth-context";
import styles from "@/styles/AppShell.module.css";

function NavLink({
  href,
  label,
  isCurrent,
}: {
  href: string;
  label: string;
  isCurrent: boolean;
}) {
  return (
    <Link
      href={href}
      className={styles.navItem}
      aria-current={isCurrent ? "page" : undefined}
    >
      {label}
    </Link>
  );
}

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { user } = useAuth();
  const isStaff = user?.role === "staff";

  const navItems = [
    { href: "/", label: "Home", match: (p: string) => p === "/" },
    { href: "/tickets", label: "Tickets", match: (p: string) => p.startsWith("/tickets") },
    ...(isStaff ? [{ href: "/staff", label: "Staff", match: (p: string) => p.startsWith("/staff") }] : []),
    { href: "/announcements", label: "Announcements", match: (p: string) => p.startsWith("/announcements") },
    { href: "/profile", label: "Profile", match: (p: string) => p.startsWith("/profile") },
  ];

  return (
    <div className={styles.shell}>
      <HeaderWithLogout />
      <main className={styles.main} id="main-content">
        {children}
      </main>
      <nav className={styles.bottomNav} aria-label="Main navigation">
        {navItems.map((item) => (
          <NavLink
            key={item.href}
            href={item.href}
            label={item.label}
            isCurrent={item.match(pathname ?? "")}
          />
        ))}
      </nav>
    </div>
  );
}
