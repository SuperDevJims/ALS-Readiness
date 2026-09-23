import axios from "axios";
import { useAuthStore } from "../store/authStore";
import { CHANGE_PASSWORD_PATH, redirect } from "../navigation";
import { isMustChangePassword } from "./errors";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  // Required so the httpOnly refresh_token cookie is sent/received on every request.
  withCredentials: true,
});

// ── Request interceptor: attach the in-memory access token ──────────────────
apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ── Response interceptor ─────────────────────────────────────────────────────
// Single-flight refresh: concurrent 401s all await the same in-flight refresh
// promise instead of each calling /refresh independently. Refresh rotation
// means only the first call would succeed; a second concurrent call would fail
// and could wrongly log the user out.
let refreshPromise: Promise<string | null> | null = null;

async function refreshAccessToken(): Promise<string | null> {
  if (!refreshPromise) {
    refreshPromise = apiClient
      .post<{ access_token: string; token_type: string }>("/api/auth/refresh")
      .then((res) => {
        const token = res.data.access_token;
        useAuthStore.getState().setAccessToken(token);
        return token;
      })
      .catch(() => null)
      .finally(() => {
        refreshPromise = null;
      });
  }
  return refreshPromise;
}

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { response, config } = error;

    if (!response || !config) {
      return Promise.reject(error);
    }

    const isAuthEndpoint =
      typeof config.url === "string" &&
      (config.url.includes("/api/auth/refresh") || config.url.includes("/api/auth/login"));

    // A 401 on /api/auth/refresh itself means there's no valid session at all -
    // never recurse into another refresh attempt (infinite-loop risk), and
    // never redirect from here; bootstrap calls refresh() directly and handles
    // that failure itself.
    // A 401 on /api/auth/login means "wrong credentials" - there's no session
    // to refresh, and no redirect belongs here either; the login form shows
    // the real error itself (Task 1/2).
    if (response.status === 401 && isAuthEndpoint) {
      return Promise.reject(error);
    }

    if (response.status === 401 && !config._retriedAfterRefresh) {
      const newToken = await refreshAccessToken();

      if (newToken) {
        // The request interceptor re-reads the store fresh on this retry, so
        // it attaches the new token itself - no need to touch headers here.
        config._retriedAfterRefresh = true;
        return apiClient(config);
      }

      useAuthStore.getState().clearSession();
      redirect("/session-expired");
      return Promise.reject(error);
    }

    // The one 403 that's a routing concern rather than a request failure: the
    // account must change its password before the backend will serve anything
    // else. Flag the store first so the router's gate lets the change-password
    // page render (a user reset mid-session has a stale flag until now), then
    // send them there. The caller's own catch still runs, but the page is
    // already being replaced.
    if (response.status === 403 && isMustChangePassword(error)) {
      useAuthStore.getState().setMustChangePassword(true);
      redirect(CHANGE_PASSWORD_PATH);
      return Promise.reject(error);
    }

    // Every other 403 (self-reset, admin-on-admin without super admin, approve
    // by a non-super admin, ...) is surfaced to the caller as-is, like 409 and
    // 400/422 - handling (toast vs. inline banner) depends on context, not this
    // layer. There is deliberately no blanket 403 redirect: page-level role
    // denial is done by RequireRole (routes/guards.tsx), in place.
    return Promise.reject(error);
  }
);

// Dev-only console access for manual verification (e.g. single-flight refresh) -
// no page makes real API calls yet this phase, so there's no UI trigger for it.
if (import.meta.env.DEV) {
  (window as unknown as { __apiClient: typeof apiClient }).__apiClient = apiClient;
}
