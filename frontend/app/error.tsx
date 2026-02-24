// ABOUTME: Global error boundary; friendly message, no raw errors.
"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { Alert } from "@/components/ui/Alert";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);
  return (
    <div style={{ padding: "1.5rem", display: "flex", flexDirection: "column", gap: "1rem" }}>
      <Alert variant="error" title="Something went wrong">
        We could not load this page. Please try again.
      </Alert>
      <Button variant="primary" onClick={reset}>Try again</Button>
    </div>
  );
}
