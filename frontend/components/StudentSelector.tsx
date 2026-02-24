// ABOUTME: Multi-select for students; used in profile display and create ticket.
"use client";

import type { Student } from "@/lib/types";
import styles from "@/styles/StudentSelector.module.css";

export function StudentSelector({
  students,
  selectedIds,
  onChange,
  disabled,
  label = "Select students",
}: {
  students: Student[];
  selectedIds: string[];
  onChange: (ids: string[]) => void;
  disabled?: boolean;
  label?: string;
}) {
  const toggle = (id: string) => {
    if (disabled) return;
    if (selectedIds.includes(id)) {
      onChange(selectedIds.filter((s) => s !== id));
    } else {
      onChange([...selectedIds, id]);
    }
  };
  return (
    <div className={styles.wrapper}>
      <span className={styles.label}>{label}</span>
      <ul className={styles.list} role="listbox" aria-multiselectable>
        {students.map((s) => (
          <li key={s.id} className={styles.item}>
            <label className={styles.labelRow}>
              <input
                type="checkbox"
                checked={selectedIds.includes(s.id)}
                onChange={() => toggle(s.id)}
                disabled={disabled}
                aria-label={s.name}
              />
              <span>{s.name}{s.grade ? ` (${s.grade})` : ""}</span>
            </label>
          </li>
        ))}
      </ul>
      {selectedIds.length > 0 && (
        <p className={styles.confirm}>This ticket is about: {students.filter((s) => selectedIds.includes(s.id)).map((s) => s.name).join(", ")}</p>
      )}
    </div>
  );
}
