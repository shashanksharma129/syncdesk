// ABOUTME: Reusable button with variants and accessible focus.
import styles from "@/styles/ui/Button.module.css";

type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";

export function Button({
  children,
  variant = "primary",
  type = "button",
  disabled,
  className = "",
  ...rest
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
  children: React.ReactNode;
  variant?: ButtonVariant;
}) {
  return (
    <button
      type={type}
      disabled={disabled}
      className={[styles.btn, styles[variant], className].filter(Boolean).join(" ")}
      {...rest}
    >
      {children}
    </button>
  );
}
