// ABOUTME: Accessible text input with label and error.
import styles from "@/styles/ui/Input.module.css";

export function Input(props: React.InputHTMLAttributes<HTMLInputElement> & { id: string; label: string; error?: string; }) {
  const { id, label, error, type = "text", className = "", ...rest } = props;
  return (
    <div className={styles.wrapper}>
      <label htmlFor={id} className={styles.label}>{label}</label>
      <input id={id} type={type}
        className={[styles.input, error && styles.inputError, className].filter(Boolean).join(" ")}
        aria-invalid={!!error} aria-describedby={error ? id + "-error" : undefined} {...rest} />
      {error && <p id={id + "-error"} className={styles.error} role="alert">{error}</p>}
    </div>
  );
}
