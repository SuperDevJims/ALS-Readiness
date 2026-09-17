import { apiClient } from "./client";
import type { TokenResponse, UserMe } from "./types";

/** POST /api/auth/login - form-encoded (OAuth2PasswordRequestForm: username/password) */
export async function login(idNo: string, password: string): Promise<TokenResponse> {
  const form = new URLSearchParams();
  form.set("username", idNo);
  form.set("password", password);

  const res = await apiClient.post<TokenResponse>("/api/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return res.data;
}

/** POST /api/auth/refresh - no body; refresh token is read from the httpOnly cookie */
export async function refresh(): Promise<TokenResponse> {
  const res = await apiClient.post<TokenResponse>("/api/auth/refresh");
  return res.data;
}

/** POST /api/auth/logout - 204 No Content */
export async function logout(): Promise<void> {
  await apiClient.post("/api/auth/logout");
}

/** GET /api/users/me */
export async function getMe(): Promise<UserMe> {
  const res = await apiClient.get<UserMe>("/api/users/me");
  return res.data;
}
