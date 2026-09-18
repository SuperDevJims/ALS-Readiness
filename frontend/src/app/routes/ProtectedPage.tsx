import type { ComponentType } from "react";
import { useAuthStore } from "../../lib/store/authStore";
import { useLegacyNavigate } from "../../lib/navigation";
import { RequireAuth, RequireRole } from "./guards";
import type { Role } from "../../lib/api/types";

/**
 * Wraps a page component with the auth/role guards and supplies it the same
 * `{ navigate, user, onLogout }` prop shape every page already expects (the
 * old `lp` spread in App.tsx) - no page's internals change.
 */
export function ProtectedPage({
  allowed,
  Component,
}: {
  allowed: Role[];
  Component: ComponentType<{ navigate: (page: string) => void; user: unknown; onLogout: () => void }>;
}) {
  const user = useAuthStore((s) => s.user);
  const navigate = useLegacyNavigate();

  const onLogout = () => {
    useAuthStore.getState().logout();
    navigate("login");
  };

  return (
    <RequireAuth>
      <RequireRole allowed={allowed}>
        <Component navigate={navigate} user={user} onLogout={onLogout} />
      </RequireRole>
    </RequireAuth>
  );
}
