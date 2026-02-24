// ABOUTME: API client for backend; base URL from env or localhost.
const getBaseUrl = () =>
  (typeof window !== "undefined" && (process.env.NEXT_PUBLIC_API_URL || "")) || "http://localhost:8000";

export function apiUrl(path: string) {
  const base = getBaseUrl().replace(/\/$/, "");
  return `${base}${path.startsWith("/") ? path : "/" + path}`;
}

function getAuthHeader(): Record<string, string> {
  if (typeof window === "undefined") return {};
  const token = localStorage.getItem("syncdesk_access_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function fetchApi<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const url = apiUrl(path);
  const res = await fetch(url, {
    ...options,
    headers: { "Content-Type": "application/json", ...getAuthHeader(), ...options.headers },
    credentials: "include",
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error((err as { detail?: string }).detail || "Request failed");
  }
  return res.json() as Promise<T>;
}
