// ABOUTME: Home page for School Communication & Helpdesk OS.
// ABOUTME: Placeholder content; no backend calls.

import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Welcome</h1>
      <p className={styles.lead}>
        Use the menu below to open tickets, read announcements, or manage your
        profile.
      </p>
    </div>
  );
}
