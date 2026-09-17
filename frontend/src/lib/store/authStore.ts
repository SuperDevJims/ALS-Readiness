import { create } from "zustand";
import * as authApi from "../api/auth";
import type { Role, UserMe } from "../api/types";

/**
 * `name`/`email` are derived from the real profile (see `fromUserMe`) so
 * every existing page/AppLayout that reads `user.name`/`user.email` keeps
 * working unchanged; `raw` carries the full UserMe for anything that needs
 * more than that.
 */
export interface StoreUser {
  name: string;
  email: string;
  role: Role;
  id_no?: string;
  raw?: UserMe;
}

interface AuthState {
  user: StoreUser | null;
  role: Role | null;
  accessToken: string | null;
  /** Router waits on this before rendering any guarded route. */
  sessionCheckComplete: boolean;

  setAccessToken: (token: string | null) => void;
  clearSession: () => void;

  /** Real POST /api/auth/login, then populates user via /me. Throws on failure - caller shows the error. */
  login: (idNo: string, password: string) => Promise<void>;

  /** Clears local session immediately, synchronously - never blocks on the network call. */
  logout: () => void;

  /** Re-derives the store's user/role from a fresh UserMe (e.g. after a profile edit). */
  refreshUser: (me: UserMe) => void;

  /** App-mount bootstrap: silent refresh -> populate via /me. Always resolves. */
  bootstrap: () => Promise<void>;
}

function fromUserMe(me: UserMe): StoreUser {
  const name = `${me.profile.first_name} ${me.profile.last_name}`.trim();
  return {
    name: name || me.id_no,
    email: me.profile.contact_email ?? "",
    role: me.role,
    id_no: me.id_no,
    raw: me,
  };
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  role: null,
  accessToken: null,
  sessionCheckComplete: false,

  setAccessToken: (token) => set({ accessToken: token }),

  clearSession: () => set({ user: null, role: null, accessToken: null }),

  login: async (idNo, password) => {
    const { access_token } = await authApi.login(idNo, password);
    set({ accessToken: access_token });

    const me = await authApi.getMe();
    set({ user: fromUserMe(me), role: me.role });
  },

  refreshUser: (me) => set({ user: fromUserMe(me), role: me.role }),

  logout: () => {
    // Clear immediately - a user who explicitly logs out sees it happen right
    // away, regardless of whether the network call succeeds, hangs, or fails.
    get().clearSession();
    authApi.logout().catch(() => {
      // Best-effort - local session is already cleared either way.
    });
  },

  bootstrap: async () => {
    try {
      const { access_token } = await authApi.refresh();
      set({ accessToken: access_token });

      const me = await authApi.getMe();
      set({ user: fromUserMe(me), role: me.role });
    } catch {
      set({ user: null, role: null, accessToken: null });
    } finally {
      set({ sessionCheckComplete: true });
    }
  },
}));

// Dev-only console access for manual verification - see client.ts.
if (import.meta.env.DEV) {
  (window as unknown as { __authStore: typeof useAuthStore }).__authStore = useAuthStore;
}
