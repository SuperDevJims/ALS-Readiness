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

  /** Real POST /api/auth/login, then populates user via /me. Throws on failure - caller shows the error. */
  login: (idNo: string, password: string) => Promise<void>;

  /** Still used by ProfileSetup's own mock completion flow - that page isn't in this phase's scope. */
  loginMock: (role: Role, name: string, email: string) => void;

  /** Clears local session immediately, synchronously - never blocks on the network call. */
  logout: () => void;

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

  loginMock: (role, name, email) => set({ user: { role, name, email }, role }),

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
