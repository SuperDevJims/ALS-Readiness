import type { ReactNode } from "react";
import { Navigate } from "react-router";
import { useAuthStore } from "../../lib/store/authStore";
import { useLegacyNavigate } from "../../lib/navigation";
import { AccessDenied } from "../components/shared/AccessDenied";
import type { Role } from "../../lib/api/types";

/** Redirects to /login if there's no active session. */
export function RequireAuth({ children }: { children: ReactNode }) {
  const user = useAuthStore((s) => s.user);

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

/** Renders AccessDenied (in place, no redirect) if the current role isn't allowed. */
export function RequireRole({
  allowed,
  children,
}: {
  allowed: Role[];
  children: ReactNode;
}) {
  const role = useAuthStore((s) => s.role);
  const navigate = useLegacyNavigate();

  if (!role || !allowed.includes(role)) {
    return <AccessDenied role={role} navigate={navigate} />;
  }

  return <>{children}</>;
}
