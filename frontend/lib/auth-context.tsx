// ABOUTME: Auth state and provider; mock-friendly, replaceable with real API.
"use client";

import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { getStoredToken, setStoredToken, clearStoredToken, fetchMe } from "@/services/auth";

export type User = { id: string; phone: string; role: "parent" | "staff"; name?: string };

type AuthContextValue = {
  user: User | null;
  loading: boolean;
  login: (u: User, token: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

function roleToFrontend(role: string): "parent" | "staff" {
  return role === "parent" ? "parent" : "staff";
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getStoredToken();
    if (!token) {
      setLoading(false);
      return;
    }
    fetchMe(token)
      .then((me) => {
        setUser({
          id: String(me.id),
          phone: me.phone,
          role: roleToFrontend(me.role),
        });
      })
      .catch(() => clearStoredToken())
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback((u: User, token: string) => {
    setUser(u);
    setStoredToken(token);
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    clearStoredToken();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
