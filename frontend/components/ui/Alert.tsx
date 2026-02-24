// ABOUTME: Banner/alert for info, success, warning, error.
import styles from "@/styles/ui/Alert.module.css";

type AlertVariant = "info" | "success" | "warning" | "error";

export function Alert({
  children,
  variant = "info",
  title,
  className = "",
}: {
  children: React.ReactNode;
  variant?: AlertVariant;
  title?: string;
  className?: string;
}) {
  const role = variant === "error" ? "alert" : "status";
  return (
    <div className={[styles.alert, styles[variant], className].filter(Boolean).join(" ")} role={role}>
      {title && <p className={styles.title}>{title}</p>}
      <div className={styles.content}>{children}</div>
    </div>
  );
}
