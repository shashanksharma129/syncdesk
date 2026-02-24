// ABOUTME: Accessible modal overlay for dialogs.
"use client";

import { useEffect } from "react";
import styles from "@/styles/ui/Modal.module.css";

export function Modal({
  open,
  onClose,
  title,
  children,
}: {
  open: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}) {
  useEffect(() => {
    if (!open) return;
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", h);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", h);
      document.body.style.overflow = "";
    };
  }, [open, onClose]);

  if (!open) return null;
  return (
    <div className={styles.overlay} onClick={onClose} role="dialog" aria-modal="true" aria-labelledby={title ? "modal-title" : undefined}>
      <div className={styles.panel} onClick={(e) => e.stopPropagation()}>
        {title && <h2 id="modal-title" className={styles.title}>{title}</h2>}
        {children}
      </div>
    </div>
  );
}
