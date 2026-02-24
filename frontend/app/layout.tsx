// ABOUTME: Root layout for School Communication & Helpdesk OS.
// ABOUTME: Applies global styles and wraps app in shell.

import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/lib/auth-context";
import { AuthGuard } from "@/components/AuthGuard";

export const metadata: Metadata = {
  title: "School Communication & Helpdesk OS",
  description: "School communication and helpdesk for parents and staff",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="manifest" href="/manifest.json" />
      </head>
      <body>
        <AuthProvider>
          <AuthGuard>{children}</AuthGuard>
        </AuthProvider>
      </body>
    </html>
  );
}
