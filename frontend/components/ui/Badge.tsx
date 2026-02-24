// ABOUTME: Status or label badge.
import styles from "@/styles/ui/Badge.module.css";

type BadgeVariant = "pending" | "in_progress" | "resolved" | "urgent" | "neutral";

export function Badge(props: { children: React.ReactNode; variant?: BadgeVariant; className?: string }) {
  const { children, variant = "neutral", className = "" } = props;
  return <span className={[styles.badge, styles[variant], className].filter(Boolean).join(" ")} role="status">{children}</span>;
}
