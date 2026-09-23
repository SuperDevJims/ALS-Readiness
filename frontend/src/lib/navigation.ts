import { useNavigate } from "react-router";
import type { Role } from "./api/types";

// A navigate() ref that code outside the React tree (axios interceptors) can
// call. Wired up once from inside the router via NavigationBridge.
type NavigateFn = (path: string) => void;

let navigateRef: NavigateFn | null = null;

export function setNavigateRef(fn: NavigateFn) {
  navigateRef = fn;
}

export function redirect(path: string) {
  if (navigateRef) {
    navigateRef(path);
  } else {
    // Fallback if called before the router mounts (shouldn't normally happen).
    window.location.assign(path);
  }
}

/**
 * Every existing page/AppLayout calls `navigate("some-page-key")` (no leading
 * slash - a holdover from the old currentPage-string router). Routes are
 * defined at the matching path (`/some-page-key`), so this is a pure
 * translation layer - it lets every page keep calling navigate() exactly as
 * before while it's actually real router navigation underneath.
 */
export function toPath(page: string): string {
  return page === "landing" ? "/" : `/${page}`;
}

/** Hook version of `toPath`-wrapped navigate, for use inside components. */
export function useLegacyNavigate() {
  const navigate = useNavigate();
  return (page: string) => navigate(toPath(page));
}

/** The forced-password-change page. Deliberately outside ProtectedPage - see App.tsx. */
export const CHANGE_PASSWORD_PATH = "/change-password";

/** The page key for a role's home dashboard, post-login. */
export function homeForRole(role: Role): string {
  return role === "facilitator" ? "facilitator-dashboard"
       : role === "admin"       ? "admin-dashboard"
       : "learner-dashboard";
}
