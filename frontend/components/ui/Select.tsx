// ABOUTME: Accessible select with label and error.
import styles from "@/styles/ui/Select.module.css";

type Props = React.SelectHTMLAttributes<HTMLSelectElement> & { id: string; label: string; error?: string; options: { value: string; label: string }[]; placeholder?: string; };

export function Select(props: Props) {
  const { id, label, error, options, placeholder, className = "", ...rest } = props;
  return (
    <div className={styles.wrapper}>
      <label htmlFor={id} className={styles.label}>{label}</label>
      <select id={id} className={[styles.select, error && styles.selectError, className].filter(Boolean).join(" ")} aria-invalid={!!error} {...rest}>
        {placeholder && <option value="">{placeholder}</option>}
        {options.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
      </select>
      {error && <p id={id + "-error"} className={styles.error} role="alert">{error}</p>}
    </div>
  );
}
