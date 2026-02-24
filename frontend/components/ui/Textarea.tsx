// ABOUTME: Accessible textarea with label and error.
import styles from "@/styles/ui/Textarea.module.css";

export function Textarea(props: React.TextareaHTMLAttributes<HTMLTextAreaElement> & { id: string; label: string; error?: string; }) {
  const { id, label, error, className = "", ...rest } = props;
  return (
    <div className={styles.wrapper}>
      <label htmlFor={id} className={styles.label}>{label}</label>
      <textarea id={id} className={[styles.textarea, error && styles.textareaError, className].filter(Boolean).join(" ")} aria-invalid={!!error} {...rest} />
      {error && <p id={id + "-error"} className={styles.error} role="alert">{error}</p>}
    </div>
  );
}
