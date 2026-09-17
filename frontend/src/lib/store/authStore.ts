import { create } from "zustand";
import * as authApi from "../api/auth";
import type { Role, UserMe } from "../api/types";

/**
 * The shape every existing page/AppLayout already expects (`user.name`,
 * `user.email`, `user.role`) preserved from the pre-backend mock login, plus
 * the real UserMe fields once a real session exists. Phase 2 rewires Login's
 * own submit logic to the real API - this store just needs to hold whichever
 * shape produced the session without breaking pages that read `.name`/`.email`.
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

  /** Back-compat for the current mock demo login (Login's real submit logic is Phase 2's job). */
  loginMock: (role: Role, name: string, email: string) => void;

  logout: () => Promise<void>;

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

  loginMock: (role, name, email) => set({ user: { role, name, email }, role }),

  logout: async () => {
    try {
      await authApi.logout();
    } catch {
      // Best-effort - clear local session regardless of network/API outcome.
    }
    get().clearSession();
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
